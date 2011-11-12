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
import os.path as op

class World:
    def __init__(self, width, height, seed=None):
        self.width = width
        self.height = height
        self.rand = random.Random()
        self.rand.seed(seed)
        
        self.load_resources()
        self.generate_map()
        
    def load_resources(self):
        pack = "PlanetCute PNG"
        def load(name):
            return pyglet.image.load(op.join(pack, '%s.png' % name))
            
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
        terrain = distmap(((self.grass, 20), (self.dirt, 5), (self.wall, 2), (self.water, 1)))
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
        self.__map[0][0] = (self.plain, self.spawn)
        self.__map[self.height-1][self.width-1] = (self.plain, self.spawn)
        
    def draw(self):
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        
        dx = self.adjacent_side
        dy = self.adjacent_stack
        stacked = self.half_stack
        
        x, y = self.start_x, self.start_y
        for row in self.__map:
            x = self.start_x
            for tile,item in row:
                tile.blit(x,y)
                if item is not None:
                    item.blit(x,y+stacked)
                x += dx
            y += dy
                
