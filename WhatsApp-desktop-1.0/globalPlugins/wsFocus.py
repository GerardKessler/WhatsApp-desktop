# -*- coding: utf-8 -*-
# Copyright (C) 2021 Gerardo Kessler <ReaperYOtrasYerbas@gmail.com>
# This file is covered by the GNU General Public License.
# Clases para abrir la aplicación por Héctor J. Benítez Corredera <xebolax@gmail.com>

import globalPluginHandler
import addonHandler
import gui
import api
import ui
from scriptHandler import script
from winUser import user32
from winsound import PlaySound, SND_FILENAME, SND_ASYNC
import shellapi
import globalVars
import wx
import os
import sys
import subprocess
import ctypes
from threading import Thread

# Lína de traducción
addonHandler.initTranslation()

class disable_file_system_redirection:

	_disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
	_revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection

	def __enter__(self):
		self.old_value = ctypes.c_long()
		self.success = self._disable(ctypes.byref(self.old_value))

	def __exit__(self, type, value, traceback):
		if self.success:
			self._revert(self.old_value)

def obtenApps():
	si = subprocess.STARTUPINFO()
	si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
	try:
		os.environ['PROGRAMFILES(X86)']
		with disable_file_system_redirection():
			p = subprocess.Popen('PowerShell get-StartApps'.split(' '), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='CP437', startupinfo=si, creationflags = 0x08000000, universal_newlines=True)
	except:
		p = subprocess.Popen('PowerShell get-StartApps'.split(' '), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='CP437', startupinfo=si, creationflags = 0x08000000, universal_newlines=True)
	result_string = str(p.communicate()[0])
	lines = [s.strip() for s in result_string.split('\n') if s]
	nuevo = lines[2:]
	lista_final = []
	for x in nuevo:
		y = ' '.join(x.split())
		z = y.rsplit(' ', 1)
		lista_final.append(z)
	return lista_final

def buscarApp(lista, valor):
	tempA = []
	tempB = []
	for i in range(0, len(lista)):
		tempA.append(lista[i][0])
		tempB.append(lista[i][1])
	filtro = [item for item in tempA if valor.lower() in item.lower()]
	return tempA, tempB, filtro

IS_WinON = False

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()
		if globalVars.appArgs.secure: return

	def terminate(self):
		try:
			if not self._MainWindows:
				self._MainWindows.Destroy()
		except (AttributeError, RuntimeError):
			pass

	@script(
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Abre WhatsApp, o la enfoca si ya se encuentra abierta'),
		category="WhatsApp")
	def script_open(self, gesture):
		_MainWindows = HiloComplemento()
		_MainWindows.start()

	@script(
		category="WhatsApp",
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Trae al frente la ventana de whatsapp desde cualquier ubicación')
	)
	def script_focusToWhatsappWindow(self, gesture):
		if api.getForegroundObject().name == 'WhatsApp': return
		WSHwnd = user32.FindWindowW('Chrome_WidgetWin_1', 'WhatsApp')
		if not WSHwnd:
			# Translators: Mensaje que anuncia que la ventana de WhatsApp no ha sido encontrada.
			ui.message(_('No se encuentra la ventana de WhatsApp'))
		else:
			user32.SetForegroundWindow(WSHwnd)

class ViewApps(wx.Dialog):
	def __init__(self, parent, nombre, id, resultados):
		# Translators: Título de la ventana
		super(ViewApps, self).__init__(parent, -1, title=_('Selector de aplicación'), size=(350, 150))
		global IS_WinON
		IS_WinON = True
		self.choiceSelection = 0
		self.nombre = nombre
		self.id = id
		self.resultados = resultados
		self.Panel = wx.Panel(self)
		self.choice = wx.Choice(self.Panel, wx.ID_ANY, choices =["Seleccione una aplicación de WhatsApp"] + self.resultados)
		self.choice.SetSelection(self.choiceSelection)
		self.choice.Bind(wx.EVT_CHOICE, self.onChoiceApp)
		#Translators: etiqueta del botón aceptar
		self.aceptar = wx.Button(self.Panel, wx.ID_ANY, _('Lanzar &aplicación'))
		self.aceptar.Bind(wx.EVT_BUTTON, self.onAceptar)
		#Translators: etiqueta del botón cancelar
		self.closeButton = wx.Button(self.Panel, wx.ID_CANCEL, _('&Cerrar'))
		self.closeButton.Bind(wx.EVT_BUTTON, self.close, id=wx.ID_CANCEL)

		sizerV = wx.BoxSizer(wx.VERTICAL)
		sizerH = wx.BoxSizer(wx.HORIZONTAL)

		sizerV.Add(self.choice, 0, wx.EXPAND | wx.ALL)

		sizerH.Add(self.aceptar, 2, wx.CENTER)
		sizerH.Add(self.closeButton, 2, wx.CENTER)

		sizerV.Add(sizerH, 0, wx.CENTER)

		self.Panel.SetSizer(sizerV)

		self.CenterOnScreen()

	def onChoiceApp(self, event):
		#Translators: título de selección de aplicación
		if self.choice.GetString(self.choice.GetSelection()) == _('Seleccione una de las aplicaciones de WhatsApp'):
			self.choiceSelection = 0
		else:
			self.choiceSelection = event.GetSelection()

	def onAceptar(self, event):
		if self.choiceSelection == 0:
			gui.messageBox(_('Debe seleccionar una aplicación para continuar.'), _("Información"), wx.ICON_INFORMATION)
			self.choice.SetFocus()
		else:
			global IS_WinON
			IS_WinON = False
			shellapi.ShellExecute(None, 'open', "explorer.exe", "shell:appsfolder\{}".format(self.id[self.nombre.index(self.resultados[self.choiceSelection - 1])]), None, 10)
			self.Destroy()
			gui.mainFrame.postPopup()

	def close(self, event):
		global IS_WinON
		IS_WinON = False
		self.Destroy()
		gui.mainFrame.postPopup()

class HiloComplemento(Thread):
	def __init__(self):
		super(HiloComplemento, self).__init__()
		PlaySound('C:\\Windows\\Media\\Windows Proximity Connection.wav', SND_FILENAME | SND_ASYNC)

		self.daemon = True

	def run(self):
		def runApp():
			nombre, id, resultados = buscarApp(obtenApps(), "WhatsApp")
			if len(resultados) == 1:
				shellapi.ShellExecute(None, 'open', "explorer.exe", "shell:appsfolder\{}".format(id[nombre.index(resultados[0])]), None, 10)
			elif len(resultados) >= 2:
				if IS_WinON == False:
					self._MainWindows = ViewApps(gui.mainFrame, nombre, id, resultados)
					gui.mainFrame.prePopup()
					self._MainWindows.Show()
			else:
				ui.message(_('No se ha encontrado la aplicación de WhatsApp'))

		wx.CallAfter(runApp)
