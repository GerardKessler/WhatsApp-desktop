# -*- coding: utf-8 -*-
# Copyright (C) 2021 Gerardo Kessler <ReaperYOtrasYerbas@gmail.com>
# This file is covered by the GNU General Public License.

import appModuleHandler
from scriptHandler import script
from NVDAObjects.IAccessible.ia2Web import Ia2Web
import api
import winUser
import controlTypes
from ui import message as msg
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
	space = KeyboardInputGesture.fromName("space")

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
		pass

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		try:
			if search("focusable-list-item", obj.IA2Attributes['class']):
				clsList.insert(0, SelectMessages)
				clsList.insert(0, WhatsAppMessage)
		except:
			pass

	def interruptedSpeech(self, message, time):
		speech.speechMode = speech.speechMode_off
		sleep(time)
		speech.speechMode = speech.speechMode_talk
		msg(message)

	@script(
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Presiona y suelta el botón de grabación'),
		category="WhatsApp",
		gesture="kb:control+r"
	)
	def script_record(self, gesture):
		focus = api.getFocusObject()
		try:
			if focus.IA2Attributes['class'] == '_1LPa8 _3DaI4':
				winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
				winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
				self.messageObj.setFocus()
			elif focus.IA2Attributes['class'] == '_2_1wd copyable-text selectable-text' and focus.value == '':
				recButton = focus.parent.parent.next.firstChild
				api.moveMouseToNVDAObject(recButton)
				winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
				winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
				winsound.PlaySound("C:\Windows\Media\Windows Pop-up Blocked.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
				Thread(target=self.interruptedSpeech, args=( recButton.name, 0.2)).start()
			elif focus.parent.IA2Attributes['class'] == '_11liR':
				recButton = focus.parent.parent.parent.next.firstChild.firstChild.next.next.next.firstChild
				api.moveMouseToNVDAObject(recButton)
				winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
				winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
				winsound.PlaySound("C:\Windows\Media\Windows Pop-up Blocked.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
				Thread(target=self.interruptedSpeech, args=( recButton.name, 0.3)).start()
		except KeyError:
			pass

	@script(
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Presiona el botón para adjuntar'),
		category="WhatsApp",
		gesture="kb:control+shift+a"
	)
	def script_toAttach(self, gesture):
		focus = api.getFocusObject()
		fg = api.getForegroundObject()
		try:
			if focus.IA2Attributes['class'] == '_2_1wd copyable-text selectable-text' or search("focusable-list-item", focus.IA2Attributes['class']):
				toAttachButton = fg.children[0].children[1].children[0].children[0].children[1].children[0].children[1].children[0].children[0].children[3].children[0].children[4].children[0].children[1].children[0]
				toAttachButton.setFocus()
				Thread(target=self.interruptedSpeech, args=( toAttachButton.name, 0.4)).start()
				sleep(0.3)
				self.space.send()
		except KeyError:
			# Translators: Mensaje que anuncia la disponibilidad de ejecución solo desde el cuadro de edición del mensaje
			msg(_('Opción solo disponible desde el cuadro de edición de mensaje'))

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
			list= [str.name for str in focus.recursiveDescendants if str.role == controlTypes.ROLE_STATICTEXT and str.name != None]
			if list[0] == "~":
				message = ". ".join(list[1:-1])
				api.copyToClip(message)
				# Translators: Informa que el mensaje ha sido copiado
				msg(_('Copiado'))
			else:
				message = ". ".join(list[:-1])
				api.copyToClip(message)
				# Translators: Informa que el mensaje ha sido copiado
				msg(_('Copiado'))
		else:
			# Translators: Informa la disponibilidad de la función solo desde la lista de mensajes
			msg(_('Solo disponible desde la lista de mensajes'))

	@script(
		category="WhatsApp",
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Se mueve al mensaje respondido'),
		gesture="kb:shift+enter"
	)
	def script_replyMessage(self, gesture):
		focus = api.getFocusObject()
		for fc in focus.recursiveDescendants:
			try:
				if fc.IA2Attributes['class'] == '_3Ppzm':
					fc.doAction()
					# Translators: Informa que se está enfocando el mensaje respondido
					msg(_('Enfocando el mensaje respondido...'))
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
		if focus.parent.IA2Attributes['class'] == '_11liR':
			titleObj = focus.parent.parent.parent.previous.previous
			if titleObj.childCount == 7:
				titleObj.children[5].firstChild.doAction()
				# Translators: Verbaliza menú del chat
				msg(_('Menú del chat'))
			elif titleObj.childCount == 5:
				titleObj.children[3].firstChild.doAction()
				# Translators: Verbaliza menú del chat
				msg(_('Menú del chat'))

	@script(
		category="WhatsApp",
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Activa el botón menú general'),
		gesture="kb:control+g"
	)
	def script_generalMenuButton(self, gesture):
		focus = api.getFocusObject()
		fg = api.getForegroundObject
		if not hasattr(focus, 'IA2Attributes'): return
		try:
			if focus.role == controlTypes.ROLE_TABLEROW:
				fg.children[0].children[1].children[0].children[0].children[1].children[0].children[1].children[0].children[0].children[2].children[0].children[0].children[3].children[0].doAction()
			elif focus.parent.IA2Attributes['class'] == '_11liR':
				focus.parent.parent.parent.parent.parent.previous.firstChild.firstChild.firstChild.next.next.next.firstChild.doAction()
			# Translators: Verbaliza menú general
			msg(_('Menú general'))
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
		description= _('Verbaliza la posición en segundos del mensaje de voz'),
		gesture='kb:control+t'
	)
	def script_timeAnnounce(self, gesture):
		fc = api.getFocusObject()
		if fc.role == controlTypes.ROLE_SLIDER:
			# Translators: Artículo que divide entre el tiempo actual y la duración total del mensaje.
			time = str(fc.value).replace(" / ", _(', de '))
			msg(time)
		elif fc.role == controlTypes.ROLE_BUTTON and fc.next.firstChild.role == controlTypes.ROLE_STATICTEXT:
			msg(fc.next.firstChild.name)
		elif fc.parent.IA2Attributes['class'] == 'C4Aab':
			str = fc.parent.children[1].children[1].children[0].children[0].name
			msg(str)


	@script(
		# Translators: Descripción del elemento en el diálogo de gestos de entrada
		description= _('Anuncia el nombre del chat'),
		category='WhatsApp',
		gesture='kb:control+shift+t'
	)
	def script_chatAnnounce(self, gesture):
		fc = api.getFocusObject()
		fg = api.getForegroundObject()
		try:
			if fc.parent.IA2Attributes['class'] == '_11liR':
				chatNameButton = fg.children[0].children[1].children[0].children[0].children[1].children[0].children[1].children[0].children[0].children[3].children[0].children[1].children[1]
				if len(chatNameButton.name) > 30:
					msg(chatNameButton.children[0].children[0].name)
				else:
					msg(chatNameButton.name)
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
			msg(status[0])
			return
		except:
			pass
		try:
			statusObj = foreground.children[0].children[1].children[0].children[0].children[1].children[0].children[1].children[0].children[0].children[3].children[0].children[3].children[0].children[0].children[-1].name
			status = search(r"\d+\:\d\d.*", statusObj)
			msg(status[0])
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
			if fc.parent.IA2Attributes['class'] == 'C4Aab':
				fc.parent.children[5].doAction()
		except:
			pass
		try:
			audioCallObj = fg.children[0].children[1].children[0].children[0].children[1].children[0].children[1].children[0].children[0].children[3].children[0].children[1].children[3].children[0]
			if fg.children[0].children[1].children[0].children[0].children[1].children[0].children[1].children[0].children[0].children[3].children[0].children[1].childCount != 7:
				# Translators: Mensaje que anuncia que la opción no está disponible.
				msg(_('Opción no disponible'))
				return
			if audioCallObj.IA2Attributes['class'] == '_1XaX-':
				audioCallObj.doAction()
			else:
				# Translators: Anuncia que la opción no está disponible.
				msg(_('Opción no disponible'))
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
			if fc.parent.IA2Attributes['class'] == 'C4Aab':
				fc.parent.children[5].doAction()
		except:
			pass
		try:
			videoCallObj = fg.children[0].children[1].children[0].children[0].children[1].children[0].children[1].children[0].children[0].children[3].children[0].children[1].children[2].children[0]
			if fg.children[0].children[1].children[0].children[0].children[1].children[0].children[1].children[0].children[0].children[3].children[0].children[1].childCount != 7:
				# Translators: Mensaje que anuncia que la opción no está disponible.
				msg(_('Opción no disponible'))
				return
			if videoCallObj.IA2Attributes['class'] == '_1XaX-':
				videoCallObj.doAction()
		except:
			pass

class WhatsAppMessage(Ia2Web):
	def initOverlayClass(self):
		for hs in self.recursiveDescendants:
			try:
				if hs.IA2Attributes['class'] == '_2HtgQ':
					self.bindGesture("kb:enter", "playMessage")
					break
			except KeyError:
				pass

	def script_playMessage(self, gesture):
		for f in self.recursiveDescendants:
			try:
				if f.IA2Attributes['class'] == '_2HtgQ':
					f.doAction()
					f.parent.next.children[2].setFocus()
					break
			except KeyError:
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
			msg(_('Desmarcado'))
		else:
			# Translators: Mensaje que informa que el mensaje ha sido marcado
			msg(_('Marcado'))

	def script_delete(self, gesture):
		try:
			self.actions.children[3].doAction()
			if self.selected.name[0] != "0":
				# Translators: Se informa que se realiza la acción eliminar mensajes
				msg(_('Eliminar mensajes'))
			else:
				msg(self.errorMessage)
		except AttributeError:
			pass

	def script_resend(self, gesture):
		try:
			self.actions.children[4].doAction()
			if self.selected.name[0] != "0":
				# Translators: se informa la acción reenviar mensajes
				msg(_('Reenviar mensajes'))
			else:
				msg(self.errorMessage)
		except AttributeError:
			pass

	def script_selectionAnnounce(self, gesture):
		self.selected = self.actions.children[1]
		msg(self.selected.name)

	def script_highlight(self, gesture):
		try:
			self.actions.children[2].doAction()
			if self.selected.name[0] != "0":
				# Translators: Informa la acción destacar mensajes
				msg(_('Destacar mensajes'))
			else:
				msg(self.errorMessage)
		except AttributeError:
			pass

	def script_close(self, gesture):
		self.actions.children[0].doAction()
		self.setFocus()
		# Translators: Informa que la edición ha finalizado
		msg(_('Edición finalizada'))
