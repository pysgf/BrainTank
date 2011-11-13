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

from utils import Facing

class Brain:
    '''The Brain is your primary interface to write a custom tank AI.'''
    
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    FORWARD = 4
    BACKWARD = 5
    SHOOT = 6
    
    def __init__(self, world, tank):
        self.world = world
        self.tank = tank
        self.tank.brain = self
        
        self.memory = []
        
    def forget(self):
        '''Forget (clear) saved command queue'''
        self.memory = []
        
    def pop(self):
        '''Return and remove the first command in the queue.'''        
        if len(self.memory):        
            return self.memory.pop(0)
        else:
            return None
        
    def face_up(self):
        '''Queue the command to change facing to up.'''
        self.memory.append(self.UP)
        
    def face_down(self):
        '''Queue the command to change facing to down.'''
        self.memory.append(self.DOWN)
        
    def face_left(self):
        '''Queue the command to change facing to the left.'''
        self.memory.append(self.LEFT)
        
    def face_right(self):
        '''Queue the command to change facing to the right.'''
        self.memory.append(self.RIGHT)
        
    def move_forward(self):
        '''Queue the command to move the tank forward.
           The direction depends on the tank's current facing.'''
        self.memory.append(self.FORWARD)
        
    def move_backward(self):
        '''Queue the command to move the tank backward.
           The direction depends on the tank's current facing.'''
        self.memory.append(self.BACKWARD)
        
    def shoot(self):
        '''Queue a shoot command.
           The direction depends on the tank's current facing.'''
        self.memory.append(self.SHOOT)
        
    def position(self):
        '''Return the (x,y) coordinate of the tank.'''
        return self.tank.get_position()
        
    def facing(self):
        '''Return the facing of the tank.
           It returns Facing.UP, Facing.DOWN, etc.'''
        return self.tank.facing.value
        
    def radar(self, x, y):
        '''Return the tile information for a given coordinate.
           Returns (terrain, item). If no terrain or item, it uses None.
           See the World docs for some terrain types.'''
        return self.world.get_tile(x, y)
       
    def kill(self):
        '''Destroys the tank.'''
        self.tank.kill()
        
    def think(self):
        '''Implement this in your custom brain. 
           It is only called if the tank has no commands.'''
        pass
        
        
class DumbBrain(Brain):
    def think(self):
        x,y = self.position()
        self.move_forward()