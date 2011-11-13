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
from utils import Animation, Facing
from brain import Brain

            
class Tank:
    '''Draws and handles tank actions.'''

    IDLE = 0
    MOVING = 1
    SHOOTING = 2
    DEAD = 3
    
    def __init__(self, x, y, facing, color, tile_offset):
        self.__set_position(x,y)
        self.facing = Facing(facing)
        self.color = color

        self.velocity = 0
        
        self.offset_dt = (0,0)
        self.offset = (0,0)
        self.tile_offset = tile_offset
        
        self.state = self.IDLE
        self.animation = None
        self.brain = None
        
        # speed is per second
        self.speed = 100 
        self.reduced_speed = self.speed *0.5
        
        self.load_resources()
        
    def get_position(self):
        '''Returns position (x,y) as a tuple'''
        return (self.__x, self.__y)
        
    def get_warp_destination(self):
        '''Used in World to get the tank's warp coordinates.'''
        return (self.__warp_x, self.__warp_y)
        
    def __set_position(self, x, y):
        self.__x = x
        self.__y = y
        self.__warp_x = None
        self.__warp_y = None
        
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
        img[Facing.UP] = self.up
        img[Facing.DOWN] = self.down
        img[Facing.LEFT] = self.left
        img[Facing.RIGHT] = self.right
       
    def blit(self, x, y, z):
        x += self.offset[0]
        y += self.offset[1]
        self.facing_img[self.facing.value].blit(x, y, z)
    
    def read_command(self):
        if self.brain:
            command = self.brain.pop()
            
            if command in (Brain.FORWARD, Brain.BACKWARD):
                self.state = self.MOVING
                self.offset_dt = self.facing.to_vector()
                self.animation = Animation(0, abs(self.tile_offset[1]), 1.0)
             
            if command in (Brain.LEFT, Brain.RIGHT):
                self.state = self.MOVING
                self.offset_dt = self.facing.to_vector()
                self.animation = Animation(0, abs(self.tile_offset[0]), 1.0)
                
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
    
        if self.state is self.MOVING:
            o = self.offset
            dt = self.offset_dt
            anim = self.animation
            world = self.brain.world
            
            if anim.done: # done moving, warp to final destination
               # set up a warp
               self.__warp_x = self.__x + dt[0]
               self.__warp_y = self.__y + dt[1]

               world.warp(self)
               self.__set_position(self.__warp_x, self.__warp_y)
               self.stop()
               
            else: # still moving
                target = world.get_tile(self.__x+dt[0], self.__y+dt[1])
                current = world.get_tile(self.__x, self.__y)
                
                # look for blocking items
                if target[0] in world.blocking or target[1] in world.blocking_item:
                    self.stop()
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
                               dt[1]*anim.value+jitter[1])         

            
    def is_idle(self):
        return self.state == self.IDLE
        
    def kill(self):
        print "BANG! %s is dead." % self.color
        
        self.state = self.DEAD
        
        if self.brain:
            self.brain.world.detonate(self)

        