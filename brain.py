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

import sys
from utils import Facing

class Brain:
    '''The Brain is your primary interface to write a custom tank AI.'''
    
    UP = Facing.UP
    DOWN = Facing.DOWN
    LEFT = Facing.LEFT
    RIGHT = Facing.RIGHT
    FORWARD = 10
    BACKWARD = 11
    SHOOT = 12
    
    command_to_str = {
        Facing.UP: 'UP',
        Facing.DOWN: 'DOWN',
        Facing.LEFT: 'LEFT',
        Facing.RIGHT: 'RIGHT',
        10: 'FORWARD',
        11: 'BACKWARD',
        12: 'SHOOT'
    }
    
    def __init__(self, tank):
        self.tank = tank
        self.tank.brain = self
        
        self.memory = []
        
        self.setup()

    def detach(self):
        '''Detach brain in preparation for attaching a new one.'''
        self.tank.brain = None
        self.tank = None
        
    def forget(self):
        '''Forget (clear) saved command queue'''
        self.memory = []
        
    def pop(self):
        '''Return and remove the first command in the queue.'''        
        if len(self.memory):        
            return self.memory.pop(0)
        else:
            return None
        
    def set_facing(self, facing):
        '''Queue the command to change to a certain facing.'''
        if facing is Facing.UP:
            self.face_up()
        elif facing is Facing.DOWN:
            self.face_down()
        elif facing is Facing.RIGHT:
            self.face_right()
        elif facing is Facing.LEFT:
            self.face_left()
        else:
            raise Exception('brain malfunction')
        
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
        return self.tank.get_facing()
        
    def direction(self):
        '''Return the facing of the tank.
           It returns (dx,dy) pointing in the direction the tank is.'''
        return self.tank.get_facing_vector()
        
    def radar(self, x, y):
        '''Return the tile information for a given coordinate.
           Returns (terrain, item). If no terrain or item, it uses None.
           See the World docs for some terrain types.'''
        return self.tank.world.get_tile(x, y)
       
    def kill(self):
        '''Destroys the tank.'''
        self.tank.kill()
        
    def setup(self):
        '''Sets up the brain for the round.'''
        pass
        
    def think(self):
        '''Implement this in your custom brain. 
           It is only called if the tank has no commands.'''
        pass

def import_think(name):
    if name in sys.modules:
        reload(sys.modules[name])
    else:
        __import__(name)

    return sys.modules[name]


def do_think(tank, thinker):
    #for 
    thinker.think()

        
        
import random
        
class DumbBrain(Brain):
    def setup(self):
        pass

    def think(self):
        self.forget() # clear old commands 
        
        color = self.tank.color()
            
        x,y = self.position()
        face = self.facing()
        dx, dy = self.direction()
        
        target = self.radar(x + dx, y + dy)
        print color, "at", x, y, "and facing", Facing.facing_to_str[face]
        print color, "will be moving into:", target

        def new_facing():
            # out of all facing possibilities, choose one we don't have currently
            new_facing = [Facing.UP, Facing.DOWN, Facing.LEFT, Facing.RIGHT]
            new_facing.remove(face)
            return random.choice(new_facing)
        
        # avoid moving into blocking items
        if target[1] is not None or target[0] is self.tank.world.water or target[0] is None:
            self.set_facing(new_facing())
        elif random.randint(0,5) == 0:
            # 1 out of 5 times choose a new direction
            self.set_facing(new_facing())
        
        self.move_forward()
        
        queue = ', '.join([self.command_to_str[x] for x in self.memory])
        print color,"brain queue:", queue
