# -*- coding: utf-8 -*-
# Copyright (C) 2021 Gerardo Kessler <ReaperYOtrasYerbas@gmail.com>
# This file is covered by the GNU General Public License.

import appModuleHandler
from scriptHandler import script
from NVDAObjects.IAccessible.ia2Web import Ia2Web
import api
import winUser
import controlTypes
from ui import message
import winsound
import addonHandler
from re import search
from threading import Thread
from time import sleep
import speech
from keyboardHandler import KeyboardInputGesture

# Lína de traducción
addonHandler.initTranslation()

class AppModule(appModuleHandler.AppModule):

	disableBrowseModeByDefault=True
	messageObj = None
	x = 0
	chatList = []

	def event_NVDAObject_init(self, obj):
		try:
			if obj.IA2Attributes["class"] == 'dNn0f':
				# Translators: Etiquetado del botón mensaje de voz
				obj.name = _('Mensaje de voz')
			elif obj.IA2Attributes["class"] == 'SncVf _3doiV':
				# Translators: Etiquetado del botón reenviar mensaje
				obj.name = _('Reenviar')
		except:
			pass

	def event_gainFocus(self, obj, nextHandler):
		try:
			if search("focusable-list-item", obj.IA2Attributes['class']):
				self.messageObj = obj
				nextHandler()
			elif obj.firstChild.IA2Attributes['class'] == 'SncVf _3doiV':
				obj.firstChild.doAction()
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
			if search("focusable-list-item", obj.IA2Attributes['class']):
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
				Thread(target=self.interruptedSpeech, args=( recButton.name, 0.2)).start()
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
				Thread(target=self.interruptedSpeech, args=( toAttachButton.name, 0.4)).start()
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
				if h.IA2Attributes['class'] == '_1UTQ6 _1s_fV':
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
		description="reproduce los videos adjuntados como tal",
		gesture="kb:control+shift+v"
	)
	def script_playVideo(self, gesture):
		fc = api.getFocusObject()
		try:
			for child in fc.recursiveDescendants:
				if child.role == controlTypes.ROLE_STATICTEXT and child.IA2Attributes['display'] == "block" and child.previous.role == controlTypes.ROLE_GRAPHIC:
					child.doAction()
					# Translators: Verbalización que informa que el proceso se está cargando
					Thread(target=self.interruptedSpeech, args=(_('Cargando...'), 0.2)).start()
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
		self.chatList[self.x].setFocus()

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
