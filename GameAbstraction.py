# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from Boats import Carrier, Battleship, Destroyer, PatrolBoat, Submarine, \
    make_fleet
from constants import HIT, MISS, OPEN_WATER


class GameAbstraction(object):
    def __init__(self):
        # boards is addressed via board[col][row]
        COL_COUNT = 9
        ROW_COUNT = 10
        self.boards = [[[OPEN_WATER] * ROW_COUNT for x in xrange(COL_COUNT)],
                       [[OPEN_WATER] * ROW_COUNT for x in xrange(COL_COUNT)]]
        self.fleet = [make_fleet(), make_fleet()]
        self.ship_coords = [[], []]

    def convert_coords(self, coord_pair):
        letter = coord_pair[0].upper()
        if not letter in 'ABCDEFGHI':
            raise Exception("Bad Coordinate Provided: %s" % coord_pair)
        col = int(ord(letter) - ord('A'))
        number = int(coord_pair[1:])
        if number < 1 or number > 10:
            raise Exception("Bad Coordinate Provided: %s" % coord_pair)
        row = number - 1
        return col, row

    def get_contents(self, coord_pair, player):
        col, row = self.convert_coords(coord_pair)
        return self.boards[player][col][row]

    def save_fleet(self, player, fleet):
        used_coords = []
        for boat in self.fleet[player].keys():
            self.fleet[player][boat].coords = fleet[boat].coords
            used_coords.extend(self.fleet[player][boat].coords)
        self.ship_coords[player] = list(set(used_coords))
        self.ship_coords[player].sort()
        fleet_coord_count = len(self.ship_coords[player])
        if not fleet_coord_count == 17:
            msg = "Invalid fleet provided: %s" % str(self.ship_coords[player])
            raise Exception(msg)

    def is_boat_sunk(self, player, boat_name):
        for coord in self.fleet[player][boat_name].coords:
            col, row = self.convert_coords(coord)
            if not self.boards[player][col][row] == HIT:
                return False
        return True

    def record_shot(self, player, coord_pair):
        col, row = self.convert_coords(coord_pair)
        self.boards[player][col][row] = MISS
        if coord_pair.upper() in self.ship_coords[player]:
            self.boards[player][col][row] = HIT
        return self.boards[player][col][row]

    def is_fleet_destroyed(self, player):
        for coord in self.ship_coords[player]:
            col, row = self.convert_coords(coord)
            if not self.boards[player][col][row] == HIT:
                return False
        return True

    # Restricted API that can be passed to the player
    def is_enemy_boat_sunk(self, boat_name):
        return self.is_boat_sunk(1 - self.current_player, boat_name)

    def get_current_contents(self, coord_pair):
        return self.get_contents(coord_pair, self.current_player)

    def get_enemy_contents(self, coord_pair):
        return self.get_contents(coord_pair, 1 - self.current_player)

    def current_board(self, player):
        self.current_player = player
        h = BoardAPI()
        h.get_current_contents = self.get_current_contents
        h.get_enemy_contents = self.get_enemy_contents
        h.is_enemy_boat_sunk = self.is_enemy_boat_sunk
        return h


class BoardAPI(object):
    """ A generic object to house the board API calls """
