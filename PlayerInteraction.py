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
        if btn.Name != 'dialog':
            coords = btn.Name.split('_')[-1]
            self.presentation.coords_clicked.append(coords)
            sort_fn = lambda x: '%s%02d' % (x[0], int(x[1:]))
            self.presentation.coords_clicked = sorted(
                self.presentation.coords_clicked,
                key= sort_fn)

        # We're modal, so use EndModal, not Close.  Ending a modal
        # also happens to fire a command/button event on most
        # platforms, with the dialog itself as the target.  We screen
        # that possibility out above.
        self.presentation.EndModal(0)
