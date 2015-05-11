# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wx


class PlayerInteraction(object):
    def install(self, controller, pres):
        self.controller = controller
        self.presentation = pres

        pres.Bind(wx.EVT_BUTTON, self.on_button)

    def on_button(self, evt):
        btn = evt.GetEventObject()
        coords = btn.Name.split('_')[-1]

        self.presentation.coords_clicked.append(coords)
        self.presentation.Close()
