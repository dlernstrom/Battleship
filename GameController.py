# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from random import randint

from AIController import AIController
from Boats import make_fleet
from constants import HIT
from PlayerAbstraction import PlayerAbstraction
from PlayerController import PlayerController
from PlayerInteraction import PlayerInteraction
from PlayerPresentation import PlayerPresentation
from Player import AI


class GameController(object):
    def __init__(self, parent, abstraction, player_config, hotseat):
        self.abstraction = abstraction
        self.players = []
        for config in player_config:
            if isinstance(config, AI):
                self.players.append(AIController(config))
            else:
                controller = PlayerController(PlayerAbstraction(),
                                              PlayerPresentation(parent),
                                              PlayerInteraction(),
                                              config,
                                              hotseat)
                self.players.append(controller)

    def play_game(self):
        self.switch_players(True)
        # Configure Fleet
        ## First Player
        ret_val = self.configure_fleet()
        if ret_val:
            return ret_val
        self.switch_players()
        ## Second Player
        ret_val = self.configure_fleet()
        if ret_val:
            return ret_val
        self.switch_players()
        ## "Playing game"
        while True:
            p = self.players[self.current]
            current_board_api = self.abstraction.current_board(self.current)
            fleet = self.abstraction.fleet[self.current]
            try:
                coords = p.get_coords_for_shot(current_board_api, fleet)
            except IndexError:
                RETIRE_MSG = "%s won because %s retired!"
                winner = self.players[self.enemy].config
                loser = self.players[self.current].config
                return {'winner': winner,
                        'msg': RETIRE_MSG % (winner.name, loser.name)}
            result = self.abstraction.record_shot(self.enemy, coords)
            p.notify_shot_outcome(result)
            if self.abstraction.is_fleet_destroyed(self.enemy):
                winner = self.players[self.current].config
                loser = self.players[self.enemy].config
                MSG = "%s won because %s's ships were destroyed"
                return {'winner': winner,
                        'msg': MSG % (winner.name, loser.name)}
            if not result == HIT:
                self.switch_players()

    def switch_players(self, seed=False):
        if seed:
            self.current = randint(0, 1)
        self.current = 1 - self.current
        self.enemy = 1 - self.current

    def configure_fleet(self):
        FLEET_MSG = "%s won because %s couldn't configure their fleet!"
        try:
            fleet = self.players[self.current].config_fleet(make_fleet())
            self.abstraction.save_fleet(self.current, fleet)
        except Exception, data:
            winner = self.players[self.enemy].config
            loser = self.players[self.current].config
            return {'winner': winner,
                    'msg': FLEET_MSG % (winner.name, loser.name)}

