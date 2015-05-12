# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from itertools import combinations

from Exceptions import UserCancelError, MultipleAiNeededError
from GameAbstraction import GameAbstraction
from GameController import GameController
from Player import AI, Human


class MenuController(object):
    def __init__(self, abstraction, presentation, interaction):
        self.abstraction = abstraction
        self.presentation = presentation
        interaction.install(self, presentation)
        self.presentation.start_sonar()

    def prepare_game(self, ai_player_count):
        self.presentation.Hide()
        try:
            if ai_player_count == 0:
                p1 = Human(self.presentation.get_player_name("Player #1"))
                p2 = Human(self.presentation.get_player_name("Player #2"))
                hotseat = True
            elif ai_player_count == 1:
                p1 = Human(self.presentation.get_player_name("Player #1"))
                p2 = AI(self.presentation.get_ai_file("Player #2"))
                hotseat = False
            else: # ai_player_count == 2:
                p1 = AI(self.presentation.get_ai_file("Player #1"))
                p2 = AI(self.presentation.get_ai_file("Player #2"))
                hotseat = False
        except UserCancelError:
            return
        self.presentation.stop_sonar()
        return_msg = self.run_game([p1, p2], hotseat)
        self.presentation.play_game_over_sound()
        self.presentation.give_message("Game Over", return_msg['msg'])
        self.presentation.Show()
        self.presentation.start_sonar()

    def run_headless_tournament(self):
        try:
            self.presentation.show_progress(self.run_headless_tournament_generator)
        except MultipleAiNeededError, data:
            self.presentation.give_error(unicode(type(data)),
                                         unicode(data))
        except StopIteration:
            return

    def run_headless_tournament_generator(self):
        TARGET_GAME_COUNT = 500
        players = []
        victors_dict = {}
        try:
            paths = self.presentation.get_ai_files()
        except UserCancelError:
            return
        for path in paths:
            try:
                player = AI(path)
            except Exception, data:
                continue
            players.append(path)
            victors_dict[player.name] = 0
        if not len(players) >= 2:
            msg = 'Must have more than one AI player for tournament mode'
            raise MultipleAiNeededError(msg)
        combinations_len = len(list(combinations(players, 2)))
        iteration_count = TARGET_GAME_COUNT / combinations_len
        yield iteration_count * combinations_len
        counter = 0
        for p1, p2 in combinations(players, 2):
            for i in xrange(iteration_count):
                counter += 1
                yield counter
                result = self.run_game([AI(p1), AI(p2)], hotseat=False)
                winner_name = result['winner'].name
                loser_name = result['loser'].name
                msg = '%s beat %s in round %d' % (winner_name, loser_name,
                                                  counter)
                yield (counter, msg)
                victors_dict[winner_name] += 1
        victors_sorted = sorted(victors_dict, key=lambda k: victors_dict[k])
        victors_sorted.reverse()
        self.presentation.stop_sonar()
        self.presentation.play_game_over_sound()
        self.presentation.show_tournament_results(victors_sorted, victors_dict,
                                                  iteration_count)
        self.presentation.start_sonar()

    def run_game(self, player_config, hotseat):
        handle = GameController(self.presentation,
                                GameAbstraction(),
                                player_config,
                                hotseat)
        return handle.play_game()
