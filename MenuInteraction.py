# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wx


class MenuInteraction(object):
    def install(self, controller, pres):
        self.controller = controller

        pres.Bind(wx.EVT_BUTTON, self.on_pvp, pres.btn_pvp)
        pres.Bind(wx.EVT_BUTTON, self.on_pvc, pres.btn_pvc)
        pres.Bind(wx.EVT_BUTTON, self.on_cvc, pres.btn_cvc)
        pres.Bind(wx.EVT_BUTTON, self.on_tournament, pres.btn_tournament)

    def on_pvp(self, evt):
        self.controller.prepare_game(ai_player_count=0)

    def on_pvc(self, evt):
        self.controller.prepare_game(ai_player_count=1)

    def on_cvc(self, evt):
        self.controller.prepare_game(ai_player_count=2)

    def on_tournament(self, evt):
        self.controller.run_headless_tournament()
