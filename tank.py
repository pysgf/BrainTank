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
from utils import Animation, Facing, Symbol, Rect
from brain import Brain

class Bullet:
    '''Represents a moving bullet with facing'''
    
    def __init__(self, tank):
        self.tank = tank
        self.speed = 200

        self.facing = Facing(tank.get_facing())
        fv = self.tank.facing.value
        
        self.img = tank.bullet_facing_img[fv]
        self.hw = self.img.width * 0.5
        self.hh = self.img.height * 0.5
       
        self.x, self.y = tank.get_position()
        self.x, self.y = tank.world.world_to_screen(self.x, self.y)

        ts = tank.world.tile_size
        
        if fv is Symbol.UP:
            self.x += ts[0] * 0.5
            self.y -= ts[1] * 0.5
        elif fv is Symbol.DOWN:
            self.x += ts[0] * 0.5
            self.y += ts[1] * 0.5
        elif fv is Symbol.RIGHT:
            self.x += ts[0] 
        elif fv is Symbol.LEFT:
            pass
            
    def __repr__(self):
        return "Bullet(%s)" % self.tank.color
            
    def rect(self):
        '''Returns a Rect suitable for collision detection'''
        return Rect(self.x-self.hw, self.y-self.hh, self.img.width, self.img.height)
        
    def draw(self):
        #print "drawing bullet at", self.x, self.y
        hw, hh = self.hw, self.hh
        self.img.blit(self.x, self.y)

        #self.rect().debug_draw()
        
    def update(self, dt):
        step = self.speed * dt
        dx, dy = self.facing.to_vector()
        self.x += dx * step
        self.y -= dy * step
        
            
class Tank:
    '''Draws and handles tank actions.'''

    IDLE, MOVING, TURNING, SHOOTING, DEAD = range(5)
    state_str = dict(zip(range(5),
        ('IDLE', 'MOVING', 'TURNING', 'SHOOTING', 'DEAD')
    ))
    
    def __init__(self, world, x, y, facing, color):
        self.set_position(x,y)
        self.facing = Facing(facing)
        self.color = color

        self.offset_dt = (0,0)
        self.offset = (0,0)
        
        self.state = self.IDLE
        self.driving_forward = True
        self.animation = None
        self.brain = Brain(self)
        self.world = world
        self.bullet = None
        self.shots = 0
        
        # speed is per second
        self.speed = 100 
        self.reduced_speed = self.speed *0.5
        
        self.load_resources()
        
    def __str__(self):
        return "%s tank" % self.color
        
    def __repr__(self):
        return "Tank(%s)" % self.color
        
    def rect(self):
        '''Returns a Rect suitable for collision'''
        x,y = self.world.world_to_screen(self.x, self.y)
        x += self.offset[0]
        y += self.offset[1] + self.world.half_stack
        return Rect(x, y, self.world.tile_size[0], self.world.tile_size[1])

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
        
        # build images
        img = pyglet.resource.image('tank/bullet.png')
        img.anchor_x = img.width * 0.5
        img.anchor_y = img.height * 0.5
        
        rot_lookup = {
            Symbol.UP: 0,
            Symbol.RIGHT: 90,        
            Symbol.DOWN: 180,
            Symbol.LEFT: 270,
        }
        self.bullet_facing_img = {
            x: img.get_transform(rotate=rot_lookup[x])
                for x in (Symbol.UP, Symbol.DOWN, Symbol.LEFT, Symbol.RIGHT)
        }
        
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
        #self.rect().debug_draw()
    
    def read_command(self):
        '''Pop a command from the brain memory and interpret it'''
        if self.brain:
            command = self.brain.pop()
            if command in Symbol.vals:
                #print self.color, 'executing', Symbol.str[command]
                pass
            
            if command in (Symbol.FORWARD, Symbol.BACKWARD):
                self.state = self.MOVING
                self.offset_dt = self.facing.to_vector()

                self.driving_forward = (command is Symbol.FORWARD)

                end = self.world.tile_size[0]
                if self.facing.value in (Symbol.DOWN, Symbol.UP):
                    end = self.world.tile_size[1]

                self.animation = Animation(0, abs(end), 1.0)
             
            if command in (Symbol.UP, Symbol.DOWN, Symbol.LEFT, Symbol.RIGHT):
                self.state = self.TURNING
                self.turn_to = command # bleh
                
                time_to_turn = 1.0
                if command in (Symbol.UP, Symbol.DOWN):
                    if self.facing.value in (Symbol.LEFT, Symbol.RIGHT):
                        time_to_turn = 0.5
                        
                else:
                    if self.facing.value in (Symbol.UP, Symbol.DOWN):
                        time_to_turn = 0.5
                        
                if command == self.facing.value:
                    time_to_turn = 0
                        
                self.animation = Animation(0, time_to_turn, 1.0)
                
            if command is Symbol.SHOOT and self.bullet is None:
                #print self.color, 'is SHOOTING'
                self.state = self.SHOOTING
                
    def stop(self):
        '''Stop current state and return to idle.'''
        self.offset = (0,0)
        self.animation = None
        self.state = self.IDLE
                
    def update(self, dt):
        '''Process tank state, with respect to time'''
        if self.animation:
            self.animation.update(dt)

        if self.state is self.IDLE:
            self.read_command()            
    
        if self.state is self.TURNING:
            if self.animation.done:
                self.state = self.IDLE
                self.facing.value = self.turn_to
            return
    
        if self.state is self.SHOOTING:
            self.shots += 1
            self.bullet = Bullet(self)
            self.world.add_bullet(self.bullet)
            self.state = self.IDLE
            return
    
        if self.state is self.MOVING:
            o = self.offset
            dt = self.offset_dt
            anim = self.animation
            world = self.world
            
            sign = 1 if self.driving_forward else -1

            if anim.done: # done moving, warp to final destination
               # set up a warp
               self.warp_x = self.x + dt[0]*sign
               self.warp_y = self.y + dt[1]*sign

               world.warp(self)
               self.set_position(self.warp_x, self.warp_y)
               self.stop()
               
            else: # still moving
                target = world.get_tile(self.x+dt[0]*sign, self.y+dt[1]*sign)
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
                
                self.offset = (dt[0]*anim.value*sign+jitter[0], 
                               -dt[1]*anim.value*sign+jitter[1])      

            
    def is_idle(self):
        return self.state == self.IDLE
        
    def kill(self):
        print "BANG! %s is dead." % self.color
        
        self.state = self.DEAD
        
        if self.brain:
            self.brain.detach()
            self.world.detonate(self)

        
