# -*- coding: utf-8 -*-
from __future__ import unicode_literals


OPEN_WATER = 0
MISS = 1
HIT = 2
BATTLESHIP = 'battleship'
CARRIER = 'carrier'
DESTROYER = 'destroyer'
PATROL_BOAT = 'patrolboat'
SUBMARINE = 'submarine'
SHIPS = [BATTLESHIP, CARRIER, DESTROYER, PATROL_BOAT, SUBMARINE]
SHIP_SIZE = {BATTLESHIP: 4,
             CARRIER: 5,
             DESTROYER: 3,
             PATROL_BOAT: 2,
             SUBMARINE: 3}
