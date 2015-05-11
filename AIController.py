# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class AIController(object):
    def __init__(self, player):
        self.config = player

    def config_fleet(self, fleet):
        self.config.config_fleet(fleet)
        return fleet

    def get_coords_for_shot(self, current_board_api, fleet):
        return self.config.get_coords_for_shot(current_board_api)

    def notify_shot_outcome(self, result):
        return
