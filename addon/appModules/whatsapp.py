# -*- coding: utf-8 -*-
# Copyright (C) 2021 Gerardo Kessler <ReaperYOtrasYerbas@gmail.com>
# This file is covered by the GNU General Public License.

import appModuleHandler
from scriptHandler import script
import api
import winUser
import controlTypes
from ui import message
from re import search, sub
from tones import beep
from threading import Thread
from time import sleep
import speech
import config
import addonHandler

# Lína de traducción
addonHandler.initTranslation()

getRole = lambda attr: getattr(controlTypes, f'ROLE_{attr}') if hasattr(controlTypes, 'ROLE_BUTTON') else getattr(controlTypes.Role, attr)

def initConfiguration():
	confspec = {
		'isUpgrade': 'boolean(default=False)',
		'RemovePhoneNumberInMessages': 'boolean(default=False)'
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

def speak(msg, time, str= False):
	if msg:
		message(msg)
		sleep(0.1)
	Thread(target=killSpeak, args=(time,), daemon= True).start()

def killSpeak(time):
	if speech.getState().speechMode == speech.SpeechMode.off: return
	speech.setSpeechMode(speech.SpeechMode.off)
	sleep(time)
	speech.setSpeechMode(speech.SpeechMode.talk)

class AppModule(appModuleHandler.AppModule):

	disableBrowseModeByDefault=True

	def __init__(self, *args, **kwargs):
		super(AppModule, self).__init__(*args, **kwargs)
		self.messageObj = None
		self.messagesList = None
		self.editableText = None
		self.temp_value = getConfig('RemovePhoneNumberInMessages')
		self.x = None
		self.control= None

	def event_NVDAObject_init(self, obj):
		try:
			if self.control:
				self.control.setFocus()
				self.control= None
		except:
			self.control= None
		try:
			if 'fd365im1' in obj.IA2Attributes['class']:
				self.messagesList= obj.parent.parent.parent.parent.parent.previous.lastChild.lastChild
				self.editableText= obj
			elif "focusable-list-item" in obj.IA2Attributes['class']:
				self.messageObj = obj
		except:
			pass
		try:
			if not self.temp_value: return
			if 'focusable-list-item' in obj.IA2Attributes['class']:
				obj.name = sub(r'\+\d[()\d\s‬-]{12,}', '', obj.name)
		except:
			pass

	@script(
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Presiona y suelta el botón de grabación'),
		category='WhatsApp',
		gesture="kb:control+r"
	)
	def script_record(self, gesture):
		focus = api.getFocusObject()
		fg = api.getForegroundObject()
		try:
			if 'p357zi0d' in focus.IA2Attributes['class']:
				speak(focus.parent.lastChild.name, 0.5, self.messagesList.lastChild.name)
				focus.parent.lastChild.doAction()
				self.control= self.messagesList.lastChild.lastChild
				return
			elif 'fd365im1' in focus.IA2Attributes['class']:
				recordBtn= focus.simpleNext.simpleNext
			elif 'focusable-list-item' in focus.IA2Attributes['class']:
				recordBtn= focus.simpleParent.simpleParent.simpleNext.simpleLastChild
			if recordBtn:
				speak(recordBtn.name, 0.5)
				api.moveMouseToNVDAObject(recordBtn)
				winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
				winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
		except:
			pass

	@script(
		# Translators: Descripción del elemento en el diálogo de gestos de entrada
		description= _('Copia el texto del mensaje con el foco al portapapeles'),
		category='WhatsApp',
		gesture="kb:control+shift+c"
	)
	def script_textCopy(self, gesture):
		messagesObj= False
		messagesContent = ""
		focus = api.getFocusObject()
		for obj in focus.recursiveDescendants:
			try:
				if 'copyable-text' in obj.IA2Attributes['class']:
					messagesObj = obj
					break
			except:
				pass
		if messagesObj:
			for msg in messagesObj.children:
				if msg.name != None:
					messagesContent += ' {}'.format(msg.name)
			api.copyToClip(messagesContent)
			beep(440, 5)

	@script(gesture="kb:alt+r")
	def script_response(self, gesture):
		if api.getFocusObject().role != getRole('SECTION'): return
		messagesObj = False
		messagesContent = ""
		for obj in api.getFocusObject().recursiveDescendants:
			try:
				if obj.IA2Attributes['class'] == '_1Gy50':
					messagesObj = obj
					break
			except:
				pass
		if messagesObj:
			for msg in messagesObj.children:
				if msg.name != None:
					messagesContent += ' {}'.format(msg.name)
			message(messagesContent)

	@script(
		category='WhatsApp',
		# Translators: Descripción del elemento en el diálogo de gestos de entrada
		description= _('Verbaliza el tiempo  del mensaje en reproducción, o la duración del mensaje en grabación'),
		gesture='kb:control+t'
	)
	def script_timeAnnounce(self, gesture):
		fc = api.getFocusObject()
		try:
			if fc.role == getRole('SLIDER'):
				# Translators: Artículo que divide entre el tiempo actual y la duración total del mensaje.
				time = fc.value.replace("/", _(' de '))
				message(time)
			elif fc.role == getRole('BUTTON') and fc.next.firstChild.firstChild.firstChild.role == getRole('STATICTEXT'):
				message(fc.next.children[0].children[0].children[0].name)
			elif fc.parent.IA2Attributes['class'] == 'h4Qs-':
				str = fc.parent.children[1].children[1].children[0].children[0].name
				message(str)
		except:
			pass

	@script(
		# Translators: Descripción del elemento en el diálogo de gestos de entrada
		description= _('Anuncia el nombre del chat'),
		category='WhatsApp',
		gesture='kb:control+shift+t'
	)
	def script_chatAnnounce(self, gesture):
		fg = api.getForegroundObject()
		try:
			message(fg.children[0].children[1].children[0].children[0].children[1].children[0].children[1].children[0].children[0].children[3].children[0].children[1].children[1].children[0].children[0].children[0].name)
		except:
			pass

	@script(
		category='WhatsApp',
		# Translators: Descripción del elemento en el diálogo de gestos de entrada
		description= _('reproduce los videos adjuntados como tal'),
		gesture="kb:control+shift+v"
	)
	def script_playVideo(self, gesture):
		fc = api.getFocusObject()
		try:
			for child in fc.recursiveDescendants:
				if child.role == getRole('STATICTEXT') and child.IA2Attributes['display'] == "block" and child.previous.role == getRole('GRAPHIC'):
					child.doAction()
					# Translators: anuncia que el video se está cargando
					speak(_('el video se está cargando...'), 0.2)
					break
		except:
			pass

	@script(gesture="kb:alt+rightArrow")
	def script_lastMessageObj(self, gesture):
		if self.messageObj == None: return
		self.messageObj.setFocus()

	@script(
		category='WhatsApp',
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Conmuta entre la lista de mensajes y el cuadro de edición'),
		gesture="kb:alt+leftArrow"
	)
	def script_messages_edit(self, gesture):
		try:
			focus = api.getFocusObject()
			if 'fd365im1' in focus.IA2Attributes['class']:
				self.messagesList.lastChild.lastChild.setFocus()
			elif "focusable-list-item" in focus.IA2Attributes['class']:
				self.editableText.setFocus()
		except:
			pass

	@script(gesture="kb:alt+downArrow")
	def script_readMore(self, gesture):
		focus = api.getFocusObject()
		if focus.role != getRole('SECTION'): return
		for obj in focus.recursiveDescendants:
			try:
				if obj.IA2Attributes['class'] == 'o0rubyzf le5p0ye3 ajgl1lbb read-more-button':
					message(obj.name)
					obj.doAction()
					focus.setFocus()
					break
			except:
				pass

	@script(
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		category= 'WhatsApp',
		description= _('Activa y desactiva la eliminación de los números de teléfono de los contactos no agendados en los mensajes'),
		gesture="kb:control+shift+r"
	)
	def script_viewConfigToggle(self, gesture):
		if self.temp_value:
			setConfig('RemovePhoneNumberInMessages', False)
			self.temp_value = False
			# Translators: Mensaje que indica la desactivación de los mensajes editados
			message(_('Mensajes editados, desactivado'))
		else:
			setConfig('RemovePhoneNumberInMessages', True)
			self.temp_value = True
			# Translators: Mensaje que anuncia la activación de los mensajes editados
			message(_('Mensajes editados, activado'))

	@script(gestures=[f'kb:alt+{i}' for i in range(1,10)])
	def script_messageHistory(self, gesture):
		self.x = int(gesture.displayName[-1])*-1
		if not self.messagesList: return
		try:
			message(self.messagesList.children[self.x].lastChild.name)
		except:
			gesture.send()

	@script(gesture="kb:alt+enter")
	def script_messageFocus(self, gesture):
		try:
			self.messagesList.children[self.x].lastChild.setFocus()
		except:
			gesture.send()
