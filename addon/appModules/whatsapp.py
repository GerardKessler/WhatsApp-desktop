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
import speech
import winsound

class AppModule(appModuleHandler.AppModule):
	disableBrowseModeByDefault=True
	def event_NVDAObject_init(self, obj):
		try:
			if obj.IA2Attributes["class"] == 'dNn0f':
				obj.name = "Mensaje de voz"
			elif obj.IA2Attributes["class"] == 'SncVf _3doiV':
				obj.name = "Reenviar el mensaje"
			elif obj.IA2Attributes["class"] == 'SncVf _3doiV':
				obj.name = "Enviando..."
		except:
			pass

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		try:
			if hasattr(obj, "IA2Attributes") and 'message-' in obj.IA2Attributes['class']:
				clsList.insert(0, WhatsAppMessage)
		except:
			pass

	@script(
	description="Presiona y suelta el botón de grabación",
	category="WhatsApp",
	gesture="kb:control+r")
	def script_record(self, gesture):
		focus = api.getFocusObject()
		focus = focus.parent
		if focus.name == 'Escribe un mensaje aquí':
			recButton = focus.parent.next.firstChild
			api.moveMouseToNVDAObject(recButton)
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
			winsound.PlaySound("C:\Windows\Media\Windows Pop-up Blocked.wav", winsound.SND_FILENAME)
		elif focus.name == 'WhatsApp Web':
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
			winsound.PlaySound("C:\Windows\Media\Windows Information Bar.wav", winsound.SND_FILENAME)
		elif 'Lista de mensajes' in focus.name:
			recButton = focus.parent.parent.next.firstChild.firstChild.next.next.next.firstChild
			api.moveMouseToNVDAObject(recButton)
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
			winsound.PlaySound("C:\Windows\Media\Windows Pop-up Blocked.wav", winsound.SND_FILENAME)

	@script(
		description="Presiona el botón para adjuntar",
		category="WhatsApp",
		gesture="kb:control+shift+a"
	)
	def script_toAttach(self, gesture):
		focus = api.getFocusObject()
		if focus.parent.parent.name == 'Escribe un mensaje aquí':
			toAttachButton = focus.parent.parent.previous.firstChild
			api.moveMouseToNVDAObject(toAttachButton)
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
		else:
			msg("Esta opción solo está disponible desde el cuadro de edición de mensaje")

	@script(
		description="Abre el link del mensaje en el navegador predeterminado del sistema",
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
		description="Copia el texto del mensaje con el foco al portapapeles",
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
				msg("Copiado")
			else:
				message = ". ".join(list[:-1])
				api.copyToClip(message)
				msg("Copiado")
		else:
			msg("Solo disponible desde la lista de mensajes")

	@script(
		description="Enviar el archivo adjunto",
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
		description="Se mueve al mensaje respondido",
		gesture="kb:shift+enter"
	)
	def script_replyMessage(self, gesture):
		focus = api.getFocusObject()
		for fc in focus.recursiveDescendants:
			if getattr(fc, "name") == "Mensaje de voz" and getattr(fc, "role") == controlTypes.ROLE_SECTION:
				fc.parent.previous.previous.doAction()
				msg("Enfocando el mensaje respondido...")
				break

	@script(
		category="WhatsApp",
		description="Activa el botón menú",
		gesture="kb:control+m"
	)
	def script_menuButton(self, gesture):
		focus = api.getFocusObject()
		if 'Lista de mensajes' in focus.parent.name:
			if focus.parent.parent.parent.previous.previous.roleText == 'título región':
				for hs in focus.parent.parent.parent.previous.previous.recursiveDescendants:
					if hs.name == 'Menú' and hs.role == controlTypes.ROLE_BUTTON:
						msg("Menú del mensaje")
						hs.doAction()

	@script(
		category="WhatsApp",
		description="Activa el botón menú general",
		gesture="kb:control+g"
	)
	def script_generalMenuButton(self, gesture):
		fc = api.getFocusObject()
		if fc.parent.name == 'Lista de mensajes. Presiona la tecla de flecha hacia la derecha en un mensaje para abrir su menú contextual.':
			fc.parent.parent.parent.parent.parent.previous.firstChild.firstChild.firstChild.next.next.next.firstChild.doAction()
			msg("Menú general")

	@script(
		category="WhatsApp",
		description="Pulsa en el botón descargar cuando el mensaje contiene un archivo descargable",
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

class WhatsAppMessage(Ia2Web):
	def initOverlayClass(self):
		for hs in self.recursiveDescendants:
			if hs.name == 'Mensaje de voz' and hs.role == controlTypes.ROLE_SECTION:
				self.bindGestures({"kb:enter":"playMessage"})
				break
	@script(
		category="WhatsApp",
		description="Pulsa el botón de reproducción	 en los mensajes de voz",
	)
	def script_playMessage(self, gesture):
		for f in self.recursiveDescendants:
			if getattr(f, "name") == "Mensaje de voz" and getattr(f, "role") == controlTypes.ROLE_SECTION:
				playButton = f.parent.previous.firstChild
				playButton.doAction()
				self.setFocus()
				break

