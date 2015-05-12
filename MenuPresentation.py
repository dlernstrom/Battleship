# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from types import TupleType

import wx
from wx.lib.dialogs import ScrolledMessageDialog

from Exceptions import UserCancelError, MultipleAiNeededError

PY_WILDCARD = "Python source (*.py)|*.py"


class MenuPresentation(wx.Dialog):
    def __init__(self):
        title = 'Battleship!'
        super(MenuPresentation, self).__init__(None, -1, title)
        outer_sizer = wx.BoxSizer(wx.HORIZONTAL)

        path = os.path.join(
            os.path.dirname(__file__), 'images', 'battleship.jpg')
        i = wx.Image(path , wx.BITMAP_TYPE_JPEG)
        img = wx.StaticBitmap(self, -1, i.ConvertToBitmap(),
                              size=(i.GetWidth(), i.GetHeight()))
        outer_sizer.Add(img, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        BTN_SIZE = (-1, 50)
        BTN_STYLE = wx.EXPAND | wx.ALL
        btn_sizer = wx.BoxSizer(wx.VERTICAL)
        self.btn_pvp = wx.Button(self, -1, "Player vs. Player", size=BTN_SIZE)
        btn_sizer.Add(self.btn_pvp, 0, BTN_STYLE, 5)
        self.btn_pvc = wx.Button(
            self, -1, "Player vs. Computer", size=BTN_SIZE)
        btn_sizer.Add(self.btn_pvc, 0, BTN_STYLE, 5)
        self.btn_cvc = wx.Button(
            self, -1, "Computer vs. Computer", size=BTN_SIZE)
        btn_sizer.Add(self.btn_cvc, 0, BTN_STYLE, 5)
        self.btn_tournament = wx.Button(
            self, -1, "Tournament Style", size=BTN_SIZE)
        btn_sizer.Add(self.btn_tournament, 0, BTN_STYLE, 5)
        outer_sizer.Add(btn_sizer, 0, wx.ALL, 5)
        outer_sizer.SetSizeHints(self)
        self.SetSizer(outer_sizer)

        self.Bind(wx.EVT_CLOSE, self.on_close)

    def start_sonar(self):
        self.sound = wx.Sound(os.path.join(os.path.dirname(__file__),
                                           'audio', 'sonar.wav'))
        self.sound.Play(wx.SOUND_ASYNC | wx.SOUND_LOOP)

    def stop_sonar(self):
        self.sound.Stop()

    def on_close(self, evt):
        self.stop_sonar()
        self.Destroy()

    def get_player_name(self, role):
        dlg = wx.TextEntryDialog(
            self, "Please enter %s's name" % role, "Name Please", role)
        if dlg.ShowModal() == wx.ID_OK:
            val = dlg.GetValue()
            dlg.Destroy()
            return val
        dlg.Destroy()
        raise UserCancelError("User Cancelled Selection")

    def get_ai_file(self, role):
        dlg = wx.FileDialog(
            self, message="Choose an AI file for %s" % role,
            defaultDir=os.path.join(os.path.dirname(__file__),
                                    'MyAI'),
            defaultFile="",
            wildcard=PY_WILDCARD,
            style=wx.OPEN | wx.CHANGE_DIR
        )
        if dlg.ShowModal() == wx.ID_OK:
            return dlg.GetPath()
        raise UserCancelError("User Cancelled Selection")

    def give_message(self, title, msg, iconStyle=wx.ICON_INFORMATION):
        dlg = wx.MessageDialog(self, msg, title,
                               wx.OK | wx.STAY_ON_TOP | iconStyle)
        dlg.ShowModal()
        dlg.Destroy()

    def give_error(self, title, msg):
        self.give_message(title, msg, wx.ICON_HAND)

    def give_scrolled_message(self, title, msg):
        dlg = ScrolledMessageDialog(
            self, msg, title, size=(1000, 600),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        points = dlg.text.GetFont().GetPointSize()  # get the current size
        f = wx.Font(points, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL,
                    wx.FONTWEIGHT_NORMAL)
        dlg.text.SetFont(f)
        dlg.ShowModal()
        dlg.Destroy()

    def get_ai_files(self):
        dlg = wx.FileDialog(
            self, message="Choose AI files",
            defaultDir=os.path.join(os.path.dirname(__file__),
                                    'MyAI'),
            defaultFile="",
            wildcard=PY_WILDCARD,
            style=wx.OPEN | wx.CHANGE_DIR | wx.MULTIPLE
        )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            if len(paths) < 2:
                raise MultipleAiNeededError("Must select more than 1 AI file")
            return paths
        raise UserCancelError("User Cancelled Selection")

    def show_tournament_results(self, victors_sorted, victors_dict,
                                iteration_count):
        title = "Contest Results"
        msg = ['Each combination of players played %d times' % iteration_count,
               'Below are the results of the contest:\n']
        contestant_count = len(victors_sorted)
        for counter in xrange(contestant_count):
            victor_name = victors_sorted[counter]
            params = (str(counter + 1).ljust(4),
                      str(victor_name).ljust(40),
                      str(victors_dict[victor_name]).rjust(10))
            msg.append('RANK #%s%s%s' % params)
        self.give_scrolled_message(title, '\n'.join(msg))

    def play_game_over_sound(self):
        sound = wx.Sound(os.path.join(os.path.dirname(__file__),
                                      'audio', 'win.wav'))
        sound.Play(wx.SOUND_ASYNC)

    def show_progress(self, generator):
        gen = generator()
        total = gen.next()
        dlg = wx.ProgressDialog(title="Bleh", message="Running...",
                                maximum=total, parent=self,
                                style=wx.PD_AUTO_HIDE | wx.PD_APP_MODAL | \
                                wx.PD_ELAPSED_TIME | wx.PD_ESTIMATED_TIME | \
                                wx.PD_REMAINING_TIME)
        for x in gen:
            if type(x) == TupleType:
                dlg.Update(x[0], x[1])
            else:
                dlg.Update(x)#, "Running..")
        dlg.Destroy()
