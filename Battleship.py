# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wx

from MenuAbstraction import MenuAbstraction
from MenuPresentation import MenuPresentation
from MenuInteraction import MenuInteraction
from MenuController import MenuController


class BattleshipApp(wx.App):
    def OnInit(self):
        abstraction = MenuAbstraction()
        presentation = MenuPresentation()
        interaction = MenuInteraction()
        controller = MenuController(abstraction, presentation, interaction)
        presentation.Show()
        self.SetTopWindow(presentation)
        #import wx.lib.inspection
        #wx.lib.inspection.InspectionTool().Show()
        return True


if __name__ == '__main__':
    app = BattleshipApp(redirect=False)
    app.MainLoop()
