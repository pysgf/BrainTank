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

from utils import Enum


Command = Enum('FORWARD', 'BACKWARD', 'SHOOT')

Facing = Enum('UP', 'DOWN', 'LEFT', 'RIGHT')

TankState = Enum('IDLE', 'MOVING', 'TURNING', 'SHOOTING', 'DEAD')

# make sure Tiles and Items match what world contains!

Tile = Enum('GRASS', 'DIRT', 'WATER', 'PLAIN')

Item = Enum('TREE', 'ROCK', 'TANK_RED', 'TANK_BLUE')


FACING_TO_VEC = {
    Facing.UP:    ( 0,-1),
    Facing.DOWN:  ( 0, 1),
    Facing.LEFT:  (-1, 0),
    Facing.RIGHT: ( 1, 0)
}
