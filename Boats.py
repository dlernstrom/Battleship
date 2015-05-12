# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from Exceptions import MisconfiguredBoatError


class Boat(object):
    """ base class for all boats """
    length = 0
    _coordinates = []
    @property
    def name(self):
        return self.__class__.name

    @property
    def coords(self):
        return self._coordinates

    @coords.setter
    def coords(self, new_coords):
        coords = [x.upper() for x in new_coords]
        coords = list(set(coords))
        coords.sort()
        if not len(coords) == self.__class__.length:
            raise MisconfiguredBoatError("Your boat coords are misconfigured")
        for coord in coords:
            self.validate_coordinate(coord)
        integer_coords = list(set([int(x[1:]) for x in coords]))
        integer_coords.sort()
        letter_coords = list(set([x[0] for x in coords]))
        letter_coords.sort()
        if len(letter_coords) > 1 and len(integer_coords) > 1:
            raise MisconfiguredBoatError("Your boat must be orthogonal")
        if len(letter_coords) == 1:
            # we are going down
            start = integer_coords[0]
            if not integer_coords == range(start, start + self.length):
                raise MisconfiguredBoatError("Your boat is not consecutive")
        else:
            # make sure numbers are the same
            # we are going across
            first = letter_coords[0]
            ideal_ords = range(ord(first), ord(first) + self.length)
            ideal_letters = [chr(x) for x in ideal_ords]
            if not ideal_letters == letter_coords:
                raise MisconfiguredBoatError("Across boat skips letters")
        self._coordinates = coords

    def validate_coordinate(self, coord):
        letter = coord[0]
        if not letter in 'ABCDEFGHI':
            raise MisconfiguredBoatError("Bad Coordinate Provided: %s" % coord)
        col = int(ord(letter) - ord('A'))
        number = int(coord[1:])
        if number < 1 or number > 10:
            raise MisconfiguredBoatError("Bad Coordinate Provided: %s" % coord)


class Carrier(Boat):
    length = 5


class Battleship(Boat):
    length = 4


class Submarine(Boat):
    length = 3


class Destroyer(Boat):
    length = 3


class PatrolBoat(Boat):
    length = 2


def make_fleet():
    return {'Carrier': Carrier(),
            'Battleship': Battleship(),
            'Submarine': Submarine(),
            'Destroyer': Destroyer(),
            'PatrolBoat': PatrolBoat()}
