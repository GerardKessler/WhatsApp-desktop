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

# Lína de traducción
addonHandler.initTranslation()

class AppModule(appModuleHandler.AppModule):

	disableBrowseModeByDefault=True

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
			if obj.firstChild.IA2Attributes['class'] == 'SncVf _3doiV':
				obj.firstChild.doAction()
				nextHandler()
			elif obj.children[0].children[0].children[0].children[2].role == controlTypes.ROLE_BUTTON and obj.children[0].children[0].children[0].children[3].role == controlTypes.ROLE_BUTTON and obj.children[0].children[0].children[0].children[4].role == controlTypes.ROLE_BUTTON:
				fg = api.getForegroundObject()
				fg.children[0].children[1].children[0].children[0].children[1].children[0].children[1].children[0].children[0].children[3].children[0].children[5].children[4].doAction()
				nextHandler()
		except:
			nextHandler()

	def event_valueChange(self, obj, nextHandler):
		pass

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		try:
			if hasattr(obj, "IA2Attributes") and 'message-' in obj.IA2Attributes['class']:
				clsList.insert(0, WhatsAppMessage)
		except:
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
			if focus.IA2Attributes['class'] == '_2_1wd copyable-text selectable-text' and focus.value == '':
				recButton = focus.parent.parent.next.firstChild
				api.moveMouseToNVDAObject(recButton)
				winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
				winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
				winsound.PlaySound("C:\Windows\Media\Windows Pop-up Blocked.wav", winsound.SND_FILENAME)
			elif focus.parent.IA2Attributes['class'] == '_11liR':
				recButton = focus.parent.parent.parent.next.firstChild.firstChild.next.next.next.firstChild
				api.moveMouseToNVDAObject(recButton)
				winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
				winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
				winsound.PlaySound("C:\Windows\Media\Windows Pop-up Blocked.wav", winsound.SND_FILENAME)
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
		if focus.IA2Attributes['class'] == '_2_1wd copyable-text selectable-text':
			toAttachButton = focus.parent.parent.previous.firstChild
			api.moveMouseToNVDAObject(toAttachButton)
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
		else:
			# Translators: Mensaje que anuncia la disponibilidad de ejecución solo desde el cuadro de edición del mensaje
			msg(_('Esta opción solo está disponible desde el cuadro de edición de mensaje'))

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
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Enviar el archivo adjunto'),
		category="WhatsApp",
		gesture="kb:control+s"
	)
	def script_sendAttach(self, gesture):
		focus = api.getFocusObject()
		if focus.firstChild.role == controlTypes.ROLE_BUTTON:
			focus.firstChild.doAction()
			focus.setFocus()

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
		if not hasattr(focus, 'IA2Attributes'): return
		if focus.parent.IA2Attributes['class'] == '_11liR':
			focus.parent.parent.parent.parent.parent.previous.firstChild.firstChild.firstChild.next.next.next.firstChild.doAction()
			# Translators: Verbaliza menú general
			msg(_('Menú general'))

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
			time = str(fc.value).replace(" / ", ", de ")
			# Translators: Se anuncia el tiempo que lleva grabado el mensaje y la duración total del mismo
			msg(_(time))
		elif fc.role == controlTypes.ROLE_BUTTON and fc.next.firstChild.role == controlTypes.ROLE_STATICTEXT:
			# Translators: Se anuncia el tiempo que lleva grabado el mensaje de voz
			msg(_(fc.next.firstChild.name))

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
		category='WhatsApp',
		# Translators: Descripción del elemento en el diálogo de gestos de entrada
		description= _('Activa el botón reenviar'),
		gesture="kb:control+shift+r"
	)
	def script_resend(self, gesture):
		fg = api.getForegroundObject()
		fg.children[0].children[1].children[0].children[0].children[1].children[0].children[1].children[0].children[0].children[3].children[0].children[5].children[4].doAction()

class WhatsAppMessage(Ia2Web):
	def initOverlayClass(self):
		for hs in self.recursiveDescendants:
			try:
				if hs.IA2Attributes['class'] == '_2HtgQ':
					self.bindGesture("kb:enter", "playMessage")
					break
			except KeyError:
				pass

	@script(
		category="WhatsApp",
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Pulsa el botón de reproducción	 en los mensajes de voz'),
	)
	def script_playMessage(self, gesture):
		for f in self.recursiveDescendants:
			try:
				if f.IA2Attributes['class'] == '_2HtgQ':
					f.doAction()
					f.parent.next.children[2].setFocus()
					break
			except KeyError:
				pass
