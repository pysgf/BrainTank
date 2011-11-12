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

class Tank:
    '''Draws and handles tank actions.'''

    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    
    def __init__(self, x, y, color, offset_delta, facing=0):
        self.__set_position(x,y)
        self.color = color
        self.facing = facing
        self.fire = 0
        self.move = 0
        self.offset = (0,0)
        self.offset_delta = offset_delta
        self.target = None
        self.brain = None
        
        self.load_resources()
        
    def get_position(self):
        '''Returns position (x,y) as a tuple'''
        return (self.__x, self.__y)
        
    def get_warp_destination(self):
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
        
        self.facing_img = (self.up, self.down, self.left, self.right)
       
    def blit(self, x, y, z):
        x += self.offset[0]
        y += self.offset[1]
        self.facing_img[self.facing].blit(x, y, z)
        
    def update(self, dt):
        if not self.brain:
            return
            
        world = self.brain.world
    
        if self.move != 0:
            facing = self.facing
            speed = self.move
            
            def clamp(x):
                if x > 0:
                    return 1
                elif x < 0:
                    return -1
                else:
                    return 0
            
            speed = clamp(speed)
                
            self.move = speed
                
            dx, dy = 0, 0
            
            if facing is self.UP:
                dy = -speed
            elif facing is self.DOWN:
                dy = speed
            elif facing is self.LEFT:
                dx = -speed
            elif facing is self.RIGHT:
                dx = speed
            else:
                raise Exception('Brain meltdown')
                
            target = world.get_tile(self.__x+dx, self.__y+dy)
            current = world.get_tile(self.__x, self.__y)
            if current[0] is world.dirt:
                dx *= 0.5
                dy *= 0.5
            
            o = self.offset
            self.offset = (o[0]+dx, o[1]+dy)
            
            # see if we're done moving
            o = self.offset
            od = self.offset_delta
            q = lambda x: abs(int(x))
            if q(o[0]) == abs(od[1]) or q(o[1]) == abs(od[1]):
               self.offset = (0,0)
               self.move = 0
               
               # set up a warp
               self.__warp_x = self.__x + clamp(dx)
               self.__warp_y = self.__y + clamp(dy)
               #print self.color, "is preparing to warp to", self.__warp_x, self.__warp_y
               #print "it is currently at", self.__x, self.__y
               #print "deltas were", dx, dy
               world.warp(self)
               self.__set_position(self.__warp_x, self.__warp_y)
            
    def is_busy(self):
        if self.move != 0:
            return True
            
        return False
        
    def kill(self):
        print "BANG! %s is dead." % self.color
        if self.brain:
            self.brain.world.detonate(self)

        