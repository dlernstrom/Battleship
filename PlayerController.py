# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time


class PlayerController(object):
    def __init__(
            self, abstraction, presentation, interaction, player, hotseat):
        self.abstraction = abstraction
        self.presentation = presentation
        self.config = player
        self.hotseat = hotseat
        interaction.install(self, presentation)

    def config_fleet(self, fleet):
        if self.hotseat:
            self.presentation.notify_turn(self.config.name)
        for key in fleet.keys():
            self.config_ship(key, fleet)
        if not self.hotseat:
            self.presentation.notify_turn(self.config.name)
        return fleet

    def get_coords_for_shot(self, current_board_api, fleet):
        if self.hotseat:
            self.presentation.notify_turn(self.config.name)
        self.presentation.refresh_boards(current_board_api, fleet)
        return self.presentation.get_shot()

    def notify_shot_outcome(self, result):
        self.presentation.give_shot_results(result)

    def config_ship(self, ship_name, fleet):
        coords = []
        desired_size = fleet[ship_name].length
        while len(coords) < desired_size:
            coords = self.presentation.config_ship(ship_name, fleet)
            if len(coords) == desired_size:
                try:
                    fleet[ship_name].coords = coords
                except Exception, data:
                    self.presentation.give_error(data.__class__.__name__,
                                                 str(data))
                    coords = []
                self.presentation.reset_clicked_coords()
