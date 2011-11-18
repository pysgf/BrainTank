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
    forget() - clear all queued brain commands
    face(symbol) - change tank facing to symbol UP, DOWN, LEFT, or RIGHT
    forward() - move tank forward one space
    backward() - move tank backward one space
    shoot() - fire tank's weapon with current facing
    radar(x,y) - get a tuple (tile, item) from the map's x,y coordinate
    kill() - self destruct tank

Tiles:
    GRASS, DIRT, PLAIN, WATER
    SAFE_TILES = (GRASS, DIRT, PLAIN)
    UNSAFE_TILES = (WATER,)

Items:
    ROCK, TREE
    
'''

import random

def think():
    forget() # clear old commands 
        
    x, y = position
    dx, dy = direction
    
    tile, item = radar(x + dx, y + dy)
    print color, "at", x, y, "and facing", SYMBOL_TO_STR[facing]
    print color, "will be moving into:", tile, item

    def new_facing():
        # out of all facing possibilities, choose one we don't have currently
        new_facing = [UP, DOWN, LEFT, RIGHT]
        new_facing.remove(facing)
        return random.choice(new_facing)
    
    # avoid moving into blocking items
    if item is not None or tile in (WATER, None):
        face(new_facing())
    elif random.randint(0,5) == 0:
        # 1 out of 5 times choose a new direction
        face(new_facing())
    
    forward()
    
    #queue = ', '.join([self.command_to_str[x] for x in self.memory])
    #print color,"brain queue:", queue
