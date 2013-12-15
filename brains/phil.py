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
Phil's Brain

See the wander.py file for brain docs (too hard to keep two up to date)
'''


def turn_around(game):
    '''Turn 180 degress around. New by Phil.'''
    if game.facing is game.UP:
        game.face(game.DOWN)
    elif game.facing is game.DOWN:
        game.face(game.UP)
    elif game.facing is game.LEFT:
        game.face(game.RIGHT)
    elif game.facing is game.RIGHT:
        game.face(game.LEFT)


def think(game):

    x, y = game.position
    dx, dy = game.direction

    tile, item = game.radar(x + dx, y + dy)

    print "Tank: ", game.color, " Tile: ", tile, " Item: ", item

    if tile is None or tile is game.WATER or item is not None:
        print game.memory
        turn_around(game)
    else:
        game.forward()
