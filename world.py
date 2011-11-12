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
from tank import Tank, Facing

class VoidKill(Exception):
    pass

class World:
    '''Generates, draws, and provides info about game worlds.'''

    def __init__(self, width, height, seed=None):
        self.width = width
        self.height = height
        self.rand = random.Random()
        self.rand.seed(seed)
        
        self.game_over = False
        
        self.load_resources()
        self.generate_map()
        
    def get_tile(self, x, y):
        '''Returns a (tile, item) tuple.
           tile will be a type:
               world.grass, dirt, etc
           item will be None or an item:
               world.rock, tree, etc
           '''
        if not(x >= 0 and x < self.width):
            return (None, None)
           
        if not(y >= 0 and y < self.height):
            return (None, None)
        
        return self.__map[y][x]
        
    def load_resources(self):

        def load(name):
            pack = "PlanetCute PNG"
            return pyglet.resource.image('%s/%s.png' % (pack, name))
            
        self.grass = load('Grass Block')
        self.dirt = load('Dirt Block')
        self.wall = load('Stone Block Tall')
        self.brown = load('Brown Block')
        self.plain = load('Plain Block')
        self.water = load('Water Block')
        
        self.safe = (self.dirt, self.grass, self.brown, self.plain)
        self.unsafe = (self.water,)
        self.blocking = (self.wall,)
        
        self.spawn = load('Selector')
        self.rock = load('Rock')
        self.tree = load('Tree Tall')
        self.bush = load('Tree Short')
        self.heart = load('Heart')
        self.gem = load('Gem Blue')
        
        self.tile_height = self.grass.texture.height
        self.tile_width = self.grass.texture.width
        
        self.half_stack = 43
        self.adjacent_stack = -81
        self.adjacent_side = self.tile_width
        self.start_x = 0
        self.start_y = (self.height-1) * -self.adjacent_stack
       
    def generate_map(self):
        self.__map = [[(self.grass, None)]*self.width for x in range(self.height)]
        
        def distmap(pairs):
            return [i for sublist in [[x]*y for x,y in pairs] for i in sublist]
        
        # spawn lists
        terrain = distmap(((self.grass, 20), (self.dirt, 5), (self.wall, 0), (self.water, 1)))
        items = distmap(((None, 20), (self.rock,3), (self.tree,3)))

        # generate actual map
        r = self.rand
        for row in self.__map:
            for i in range(len(row)):
                tile = r.choice(terrain)
                item = None
                if tile in self.safe: # avoid water etc for placeables
                    item = r.choice(items)
                    
                row[i] = (tile, item)
                
        # clear spawn points
        s1 = (0, 0, Facing.RIGHT)
        s2 = (self.width-1, self.height-1, Facing.LEFT)
        if r.randint(0,1):
            s1, s2 = s2, s1
        
        tile_offset = (self.adjacent_stack, self.adjacent_side)
        self.red_tank = Tank(s1[0], s1[1], s1[2], 'red', tile_offset)
        self.blue_tank = Tank(s2[0], s2[1], s2[2], 'blue', tile_offset)
        
        self.__set_tile(s1, (self.plain, self.red_tank))
        self.__set_tile(s2, (self.plain, self.blue_tank))
        
    def __set_tile(self, pos, data):
        print "setting", pos, data
        self.__map[pos[1]][pos[0]] = data
        
    def draw(self):
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glDepthFunc(gl.GL_LEQUAL)
        
        dx = self.adjacent_side
        dy = self.adjacent_stack
        stacked = self.half_stack
        
        # terrain pass
        x, y = self.start_x, self.start_y
        for row in self.__map:
            x = self.start_x
            for tile,item in row:
                tile.blit(x,y,0)
                x += dx
            y += dy
            
        # item pass
        x, y = self.start_x, self.start_y
        for row in self.__map:
            x = self.start_x
            for tile,item in row:
                if item is not None:
                    item.blit(x,y+stacked,1)
                x += dx
            y += dy

    def warp(self, tank):
        '''Called before tank sets x,y to new tile.'''
        pos = tank.get_position()
        wpos = tank.get_warp_destination()
        
        src = self.get_tile(pos[0], pos[1])
        dst = self.get_tile(wpos[0], wpos[1])
        if dst[0] not in self.safe and tank.brain:
            tank.brain.kill()
            return
            
        self.__set_tile(pos, (src[0], None))
        self.__set_tile(wpos, (dst[0], tank))
        
                
    def update(self, dt):
        if not self.game_over:
            tanks = [self.red_tank, self.blue_tank]
            self.rand.shuffle(tanks)

            # bad tanks will try to escape the game board, capture them
            try:
                tanks[0].update(dt)
            except VoidKill:
                tanks[0].kill()
                
            try:
                tanks[1].update(dt)
            except VoidKill:
                tanks[1].kill()

    def detonate(self, thing):
        if thing in (self.red_tank, self.blue_tank):
            self.game_over = True
            
        # TODO: set up explosion
        