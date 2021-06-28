# -*- coding: utf-8 -*-
# Copyright (C) 2021 Gerardo Kessler <ReaperYOtrasYerbas@gmail.com>
# This file is covered by the GNU General Public License.
# Basado en la función focusToSPLWindow del complemento stationPlaylist

import globalPluginHandler
import api
import ui
from scriptHandler import script
from winUser import user32
import addonHandler

# Lína de traducción
addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	@script(
		category="WhatsApp",
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Trae al frente la ventana de whatsapp desde cualquier ubicación')
	)
	def script_focusToWhatsappWindow(self, gesture):
		if api.getForegroundObject().name == 'WhatsApp': return
		WSHwnd = user32.FindWindowW('Chrome_WidgetWin_1', 'WhatsApp')
		if not WSHwnd:
			ui.message("No se encuentra la ventana de WhatsApp")
		else:
			user32.SetForegroundWindow(WSHwnd)
