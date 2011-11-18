#!/usr/bin/python
# -*- coding: utf-8 -*-

###############################################################################
# Python AI Battle
#
# Copyright 2011 Matthew Thompson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################

'''
Wander Brain

This is a sample wandering brain. It just drives until it
hits an obstacle then chooses a new direction. It also changes
direction periodically.

Variables available to brains:
    color - string, tank color
    position - tuple (x,y), current tank grid position
    facing - symbol UP, DOWN, LEFT, RIGHT, current tank facing
    direction - tuple (x,y), unit vector representing tank facing

Functions available to brains:
    memory() - returns [symbol], a read only copy of queued commands
    forget() - clear all queued brain commands
    face(symbol) - change tank facing to symbol UP, DOWN, LEFT, or RIGHT
    forward() - move tank forward one space
    backward() - move tank backward one space
    shoot() - fire tank's weapon with current facing
    radar(x,y) - get a tuple (tile, item) from the map's x,y coordinate
    kill() - self destruct tank

Symbols:
    UP, DOWN, LEFT, RIGHT, FORWARD, BACKWARD, SHOOT
    
Tiles:
    GRASS, DIRT, PLAIN, WATER
    SAFE_TILES = (GRASS, DIRT, PLAIN)
    UNSAFE_TILES = (WATER,)

Items:
    ROCK, TREE
    
Lookup Helper Dictionaries:
    SYMBOL_TO_STR - takes a symbol and returns a string
    FACING_TO_VEC - takes a facing symbol and returns the (x,y) unit vector
    
'''

import random

def think():
    #forget() # clear old commands 
        
    x, y = position
    dx, dy = direction
    
    tile, item = radar(x + dx, y + dy)
    print color, "at", x, y, "and facing", SYMBOL_TO_STR[facing]
    print color, "will be moving into:", tile, item

    def new_facing():
        # out of all facing possibilities, choose one we don't have currently
        new_facing = [UP, DOWN, LEFT, RIGHT]
        new_facing.remove(facing)
        
        # evaluate the possible facings and remove ones that will block tank
        good_facing = []
        for f in new_facing:
            v = FACING_TO_VEC[f]
            nt, ni = radar(x + v[0], y + v[1])
            if ni is None and nt not in (None, WATER):
                good_facing.append(f)
                
        return random.choice(good_facing or new_facing)
    
    # avoid moving into blocking items
    if item is not None or tile in (WATER, None):
        forget() # clear possibly bad commands
        face(new_facing())
    elif random.randint(0,5) == 0:
        # 1 out of 5 times choose a new direction
        face(new_facing())
    
    if FORWARD not in memory():
        forward()
    
    if random.randint(0,3) == 0:
        # 1 out of 3 times try to shoot
        shoot()
    
    queue = ', '.join([SYMBOL_TO_STR[x] for x in memory()])
    print color,"brain queue:", queue
