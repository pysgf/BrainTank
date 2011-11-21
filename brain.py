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
from utils import Facing, Symbol

class Brain:
    '''The Brain is your primary interface to write a custom tank AI.'''
        
    def __init__(self, tank):
        self.tank = tank
        self.tank.brain = self
        
        self.memory = []

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
        
    def face(self, facing):
        '''Queue the command to change to a certain facing.'''
        if facing in (Symbol.UP, Symbol.DOWN, Symbol.LEFT, Symbol.RIGHT):
            self.memory.append(facing)
        else:
            raise Exception('brain malfunction')
        
    def forward(self):
        '''Queue the command to move the tank forward.
           The direction depends on the tank's current facing.'''
        self.memory.append(Symbol.FORWARD)
        
    def backward(self):
        '''Queue the command to move the tank backward.
           The direction depends on the tank's current facing.'''
        self.memory.append(Symbol.BACKWARD)
        
    def shoot(self):
        '''Queue a shoot command.
           The direction depends on the tank's current facing.'''
        self.memory.append(Symbol.SHOOT)
        
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
        ss = self.tank.world.symbol_to_safe
        tile, item = self.tank.world.get_tile(x, y)
        return (ss.get(tile), ss.get(item))
        
    def kill(self):
        '''Destroys the tank.'''
        self.tank.kill()


def thinker_import(name):
    '''Import a new thinker or reload it if it exists already'''
    if name in sys.modules:
        reload(sys.modules[name])
    else:
        __import__(name)

    return sys.modules[name]


def thinker_think(tank, thinker):
    '''Set up globals for thinking module and run think()'''
    brain = tank.brain
    
    # vars
    thinker.color = tank.color
    thinker.position = brain.position()
    thinker.facing = brain.facing()
    thinker.direction = brain.direction()
    thinker.shots = tank.shots
    
    thinker.UP = Symbol.UP
    thinker.DOWN = Symbol.DOWN
    thinker.LEFT = Symbol.LEFT
    thinker.RIGHT = Symbol.RIGHT
    thinker.SHOOT = Symbol.SHOOT
    thinker.FORWARD = Symbol.FORWARD
    thinker.BACKWARD = Symbol.BACKWARD
    
    thinker.SYMBOL_TO_STR = {}
    thinker.SYMBOL_TO_STR.update(Symbol.str)
    
    thinker.FACING_TO_VEC = {}
    thinker.FACING_TO_VEC.update(Facing.vec)
    
    world = tank.world
    ss = world.symbol_to_safe
    
    thinker.GRASS = ss[world.grass]
    thinker.DIRT = ss[world.dirt]
    thinker.PLAIN = ss[world.plain]
    thinker.WATER = ss[world.water]
    
    thinker.SAFE_TILES = [ss[x] for x in world.safe]
    thinker.UNSAFE_TILES = [ss[x] for x in world.unsafe]
    
    thinker.ROCK = ss[world.rock]
    thinker.TREE = ss[world.tree]
    
    thinker.tanks = [ss[x] for x in world.tanks]
    thinker.tank_positions = [x.get_position() for x in world.tanks 
                              if x is not tank]
    
    # functions
    thinker.memory = lambda: brain.memory[:]
    thinker.forget = brain.forget
    thinker.face = brain.face
    thinker.forward = brain.forward
    thinker.backward = brain.backward
    thinker.shoot = brain.shoot
    thinker.radar = brain.radar
    thinker.kill = brain.kill
    
    # start a think cycle
    thinker.think()
