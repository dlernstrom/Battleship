# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class BattleshipError(Exception):
    """ Common base class for all Battleship game errors """


class UserCancelError(BattleshipError):
    """ Exception thrown when user cancels out of a prompt """


class MultipleAiNeededError(BattleshipError):
    """ Exception thrown when user tries to play tournament mode with one
    AI player """


class MisconfiguredBoatError(BattleshipError):
    """ Misconfigured Boat"""
