# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from constants import HIT, MISS, OPEN_WATER, CARRIER, SUBMARINE, BATTLESHIP, \
    DESTROYER, PATROL_BOAT


class AIPlayer(object):
    def __init__(self):
        ROWS = 9
        COLS = 10
        self.all_coords = []
        for r in xrange(ROWS):
            for c in xrange(COLS):
                letter = chr(ord('A') + r)
                number = c + 1
                self.all_coords.append('%s%d' % (letter, number))

    def config_fleet(self, fleet):
        fleet[CARRIER].coords = ['A1', 'A2', 'A3', 'A4', 'A5']
        fleet[BATTLESHIP].coords = ['A6', 'A7', 'A8', 'A9']
        fleet[SUBMARINE].coords = ['B1', 'B2', 'B3']
        fleet[DESTROYER].coords = ['B4', 'B5', 'B6']
        fleet[PATROL_BOAT].coords = ['A10', 'B10']
        return fleet

    def get_coords_for_shot(self, api):
        """
        api.is_enemy_boat_sunk(boat_name)
        api.get_current_contents(coord_pair)
        api.get_enemy_contents(coord_pair)
        """

        for coord in self.all_coords:
            if api.get_enemy_contents(coord) == OPEN_WATER:
                return coord
