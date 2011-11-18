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

import pyglet
from pyglet.window import key
import pyglet.gl as gl
import os, random
from utils import Animation, Facing, Symbol
from brain import Brain

            
class Tank:
    '''Draws and handles tank actions.'''

    IDLE, MOVING, TURNING, SHOOTING, DEAD = range(5)
    state_str = dict(zip(range(5),
        ('IDLE', 'MOVING', 'TURNING', 'SHOOTING', 'DEAD')
    ))
    
    def __init__(self, world, x, y, facing, color, tile_offset):
        self.set_position(x,y)
        self.facing = Facing(facing)
        self.color = color

        self.offset_dt = (0,0)
        self.offset = (0,0)
        self.tile_offset = tile_offset
        
        self.state = self.IDLE
        self.animation = None
        self.brain = Brain(self)
        self.world = world
        
        # speed is per second
        self.speed = 100 
        self.reduced_speed = self.speed *0.5
        
        self.load_resources()
        
    def __str__(self):
        return "%s tank" % self.__color
        
    def __repr__(self):
        return "Tank(%s)" % self.__color

    def get_facing(self):
        '''Returns the facing as Facing.LEFT, Facing.RIGHT, etc'''
        return self.facing.value

    def get_facing_vector(self):
        '''Returns the facing as (dx,dy)'''
        return self.facing.to_vector()
        
    def get_position(self):
        '''Returns position (x,y) as a tuple'''
        return (self.x, self.y)
        
    def get_warp_destination(self):
        '''Used in World to get the tank's warp coordinates.'''
        return (self.warp_x, self.warp_y)
        
    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.warp_x = None
        self.warp_y = None
        
    def load_resources(self):
    
        def load(dir):
            pack = "tank"
            col = self.color
            return pyglet.resource.image('%s/%s_%s.png' % (pack, col, dir))
            
        self.up = load('up')
        self.down = load('down')
        self.left = load('left')
        self.right = load('right')
        
        # set the images in the order of the Facing enum
        img = self.facing_img = [None]*4
        img[Symbol.UP] = self.up
        img[Symbol.DOWN] = self.down
        img[Symbol.LEFT] = self.left
        img[Symbol.RIGHT] = self.right
       
    def blit(self, x, y, z):
        x += self.offset[0]
        y += self.offset[1]
        self.facing_img[self.facing.value].blit(x, y, z)
    
    def read_command(self):
        if self.brain:
            command = self.brain.pop()
            if command in Symbol.vals:
                print self.color, 'executing', Symbol.str[command]
            
            if command in (Symbol.FORWARD, Symbol.BACKWARD):
                self.state = self.MOVING
                self.offset_dt = self.facing.to_vector()
                
                end = self.tile_offset[0]
                if self.facing.value in (Symbol.DOWN, Symbol.UP):
                    end = self.tile_offset[1]
                    
                self.animation = Animation(0, abs(end), 1.0)
             
            if command in (Symbol.UP, Symbol.DOWN, Symbol.LEFT, Symbol.RIGHT):
                self.state = self.TURNING
                self.facing.value = command
                
    def stop(self):
        '''Stop current state and return to idle.'''
        self.offset = (0,0)
        self.animation = None
        self.state = self.IDLE
                
    def update(self, dt):
        if self.animation:
            self.animation.update(dt)

        if self.state is self.IDLE:
            self.read_command()            
    
        if self.state is self.TURNING:
            self.state = self.IDLE
            return
    
        if self.state is self.MOVING:
            o = self.offset
            dt = self.offset_dt
            anim = self.animation
            world = self.world
            
            if anim.done: # done moving, warp to final destination
               # set up a warp
               self.warp_x = self.x + dt[0]
               self.warp_y = self.y + dt[1]

               world.warp(self)
               self.set_position(self.warp_x, self.warp_y)
               self.stop()
               
            else: # still moving
                target = world.get_tile(self.x+dt[0], self.y+dt[1])
                current = world.get_tile(self.x, self.y)
                
                # look for blocking items
                if target[0] in world.blocking or target[1] in world.blocking_item:
                    self.stop()
                    print self.color, 'tried to drive into item, stopping'
                    return
                    
                # don't move off map
                if target[0] is None:
                    self.stop()
                    print self.color, 'tried to drive off map, stopping'
                    return
                
                # don't collide with another tank
                if target[1] in world.tanks:
                    self.stop()
                    print self.color, 'tried to ram another tank, stopping'
                    return
                
                # move speed adjustment
                jitter = (0,0)
                ri = random.randint
                progress = anim.unit()
                anim.speed = self.speed
                if current[0] is world.dirt and progress < 0.5:
                    anim.speed = self.reduced_speed
                    jitter = (ri(-1,1),ri(0,2))
                if target[0] is world.dirt and progress > 0.5:
                    anim.speed = self.reduced_speed
                    jitter = (ri(-1,1),ri(0,2))
                
                self.offset = (dt[0]*anim.value+jitter[0], 
                               -dt[1]*anim.value+jitter[1])      

            
    def is_idle(self):
        return self.state == self.IDLE
        
    def kill(self):
        print "BANG! %s is dead." % self.color
        
        self.brain.detach()
        self.brain = None
        
        self.state = self.DEAD
        
        if self.brain:
            self.world.detonate(self)

        
