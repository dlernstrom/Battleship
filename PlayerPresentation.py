# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import time

import wx

from constants import HIT, MISS, OPEN_WATER, SHIPS, SHIP_SIZE

ENEMY_PREFIX = 'btn_enemy_%s'
US_PREFIX = 'btn_us_%s'


def make_bmp(name):
    path = os.path.join(os.path.dirname(__file__), 'images', name)
    return wx.Bitmap(path, wx.BITMAP_TYPE_BMP)


class PlayerPresentation(wx.Dialog):
    def __init__(self, parent):
        title = 'Battleship!'
        super(PlayerPresentation, self).__init__(parent, -1, title)
        self.parent = parent
        self.make_bitmaps()
        self.coords_clicked = []
        self.gbs = wx.GridBagSizer(0, 0)

        self.instruction_static = wx.StaticText(self, wx.ID_ANY, '')
        self.gbs.Add(self.instruction_static, (0, 1), flag=wx.ALL, border=5)

        self.gbs.Add(self.make_board('Enemy', ENEMY_PREFIX), (1, 1))

        self.gbs.Add(self.make_board('Us', US_PREFIX), (3, 1))
        self.gbs.SetSizeHints(self)
        self.SetSizer(self.gbs)

    def notify_turn(self, name):
        self.give_message("%s's turn" % name, "%s, you're up!" % name)

    @property
    def instruction(self):
        return self.instruction_static.GetLabel()

    @instruction.setter
    def instruction(self, msg):
        self.instruction_static.SetLabel(msg)

    def coord_generator(self):
        for row in xrange(9):
            for col in xrange(10):
                coord = '%s%s' % (chr(ord('A') + row), col + 1)
                yield coord, row, col

    def make_board(self, name, prefix):
        gbs = wx.GridBagSizer(0, 0)
        for coord, row, col in self.coord_generator():
            btn_name = prefix % coord

            bmp = self.bmps['water']
            btn = wx.BitmapButton(self, wx.ID_ANY, bmp,
                                  (bmp.GetWidth(), bmp.GetHeight()),
                                  style=wx.NO_BORDER)
            btn.Name = btn_name
            setattr(self, btn_name, btn)
            gbs.Add(btn, (row, col))
        box = wx.StaticBox(self, wx.ID_ANY, name)
        sz = wx.StaticBoxSizer(box, wx.VERTICAL)
        sz.Add(gbs)
        return sz

    def redraw_ocean(self, prefix):
        for coord, col, row in self.coord_generator():
            self.draw_cell(prefix, coord, 'water')

    def draw_cell(self, prefix, coord, img_name):
        btn_name = prefix % coord
        btn = getattr(self, btn_name)
        btn.SetBitmapLabel(self.bmps[img_name])

    def draw_ship_cell(self, btn_prefix, coord, ship, direction, pos, hit_sfx=''):
        prefix = '%s_%s_%s%s'
        params = (ship, direction, pos + 1, hit_sfx)
        name = prefix % params
        self.draw_cell(btn_prefix, coord, name)

    def make_bitmaps(self):
        self.bmps = {'water': make_bmp('water.bmp'),
                     'water_miss': make_bmp('water_miss.bmp'),
                     'water_hit': make_bmp('water_hit.bmp')}
        prefix = '%s_%s_%s%s'
        for ship in SHIPS:
            for direction in ['h', 'v']:
                for hit_sfx in ['_hit', '']:
                    for position in xrange(SHIP_SIZE[ship]):
                        params = (ship, direction, position + 1, hit_sfx)
                        name = prefix % params
                        self.bmps[name] = make_bmp(name + '.bmp')

    def ship_direction(self, coords):
        if not coords:
            return 'h'
        if coords[0][0] == coords[-1][0]:
            return 'h'
        return 'v'

    def update_fleet_images(self, fleet):
        for ship_name in fleet.keys():
            ship = ship_name.lower()
            coords = fleet[ship_name].coords
            direction = self.ship_direction(coords)
            for coord in coords:
                index = coords.index(coord)
                self.draw_ship_cell(US_PREFIX, coord, ship, direction, index)

    def config_ship(self, ship_name, fleet):
        self.start_sonar()
        length = fleet[ship_name].length
        msg = "Please Click On %d Cells for %s" % (length, ship_name)
        self.instruction = msg
        self.redraw_ocean(US_PREFIX)
        self.update_fleet_images(fleet)
        for coord in self.coords_clicked:
            direction = self.ship_direction(self.coords_clicked)
            index = self.coords_clicked.index(coord)
            self.draw_ship_cell(US_PREFIX, coord, ship_name.lower(),
                                direction, index)
        self.ShowModal()
        self.stop_sonar()
        return self.coords_clicked

    def reset_clicked_coords(self):
        self.coords_clicked = []

    def give_message(self, title, msg, iconStyle=wx.ICON_INFORMATION):
        dlg = wx.MessageDialog(self, msg, title,
                               wx.OK | wx.STAY_ON_TOP | iconStyle)
        dlg.ShowModal()
        dlg.Destroy()

    def give_error(self, title, msg):
        self.give_message(title, msg, wx.ICON_HAND)

    def refresh_boards(self, api, fleet):
        self.redraw_ocean(US_PREFIX)
        self.redraw_ocean(ENEMY_PREFIX)
        for coord, col, row in self.coord_generator():
            ## Draw our ships
            cell = api.get_current_contents(coord)
            if cell == MISS:
                self.draw_cell(US_PREFIX, coord, 'water_miss')
            else:
                prefix = self.get_fleet_ship_at_coords(fleet, coord)
                suffix = ''
                if cell == HIT:
                    suffix = '_hit'
                if prefix == 'water':
                    self.draw_cell(US_PREFIX, coord, prefix + suffix)
                else:
                    ship = prefix
                    coords = fleet[ship].coords
                    direction = self.ship_direction(coords)
                    index = coords.index(coord)
                    self.draw_ship_cell(US_PREFIX, coord, ship.lower(),
                                        direction, index, suffix)
            ## Draw their ships
            cell = api.get_enemy_contents(coord)
            if cell == MISS:
                self.draw_cell(ENEMY_PREFIX, coord, 'water_miss')
            elif cell == HIT:
                self.draw_cell(ENEMY_PREFIX, coord, 'water_hit')

    def get_fleet_ship_at_coords(self, fleet, coords):
        for name in fleet.keys():
            if coords in fleet[name].coords:
                return name
        return 'water'

    def get_shot(self):
        self.start_sonar()
        self.reset_clicked_coords()
        msg = "Please Take a shot"
        self.instruction = msg
        self.ShowModal()
        self.stop_sonar()
        return self.coords_clicked[0]

    def give_shot_results(self, result):
        self.Show()
        if result == HIT:
            msg = "HIT!!! Please go again!"
            sound_file = 'hit.wav'
        else:
            msg = "MISS"
            sound_file = 'miss.wav'
        sound = wx.Sound(os.path.join(os.path.dirname(__file__),
                                      'audio', sound_file))
        sound.Play(wx.SOUND_SYNC)
        busy = wx.BusyInfo(msg)
        time.sleep(1)
        self.Hide()

    def start_sonar(self):
        self.sound = wx.Sound(os.path.join(os.path.dirname(__file__),
                                           'audio', 'sonar.wav'))
        self.sound.Play(wx.SOUND_ASYNC | wx.SOUND_LOOP)

    def stop_sonar(self):
        self.sound.Stop()
