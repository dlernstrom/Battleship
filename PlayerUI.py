# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wx

from MenuPresentation import MenuPresentation


class BattleshipApp(wx.App):
    def OnInit(self):
        presentation = MenuPresentation()
        presentation.Show()
        self.SetTopWindow(presentation)
        return True


if __name__ == '__main__':
    app = BattleshipApp(redirect=False)
    app.MainLoop()
