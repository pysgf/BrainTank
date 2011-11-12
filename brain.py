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

class Brain:
    '''The Brain is your primary interface to write an AI'''
    
    def __init__(self, world, tank):
        self.world = world
        self.tank = tank
        self.tank.brain = self
        
    def face_up(self):
        self.tank.facing = Tank.UP
        
    def face_down(self):
        self.tank.facing = Tank.DOWN
        
    def face_left(self):
        self.tank.facing = Tank.LEFT
        
    def face_right(self):
        self.tank.facing = Tank.RIGHT
        
    def move_forward(self):
        self.tank.move = 1
        
    def move_backward(self):
        self.tank.move = -1
        
    def shoot(self):
        self.tank.fire = 1
        
    def position(self):
        return self.tank.get_position()
        
    def radar(self, x, y):
        try:
            return self.world.get_tile(x, y)
        except IndexError:
            return (None, None)
       
    def kill(self):
        self.tank.kill()
        
    def take_turn(self):
        pass
        
class DumbBrain(Brain):
    def take_turn(self):
        x,y = self.position()
        self.move_forward()