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
    shots - how many shots have been fired
    tanks - list of other tanks in map
    tank_positions - [(x,y)] other tank positions
    tank_states - list of other tank states (see Tank States)

Functions available to brains:
    memory() - returns [symbol], a read only copy of queued commands
    forget() - clear all queued brain commands
    face(symbol) - change tank facing to symbol UP, DOWN, LEFT, or RIGHT
    forward() - move tank forward one space
    backward() - move tank backward one space
    shoot() - fire tank's weapon with current facing
    radar(x,y) - get a tuple (tile, item) from the map's x,y coordinate
    kill() - self destruct tank

Facings:
    UP, DOWN, LEFT, RIGHT,

Brain Commands:
    FORWARD, BACKWARD, SHOOT

Tank States:
    IDLE, MOVING, TURNING, SHOOTING, DEAD

Tiles:
    GRASS, DIRT, PLAIN, WATER
    SAFE_TILES = (GRASS, DIRT, PLAIN) - can be driven on safely
    UNSAFE_TILES = (WATER,) - will destroy your tank if you drive into them

Items:
    ROCK, TREE - blocking items that can be destroyed
    TANK_BLUE, TANK_RED - tanks located on a tile

Lookup Helper Dictionaries:
    FACING_TO_VEC - takes a facing symbol and returns the (x,y) unit vector

'''

import random

width = 10
height = 8

# 0,0 is upper left

import heapq

import collections

path_step = collections.namedtuple('path_step', ['parent', 'pos'])

def map_path(game, src, dst):
    open_set = set([dst])
    open_heap = [(0, path_step(pos=dst, parent=None))]

    print 'trying to map', src, 'to', dst

    closed_set = set()

    def retrace(current):
        path = [current.pos]
        while current.parent is not None:
            current = current.parent
            path.append(current.pos)
        # path.reverse()
        return path

    while open_set:
        score, current = heapq.heappop(open_heap)
        pos = current.pos
        open_set.remove(pos)

        if pos == src:
            return retrace(current)

        closed_set.add(current)
        for facing in [game.LEFT, game.RIGHT, game.UP, game.DOWN]:
            v = game.FACING_TO_VEC[facing]
            next_step = (pos[0] + v[0], pos[1] + v[1])
            if next_step not in closed_set:
                next_score = score + 1
                tile, item = game.radar(*next_step)
                if tile in game.SAFE_TILES:
                    if next_step not in open_set:
                        open_set.add(next_step)
                        step = path_step(pos=next_step, parent=current)
                        heapq.heappush(open_heap, (next_score, step))

    return None


def think(game):
    #forget() # clear old commands

    x, y = game.position
    dx, dy = game.direction

    # row = [0]*height
    # board = [row[:]]*width
    # for x in range(width):
        # for y in range(height):
            # board[x][y] = game.radar(x, y)
        # print board[x]

    path = map_path(game, (x,y), game.tank_positions[0])

    if len(path) > 1 and not game.memory:
        VEC_TO_FACING = {val: key for key,val in game.FACING_TO_VEC.items()}

        print game.memory
        print [z==game.SHOOT for z in game.memory]
        print [type(z) for z in game.memory]

        first = path[1]
        # print path
        print first, (x,y), (first[0]-x, first[1]-y)
        facing = VEC_TO_FACING[(first[0]-x, first[1]-y)]

        game.face(facing)
        game.forward()
        game.shoot()

    print "brain queue:", game.memory

