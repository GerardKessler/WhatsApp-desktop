# -*- coding: utf-8 -*-
# Copyright (C) 2021 Gerardo Kessler <ReaperYOtrasYerbas@gmail.com>
# This file is covered by the GNU General Public License.
# Canal de actualización y creación de ventanas por Héctor J. Benítez Corredera <xebolax@gmail.com>

import appModuleHandler
from scriptHandler import script
from NVDAObjects.IAccessible.ia2Web import Ia2Web
import api
import winUser
import controlTypes
import globalVars
from ui import message
import winsound
from re import search
from threading import Thread
from time import sleep
import speech
from keyboardHandler import KeyboardInputGesture
import urllib.request
import json
import gui
import config
from gui.settingsDialogs import NVDASettingsDialog, SettingsPanel
from gui import guiHelper, nvdaControls
import wx
import addonHandler
import core
import socket
import shutil
import os
import sys

# Lína de traducción
addonHandler.initTranslation()

def initConfiguration():
	confspec = {
		'isUpgrade':'boolean(default=False)',
	}
	config.conf.spec['WhatsApp'] = confspec

def getConfig(key):
	value = config.conf["WhatsApp"][key]
	return value

def setConfig(key, value):
	try:
		config.conf.profiles[0]["WhatsApp"][key] = value
	except:
		config.conf["WhatsApp"][key] = value

initConfiguration()
tempPropiedad = getConfig("isUpgrade")
IS_WinON = False
ID_TRUE = wx.NewIdRef()
ID_FALSE = wx.NewIdRef()

class AppModule(appModuleHandler.AppModule):

	def __init__(self, *args, **kwargs):
		super(AppModule, self).__init__(*args, **kwargs)
		NVDASettingsDialog.categoryClasses.append(WhatsAppPanel)
		self._MainWindows = HiloComplemento(1)
		self._MainWindows.start()
		self.messageObj = None
		self.x = 0
		self.chatList = []

	disableBrowseModeByDefault=True

	def terminate(self):
		try:
			NVDASettingsDialog.categoryClasses.remove(WhatsAppPanel)
		except:
			pass

	def event_NVDAObject_init(self, obj):
		try:
			if obj.IA2Attributes["class"] == 'dNn0f':
				# Translators: Etiquetado del botón mensaje de voz
				obj.name = _('Mensaje de voz')
			elif obj.IA2Attributes["class"] == '_165_h _2HL9j':
				# Translators: Etiquetado del botón enviar
				obj.name = _('enviar')
		except:
			pass

	def event_gainFocus(self, obj, nextHandler):
		try:
			if search("focusable-list-item", obj.IA2Attributes['class']):
				self.messageObj = obj
				nextHandler()
			elif obj.firstChild.IA2Attributes['class'] == '_165_h _2HL9j':
				obj.firstChild.doAction()
				message(obj.firstChild.name)
				nextHandler()
			else:
				nextHandler()
		except:
			nextHandler()
		try:
			if obj.children[0].children[1].children[0].IA2Attributes['class'] == '_3h3LX _34ybp app-wrapper-native os-win':
				self.messageObj.setFocus()
				nextHandler()
			else:
				nextHandler()
		except:
			nextHandler()

	def event_valueChange(self, obj, nextHandler):
		return

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		try:
			if obj.role == controlTypes.ROLE_SLIDER:
				clsList.insert(0, Rate)
			elif search("focusable-list-item", obj.IA2Attributes['class']):
				clsList.insert(0, SelectMessages)
				clsList.insert(0, WhatsAppMessage)
		except:
			pass

	def interruptedSpeech(self, message, time):
		try:
			speech.speechMode = speech.speechMode_off
			sleep(time)
			speech.speechMode = speech.speechMode_talk
			message(message)
		except TypeError:
			pass

	@script(
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Presiona y suelta el botón de grabación'),
		category="WhatsApp",
		gesture="kb:control+r"
	)
	def script_record(self, gesture):
		focus = api.getFocusObject()
		try:
			if focus.IA2Attributes['class'] == '_13r35 _1IP_h':
				winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
				winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
				self.messageObj.setFocus()
			elif focus.IA2Attributes['class'] == '_13NKt copyable-text selectable-text' or search("focusable-list-item", focus.IA2Attributes['class']):
				recButton = api.getForegroundObject().children[0].children[1].children[0].children[0].children[1].children[0].children[1].children[0].children[0].children[3].children[0].children[4].children[0].children[2].children[1].children[0].children[0]
				api.moveMouseToNVDAObject(recButton)
				winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
				winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
				winsound.PlaySound("C:\Windows\Media\Windows Pop-up Blocked.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
				Thread(target=self.interruptedSpeech, args=( recButton.name, 0.3)).start()
		except (KeyError, IndexError):
			pass

	@script(
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Presiona el botón para adjuntar'),
		category="WhatsApp",
		gesture="kb:control+shift+a"
	)
	def script_toAttach(self, gesture):
		focus = api.getFocusObject()
		try:
			if focus.IA2Attributes['class'] == '_13NKt copyable-text selectable-text' or search("focusable-list-item", focus.IA2Attributes['class']):
				toAttachButton = api.getForegroundObject().children[0].children[1].children[0].children[0].children[1].children[0].children[1].children[0].children[0].children[3].children[0].children[4].children[0].children[1].children[0]
				toAttachButton.setFocus()
				Thread(target=self.interruptedSpeech, args=(toAttachButton.name, 0.4)).start()
				sleep(0.3)
				KeyboardInputGesture.fromName("space").send()
				KeyboardInputGesture.fromName("downarrow").send()
		except KeyError:
			# Translators: Mensaje que anuncia la disponibilidad de ejecución solo desde el cuadro de edición del mensaje
			message(_('Opción  disponible solo desde un chat'))

	@script(
		# Translators: Descripción del elemento en el diálogo de gestos de entrada
		description= _('Abre el link del mensaje en el navegador predeterminado del sistema'),
		category="WhatsApp",
		gesture="kb:control+l"
	)
	def script_linkOpen(self, gesture):
		obj = api.getFocusObject()
		for o in obj.recursiveDescendants:
			if getattr(o, "role", None) == controlTypes.ROLE_LINK:
				o.doAction()
				break

	@script(
		# Translators: Descripción del elemento en el diálogo de gestos de entrada
		description= _('Copia el texto del mensaje con el foco al portapapeles'),
		category="WhatsApp",
		gesture="kb:control+shift+c"
	)
	def script_textCopy(self, gesture):
		focus = api.getFocusObject()
		if focus.role == controlTypes.ROLE_SECTION:
			list= [str.name for str in focus.recursiveDescendants if str.role == controlTypes.ROLE_STATICTEXT and str.name != None and str.name != "~"]
			messageList = ". ".join(list[:-1])
			api.copyToClip(messageList)
			winsound.PlaySound("C:\\Windows\\Media\\Windows Recycle.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
		else:
			# Translators: Informa la disponibilidad de la función solo desde la lista de mensajes
			message(_('Solo disponible desde la lista de mensajes'))

	@script(
		category="WhatsApp",
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Se mueve al mensaje respondido'),
		gesture="kb:alt+control+enter"
	)
	def script_replyMessage(self, gesture):
		focus = api.getFocusObject()
		for fc in focus.recursiveDescendants:
			try:
				if fc.IA2Attributes['class'] == '_3Ppzm' or fc.IA2Attributes['class'] == '_3o5fT':
					fc.doAction()
					# Translators: Informa que se está enfocando el mensaje respondido
					message(_('Enfocando el mensaje respondido...'))
					break
			except:
				pass

	@script(
		category="WhatsApp",
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Activa el menú del chat'),
		gesture="kb:control+m"
	)
	def script_menuButton(self, gesture):
		focus = api.getFocusObject()
		if not hasattr(focus, 'IA2Attributes'): return
		titleObj = api.getForegroundObject().children[0].children[1].children[0].children[0].children[1].children[0].children[1].children[0].children[0].children[3].children[0].children[1]
		if titleObj.childCount == 5:
			titleObj.children[3].children[0].doAction()
		elif titleObj.childCount == 7:
			titleObj.children[5].children[0].doAction()
		# Translators: Verbaliza menú del chat
		message(_('Menú del chat'))

	@script(
		category="WhatsApp",
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Activa el botón menú general'),
		gesture="kb:control+g"
	)
	def script_generalMenuButton(self, gesture):
		focus = api.getFocusObject()
		if not hasattr(focus, 'IA2Attributes'): return
		try:
			api.getForegroundObject().children[0].children[1].children[0].children[0].children[1].children[0].children[1].children[0].children[0].children[2].children[0].children[0].children[3].children[0].doAction()
			# Translators: Verbaliza menú general
			message(_('Menú general'))
		except AttributeError:
			pass

	@script(
		category="WhatsApp",
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Pulsa en el botón descargar cuando el mensaje contiene un archivo descargable'),
		gesture="kb:alt+enter"
	)
	def script_fileDownload(slef, gesture):
		fc = api.getFocusObject()
		for h in fc.recursiveDescendants:
			try:
				if h.IA2Attributes['class'] == 'UQz9- _1_Wyj':
					h.doAction()
					break
			except:
				pass

	@script(
		category="WhatsApp",
		# Translators: Descripción del elemento en el diálogo de gestos de entrada
		description= _('Verbaliza el tiempo  del mensaje en reproducción, o la duración del mensaje en grabación'),
		gesture='kb:control+t'
	)
	def script_timeAnnounce(self, gesture):
		fc = api.getFocusObject()
		if fc.role == controlTypes.ROLE_SLIDER:
			# Translators: Artículo que divide entre el tiempo actual y la duración total del mensaje.
			time = fc.value.replace("/", _(' de '))
			message(time)
		elif fc.role == controlTypes.ROLE_BUTTON and fc.next.firstChild.role == controlTypes.ROLE_STATICTEXT:
			message(fc.next.firstChild.name)
		elif fc.parent.IA2Attributes['class'] == 'h4Qs-':
			str = fc.parent.children[1].children[1].children[0].children[0].name
			message(str)

	@script(
		# Translators: Descripción del elemento en el diálogo de gestos de entrada
		description= _('Anuncia el nombre del chat'),
		category='WhatsApp',
		gesture='kb:control+shift+t'
	)
	def script_chatAnnounce(self, gesture):
		fc = api.getFocusObject()
		try:
			if fc.parent.IA2Attributes['class'] == 'y8WcF':
				chatNameButton = fc.parent.parent.parent.previous.previous.children[1]
				if len(chatNameButton.name) > 30:
					message(chatNameButton.children[0].children[0].name)
				else:
					message(chatNameButton.name)
		except:
			pass

	@script(
		category="WhatsApp",
		# Translators: Descripción del elemento en el diálogo de gestos de entrada
		description= _('reproduce los videos adjuntados como tal'),
		gesture="kb:control+shift+v"
	)
	def script_playVideo(self, gesture):
		fc = api.getFocusObject()
		try:
			for child in fc.recursiveDescendants:
				if child.role == controlTypes.ROLE_STATICTEXT and child.IA2Attributes['display'] == "block" and child.previous.role == controlTypes.ROLE_GRAPHIC:
					child.doAction()
					Thread(target=self.interruptedSpeech, args=(self.loadingStr, 0.2)).start()
					break
		except:
			pass

	@script(
		category="WhatsApp",
		# Translators: Descripción del elemento en el diálogo de gestos de entrada
		description= _('Retrocede 5 mensajes en la lista'),
		gesture="kb:control+upArrow"
	)
	def script_messagesBack(self, gesture):
		fc = api.getFocusObject()
		try:
			if not search('focusable-list-item', fc.IA2Attributes['class']): return
		except KeyError:
			return
		try:
			fc.previous.previous.previous.previous.previous.setFocus()
		except AttributeError:
			winsound.PlaySound("C:/Windows/Media/Windows Information Bar.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

	@script(
		category="WhatsApp",
		# Translators: Descripción del elemento en el diálogo de gestos de entrada
		description= _('Avanza 5 mensajes en la lista'),
		gesture="kb:control+downArrow"
	)
	def script_messagesNext(self, gesture):
		fc = api.getFocusObject()
		try:
			if not search('focusable-list-item', fc.IA2Attributes['class']): return
		except KeyError:
			return
		try:
			fc.next.next.next.next.next.setFocus()
		except AttributeError:
			winsound.PlaySound("C:/Windows/Media/Windows Information Bar.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

	@script(
		category="WhatsApp",
		# Translators: Descripción del elemento en el diálogo de gestos de entrada
		description= _('Verbaliza el estado del último mensaje en el chat con el foco'),
		gesture="kb:control+shift+e"
	)
	def script_stateAnnounce(self, gesture):
		fc = api.getFocusObject()
		try:
			if fc.IA2Attributes["xml-roles"] != "row": return
		except:
			return
		foreground = api.getForegroundObject()
		try:
			statusObj = foreground.children[0].children[1].children[0].children[0].children[1].children[0].children[1].children[0].children[0].children[3].children[0].children[3].children[0].children[1].children[-1].name
			status = search(r"\d+\:\d\d.*", statusObj)
			message(status[0])
			return
		except:
			pass
		try:
			statusObj = foreground.children[0].children[1].children[0].children[0].children[1].children[0].children[1].children[0].children[0].children[3].children[0].children[3].children[0].children[0].children[-1].name
			status = search(r"\d+\:\d\d.*", statusObj)
			message(status[0])
			return
		except:
			pass
		winsound.PlaySound("C:/Windows/Media/Windows Information Bar.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

	@script(gesture="kb:alt+rightArrow")
	def script_lastMessageObj(self, gesture):
		if self.messageObj == None: return
		self.messageObj.setFocus()

	@script(
		category="WhatsApp",
		# Translators: Descripción del elemento en el diálogo gestos de entrada.
		description= _('Inicia o finaliza una llamada de voz al contacto del chat con el foco'),
		gesture="kb:alt+control+l"
	)
	def script_audioCall(self, gesture):
		fg = api.getForegroundObject()
		fc = api.getFocusObject()
		try:
			if fc.parent.IA2Attributes['class'] == 'h4Qs-':
				fc.parent.children[5].doAction()
		except:
			pass
		try:
			titleObj = fg.children[0].children[1].children[0].children[0].children[1].children[0].children[1].children[0].children[0].children[3].children[0].children[1]
			if titleObj.childCount != 7:
				# Translators: Mensaje que anuncia que la opción no está disponible.
				message(_('Opción no disponible'))
				return
			titleObj.children[3].children[0].doAction()
		except:
			pass

	@script(
		category="WhatsApp",
		# Translators: Descripción del elemento en el diálogo gestos de entrada.
		description= _('Inicia una llamada de video al contacto del chat con el foco'),
		gesture="kb:alt+control+v"
	)
	def script_videoCall(self, gesture):
		fg = api.getForegroundObject()
		fc = api.getFocusObject()
		try:
			if fc.parent.IA2Attributes['class'] == 'h4Qs-':
				fc.parent.children[5].doAction()
		except:
			pass
		try:
			titleObj = fg.children[0].children[1].children[0].children[0].children[1].children[0].children[1].children[0].children[0].children[3].children[0].children[1]
			if titleObj.childCount != 7:
				# Translators: Mensaje que anuncia que la opción no está disponible.
				message(_('Opción no disponible'))
				return
			titleObj.children[2].children[0].doAction()
		except:
			pass

	@script(
		category="WhatsApp",
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Refresca la lista virtual de chats'),
		gesture="kb:shift+f5"
	)
	def script_refreshTheList(self, gesture):
		try:
			if self.chatList == []:
				self.chatList = [chat.firstChild for chat in api.getForegroundObject().children[0].children[1].children[0].children[0].children[1].children[0].children[1].children[0].children[0].children[2].children[0].children[2].children[0].children[0].children]
			else:
				self.chatList[-18].setFocus()
				self.chatList = [chat.firstChild for chat in api.getForegroundObject().children[0].children[1].children[0].children[0].children[1].children[0].children[1].children[0].children[0].children[2].children[0].children[2].children[0].children[0].children]
			# Translators: Verbaliza que la lista ha sido actualizada
			message(_('Lista actualizada'))
		except:
			pass

	@script(
		category="WhatsApp",
		# Translators: Descripción del elemento en el diáglogo gestos de entrada
		description= _('Chat siguiente en la lista virtual'),
		gesture="kb:shift+downArrow"
)
	def script_nextChat(self, gesture):
		try:
			if self.x < 18:
				self.x+=1
				message(self.chatList[self.x].name)
			else:
				winsound.PlaySound("C:/Windows/Media/Windows Information Bar.wav", winsound.SND_ASYNC | winsound.SND_FILENAME)
		except IndexError:
			message(_('Refresca la lista'))

	@script(
		category="WhatsApp",
		# Translators: Descripción del elemento en el diáglogo gestos de entrada
		description= _('Chat anterior en la lista virtual'),
		gesture="kb:shift+upArrow"
	)
	def script_previousChat(self, gesture):
		try:
			if self.x > -19:
				self.x-=1
				message(self.chatList[self.x].name)
			else:
				winsound.PlaySound("C:/Windows/Media/Windows Information Bar.wav", winsound.SND_ASYNC | winsound.SND_FILENAME)
		except IndexError:
			message(_('Refresca la lista'))

	@script(
		category="WhatsApp",
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Enfoca el chat de la lista virtual'),
		gesture="kb:shift+enter"
	)
	def script_focusChat(self, gesture):
		try:
			self.chatList[self.x].setFocus()
			self.chatList[self.x].doAction()
		except:
			pass

	@script(
		category="WhatsApp",
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Activa y desactiva la verificación de actualizaciones del complemento'),
		gesture="kb:alt+control+u"
	)
	def script_upgradeVerify(self, gesture):
		with open("{}\\addons\\WhatsApp-desktop\\globalPlugins\\upgrade".format(globalVars.appArgs.configPath), "r") as r:
			fileValue = r.read()
		if fileValue == "enabled":
			value = "disabled"
			# Translators: informa que la verificación está desactivada
			message(_('Verificación de actualizaciones desactivada'))
		elif fileValue == "disabled":
			value = "enabled"
			# Translators: informa que la verificación está activada
			message(_('Verificación de actualizaciones activada'))
		with open("{}\\addons\\WhatsApp-desktop\\globalPlugins\\upgrade".format(globalVars.appArgs.configPath), "w") as w:
			w.write(value)

class WhatsAppMessage(Ia2Web):

	messageObj = ""

	def initOverlayClass(self):
		for hs in self.recursiveDescendants:
			try:
				if hs.IA2Attributes['class'] == '_2oSLN':
					self .messageObj = hs
					self.bindGesture("kb:enter", "playMessage")
					break
			except KeyError:
				pass

	def script_playMessage(self, gesture):
		try:
			self.messageObj.doAction()
			self.messageObj.parent.next.children[2].setFocus()
		except:
			pass

class SelectMessages(Ia2Web):

	fg = ""
	actions = ""
	selected = ""
	# Translators: Mensaje que anuncia el requerimiento de al menos un mensaje seleccionado para realizar la acción.
	errorMessage = _('Debes seleccionar al menos un mensaje para realizar esta acción')
	
	def initOverlayClass(self):
		try:
			if self.firstChild.firstChild.role == controlTypes.ROLE_CHECKBOX:
				self.bindGestures({"kb:space":"selection", "kb:delete":"delete", "kb:r": "resend", "kb:s":"selectionAnnounce", "kb:d":"highlight", "kb:q":"close"})
				self.fg = api.getForegroundObject()
				self.actions = self.fg.children[0].children[1].children[0].children[0].children[1].children[0].children[1].children[0].children[0].children[3].children[0].children[5]
		except:
			pass

	def script_selection(self, gesture):
		self.firstChild.firstChild.doAction()
		self.setFocus()
		self.selected = self.actions.children[1]
		if self.firstChild.firstChild.states == {32, 16777216, 134217728}:
			# Translators: Informa que el mensaje ha sido desmarcado
			message(_('Desmarcado'))
		else:
			# Translators: Mensaje que informa que el mensaje ha sido marcado
			message(_('Marcado'))

	def script_delete(self, gesture):
		try:
			self.actions.children[3].doAction()
			if self.selected.name[0] != "0":
				# Translators: Se informa que se realiza la acción eliminar mensajes
				message(_('Eliminar mensajes'))
			else:
				message(self.errorMessage)
		except AttributeError:
			pass

	def script_resend(self, gesture):
		try:
			self.actions.children[4].doAction()
			if self.selected.name[0] != "0":
				# Translators: se informa la acción reenviar mensajes
				message(_('Reenviar mensajes'))
			else:
				message(self.errorMessage)
		except AttributeError:
			pass

	def script_selectionAnnounce(self, gesture):
		self.selected = self.actions.children[1]
		message(self.selected.name)

	def script_highlight(self, gesture):
		try:
			self.actions.children[2].doAction()
			if self.selected.name[0] != "0":
				# Translators: Informa la acción destacar mensajes
				message(_('Destacar mensajes'))
			else:
				message(self.errorMessage)
		except AttributeError:
			pass

	def script_close(self, gesture):
		self.actions.children[0].doAction()
		self.setFocus()
		# Translators: Informa que la edición ha finalizado
		message(_('Edición finalizada'))

class Rate():

	# Translators: Velocidades de los mensajes de voz
	normal = _('normal')
	fast = _('rápido')
	veryFast = _('muy rápido')

	def initOverlayClass(self):
		if self.parent.next.firstChild.firstChild.IA2Attributes['class'] == '_3QEso':
			self.bindGesture("kb:space", "rate")

	def script_rate(self, gesture):
		rateObject = self.parent.next.firstChild.firstChild
		rateObject.doAction()
		self.setFocus()
		if rateObject.name == "1":
			message(self.fast)
		elif rateObject.name == "1.5":
			message(self.veryFast)
		if rateObject.name == "2":
			message(self.normal)

class WhatsAppPanel(SettingsPanel):
	title = "WhatsApp Desktop"

	def makeSettings(self, sizer):
		helper=guiHelper.BoxSizerHelper(self, sizer=sizer)

		# Translators: Nombre de la casilla de verificación para la búsqueda de actualizaciones del menú configuración
		self.whatsappChk = helper.addItem(wx.CheckBox(self, label=_('Buscar actualizaciones al iniciar')))
		self.whatsappChk.Bind(wx.EVT_CHECKBOX, self.onChk)

		self.whatsappChk.Value = tempPropiedad

	def onSave(self):
		setConfig("isUpgrade", self.whatsappChk.Value)

	def onChk(self, event):
		global tempPropiedad
		tempPropiedad = self.whatsappChk.Value

class HiloComplemento(Thread):
	def __init__(self, opcion):
		super(HiloComplemento, self).__init__()

		self.opcion = opcion
		self.daemon = True

	def run(self):
		def upgradeVerify():
			if IS_WinON == False:
				if tempPropiedad == True:
					p = urllib.request.Request("https://api.github.com/repos/GerardKessler/WhatsApp-desktop/releases")
					r = urllib.request.urlopen(p).read()
					githubApi = json.loads(r.decode('utf-8'))
					for addon in addonHandler.getAvailableAddons():
						if addon.manifest['name'] == "WhatsApp-desktop":
							versionInstalada = addon.manifest['version']
					if githubApi[0]["tag_name"] != versionInstalada:
						self._MainWindows = UpdateDialog(gui.mainFrame)
						gui.mainFrame.prePopup()
						self._MainWindows.Show()

		def startUpgrade():
			if IS_WinON == False:
				self._MainWindows = ActualizacionDialogo(gui.mainFrame)
				gui.mainFrame.prePopup()
				self._MainWindows.Show()

		if self.opcion == 1:
			wx.CallAfter(upgradeVerify)
		elif self.opcion == 2:
			wx.CallAfter(startUpgrade)

class HiloActualizacion(Thread):
	def __init__(self, frame):
		super(HiloActualizacion, self).__init__()

		self.frame = frame

		p = urllib.request.Request("https://api.github.com/repos/GerardKessler/WhatsApp-desktop/releases")
		r = urllib.request.urlopen(p).read()
		githubApi = json.loads(r.decode('utf-8'))
		self.nombreUrl = githubApi[0]['assets'][0]['browser_download_url']

		self.directorio = os.path.join(globalVars.appArgs.configPath, "tempWhatsApp")

		self.daemon = True
		self.start()

	def generaFichero(self):
		if os.path.exists(self.directorio) == False:
			os.mkdir(self.directorio)
		nuevoIndex = len(os.listdir(self.directorio))
		return os.path.join(self.directorio, "temp%s.nvda-addon" % nuevoIndex)

	def humanbytes(self, B): # Convierte bytes
		B = float(B)
		KB = float(1024)
		MB = float(KB ** 2) # 1,048,576
		GB = float(KB ** 3) # 1,073,741,824
		TB = float(KB ** 4) # 1,099,511,627,776

		if B < KB:
			return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
		elif KB <= B < MB:
			return '{0:.2f} KB'.format(B/KB)
		elif MB <= B < GB:
			return '{0:.2f} MB'.format(B/MB)
		elif GB <= B < TB:
			return '{0:.2f} GB'.format(B/GB)
		elif TB <= B:
			return '{0:.2f} TB'.format(B/TB)

	def __call__(self, block_num, block_size, total_size):
		readsofar = block_num * block_size
		if total_size > 0:
			percent = readsofar * 1e2 / total_size
			wx.CallAfter(self.frame.onDescarga, percent)
			sleep(1 / 995)
			wx.CallAfter(self.frame.TextoRefresco, _('Por favor Espere... \n' + 'Descargando: %s' % self.humanbytes(readsofar)))
			if readsofar >= total_size:
				pass
		else:
			wx.CallAfter(self.frame.TextoRefresco, _('Por favor espere...\n' + 'Descargando: %s' % self.humanbytes(readsofar)))

	def run(self):
		try:
			fichero = self.generaFichero()
			socket.setdefaulttimeout(15)
			opener = urllib.request.build_opener()
			opener.addheaders = [('User-agent', 'Mozilla/5.0')]
			urllib.request.install_opener(opener)
			urllib.request.urlretrieve(self.nombreUrl, fichero, reporthook=self.__call__)
			bundle = addonHandler.AddonBundle(fichero)
			if not addonHandler.addonVersionCheck.hasAddonGotRequiredSupport(bundle):
				pass
			else:
				bundleName = bundle.manifest['name']
				isDisabled = False
				for addon in addonHandler.getAvailableAddons():
					if bundleName == addon.manifest['name']:
						if addon.isDisabled:
							isDisabled = True
						if not addon.isPendingRemove:
							addon.requestRemove()
						break
				addonHandler.installAddonBundle(bundle)
			# Translators: Mensaje que anuncia la finalización del proceso.
			wx.CallAfter(self.frame.done, _('La actualización se ha completado.\nNVDA necesita ser reiniciado para aplicar los cambios.\nPulsa el botón aceptar para reiniciar o cerrar para finalizar '))
		except:
			# Translators: Mensaje que anuncia la existencia de un error
			wx.CallAfter(self.frame.error, _('Error.\n' + 'CComprueba la conexión a internet y vuelve a intentarlo.\n' + 'Esta ventana puede cerrarse'))
		try:
			shutil.rmtree(self.directorio, ignore_errors=True)
		except:
			pass

class UpdateDialog(wx.Dialog):
	def __init__(self, parent):
		super(UpdateDialog, self).__init__(parent, -1, title='WhatsApp-desktop', size=(350, 150))

		global IS_WinON
		IS_WinON = True
		Panel = wx.Panel(self)

		#Translators: Mensaje que informa de una nueva versión
		label1 = wx.StaticText(Panel, wx.ID_ANY, label=_('Hay una nueva versión del complemento. ¿Quieres descargarla ahora?'))
		self.downloadButton = wx.Button(Panel, wx.ID_ANY, _('&Descargar e instalar'))
		self.downloadButton.Bind(wx.EVT_BUTTON, self.download)
		self.closeButton = wx.Button(Panel, wx.ID_CANCEL, _('&Cerrar'))
		self.closeButton.Bind(wx.EVT_BUTTON, self.close, id=wx.ID_CANCEL)

		sizerV = wx.BoxSizer(wx.VERTICAL)
		sizerH = wx.BoxSizer(wx.HORIZONTAL)

		sizerV.Add(label1, 0, wx.EXPAND | wx.ALL)

		sizerH.Add(self.downloadButton, 2, wx.CENTER)
		sizerH.Add(self.closeButton, 2, wx.CENTER)

		sizerV.Add(sizerH, 0, wx.CENTER)
		Panel.SetSizer(sizerV)

		self.CenterOnScreen()

	def download(self, event):
		global IS_WinON
		IS_WinON = False
		self._MainWindows = HiloComplemento(2)
		self._MainWindows.start()
		self.Destroy()
		gui.mainFrame.postPopup()

	def close(self, event):
		global IS_WinON
		IS_WinON = False
		self.Destroy()
		gui.mainFrame.postPopup()

class ActualizacionDialogo(wx.Dialog):
	def __init__(self, parent):

		#Translators: título de la ventana
		super(ActualizacionDialogo, self).__init__(parent, -1, title=_('Actualizando WhatsApp Desktop'), size=(550, 400))

#		self.SetSize((400, 130))
		self.CenterOnScreen()

		global IS_WinON
		IS_WinON = True

		self.Panel = wx.Panel(self)

		self.ProgressDescarga=wx.Gauge(self.Panel, wx.ID_ANY, range=100, style = wx.GA_HORIZONTAL)
		self.textorefresco = wx.TextCtrl(self.Panel, wx.ID_ANY, style =wx.TE_MULTILINE|wx.TE_READONLY)
		self.textorefresco.Bind(wx.EVT_CONTEXT_MENU, self.skip)

		#Translators: nombre del botón aceptar
		self.AceptarTRUE = wx.Button(self.Panel, ID_TRUE, _('&Aceptar'))
		self.Bind(wx.EVT_BUTTON, self.onAceptarTRUE, id=self.AceptarTRUE.GetId())
		self.AceptarTRUE.Disable()

		self.AceptarFALSE = wx.Button(self.Panel, ID_FALSE, "&Cerrar")
		self.Bind(wx.EVT_BUTTON, self.onAceptarFALSE, id=self.AceptarFALSE.GetId())
		self.AceptarFALSE.Disable()

		self.Bind(wx.EVT_CLOSE, self.onNull)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer_botones = wx.BoxSizer(wx.HORIZONTAL)

		sizer.Add(self.ProgressDescarga, 0, wx.EXPAND)
		sizer.Add(self.textorefresco, 1, wx.EXPAND)

		sizer_botones.Add(self.AceptarTRUE, 2, wx.CENTER)
		sizer_botones.Add(self.AceptarFALSE, 2, wx.CENTER)

		sizer.Add(sizer_botones, 0, wx.EXPAND)

		self.Panel.SetSizer(sizer)

		HiloActualizacion(self)

		self.textorefresco.SetFocus()

	def skip(self, event):
		return

	def onNull(self, event):
		pass

	def onDescarga(self, event):
		self.ProgressDescarga.SetValue(event)

	def TextoRefresco(self, event):
		self.textorefresco.Clear()
		self.textorefresco.AppendText(event)

	def done(self, event):
		winsound.MessageBeep(0)
		self.AceptarTRUE.Enable()
		self.AceptarFALSE.Enable()
		self.textorefresco.Clear()
		self.textorefresco.AppendText(event)
		self.textorefresco.SetInsertionPoint(0) 

	def error(self, event):
		winsound.MessageBeep(16)
		self.AceptarFALSE.Enable()
		self.textorefresco.Clear()
		self.textorefresco.AppendText(event)
		self.textorefresco.SetInsertionPoint(0) 

	def onAceptarTRUE(self, event):
		global IS_WinON
		IS_WinON = False
		self.Destroy()
		gui.mainFrame.postPopup()
		core.restart()

	def onAceptarFALSE(self, event):
		global IS_WinON
		IS_WinON = False
		self.Destroy()
		gui.mainFrame.postPopup()
