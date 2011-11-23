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
from tank import Tank
from symbols import Facing, Tile, Item


class VoidKill(Exception):
    pass

class Drawable:
    def __init__(self, name, filename):
        self.name = name
        self.img = pyglet.resource.image(filename)
        
    def blit(self, *args, **kwargs):
        self.img.blit(*args, **kwargs)
        
    def __repr__(self):
        return "Drawable(%s)" % self.name
    
    
class World:
    '''Generates, draws, and provides info about game worlds.'''

    def __init__(self, width, height, seed=None):
        self.width = width
        self.height = height
        self.rand = random.Random()
        self.rand.seed(seed)
        
        self.bullets = []
        self.explosions = []
        self.game_over = False
        
        self.TILE_TO_ENUM = {}
        self.ITEM_TO_ENUM = {}
        
        self.load_resources()
        self.generate_map()
        if self.has_sound:
            self.play_music()
        
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
        
    def get_tile_enum(self, x, y):
        '''Returns a (tile, item) tuple in enum form.
            tile will be a value from symbols.Tile
            item will be a value from symbols.Item'''
        
        tile, item = self.get_tile(x,y)
        return self.TILE_TO_ENUM[tile], self.ITEM_TO_ENUM[item]
        
    def load_resources(self):

        def load(name):
            pack = "PlanetCute PNG"
            return Drawable(name, '%s/%s.png' % (pack, name))
            
        self.grass = load('Grass Block')
        self.dirt = load('Dirt Block')
        #self.wall = load('Stone Block Tall')
        #self.brown = load('Brown Block')
        self.plain = load('Plain Block')
        self.water = load('Water Block')
        
        self.safe = (self.dirt, self.grass, self.plain)
        self.unsafe = (self.water,)
        
        self.tiles = self.safe + self.unsafe
        self.blocking_tiles = []
        
        #self.spawn = load('Selector')
        self.rock = load('Rock')
        self.tree = load('Tree Tall')
        #self.bush = load('Tree Short')
        #self.heart = load('Heart')
        #self.gem = load('Gem Blue')
        
        self.items = (self.rock, self.tree)
        self.blocking_items = self.items
        self.destructible = self.items
        
        self.tile_height = 171
        self.tile_width = 101
        
        self.half_stack = 43
        self.tile_size = (101, -81)
        self.tile_size_inv = (1.0/self.tile_size[0], 1.0/self.tile_size[1])
        self.start_x = 0
        self.start_y = (self.height-1) * -self.tile_size[1]
       
        try:
            self.main_music = pyglet.resource.media('Sounds/xmasmyth.mp3')
            self.has_sound = True
        except pyglet.media.riff.WAVEFormatException:
            self.has_sound = False

    def play_music(self):
        self.main_music.play()

    def generate_map(self):
        self.__map = [[(self.grass, None)]*self.width for x in range(self.height)]
        
        def distmap(pairs):
            return [i for sublist in [[x]*y for x,y in pairs] for i in sublist]
        
        # spawn lists
        terrain = distmap(((self.grass, 20), (self.dirt, 5), (self.water, 1)))
        items = distmap(((None, 20), (self.rock,2), (self.tree,2)))

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
        
        red_tank = Tank(self, s1[0], s1[1], s1[2], 'red')
        blue_tank = Tank(self, s2[0], s2[1], s2[2], 'blue')
        
        self.__set_tile(s1, (self.plain, red_tank))
        self.__set_tile(s2, (self.plain, blue_tank))
        self.tanks = (red_tank, blue_tank)
        
        self.ITEM_TO_ENUM.update({
            None:      None,
            self.rock: Item.ROCK,
            self.tree: Item.TREE,
        })
        self.ITEM_TO_ENUM.update({
            x: x.color.upper() for x in self.tanks
        })
        
        self.TILE_TO_ENUM.update({
            None:       None,
            self.grass: Tile.GRASS,
            self.dirt:  Tile.DIRT,
            self.plain: Tile.PLAIN,
            self.water: Tile.WATER,
        })
        
    def __set_tile(self, pos, data):
        #print "setting", pos, data
        self.__map[pos[1]][pos[0]] = data
        
    def world_to_screen(self, x, y):
        '''Convert tile coordinates to screen pixel coordinates'''
        x = self.start_x + x * self.tile_size[0]
        y = self.start_y + (y-1) * self.tile_size[1]
        return (x,y)

    def screen_to_world(self, x, y):
        '''Convert screen pixel coordinates to tile coordinates'''
        x = (x - self.start_x) * self.tile_size_inv[0]
        y = (y - self.start_y) * self.tile_size_inv[1] + 1
        return (int(x),int(y))
        
    def draw(self):
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glDepthFunc(gl.GL_LEQUAL)
        
        dx = self.tile_size[0]
        dy = self.tile_size[1]
        stack = self.half_stack
        
        # terrain pass
        x, y = self.start_x, self.start_y
        for row in self.__map:
            x = self.start_x
            for tile,item in row:
                tile.blit(x,y,0)
                x += dx
            y += dy
            
        # bullet pass
        
        for bullet in self.bullets:
            bullet.draw()
            
        # item pass
        x, y = self.start_x, self.start_y
        for row in self.__map:
            x = self.start_x
            for tile,item in row:
                if item is not None:
                    item.blit(x,y+stack,1)
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
        dead_expl = []
        for explosion in self.explosions:
            explosion.update(dt)
            if not explosion.is_exploding():
                dead_expl.append(explosion)
        for explosion in dead_expl:
            self.explosions.remove(explosion)
    
        if not self.game_over:
            # update bullets
            dead_bullets = []
            for bullet in self.bullets:
                bullet.update(dt)
                x,y = self.screen_to_world(bullet.x, bullet.y)
                tile, item = self.get_tile(x,y)
                #print "bullet at", x, y, "facing", bullet.facing
                if x < 0 or y < 0 or x >= self.width or y >= self.height:
                    dead_bullets.append(bullet)
                elif item in self.destructible:
                    self.detonate(item, pos=(x,y))
                    dead_bullets.append(bullet)
                #else:
                    #self.__set_tile((x,y), (tile, self.spawn))
                    
            for bullet in dead_bullets:
                self.bullets.remove(bullet)
                bullet.tank.bullet = None # bleh
                self.detonate(bullet)

            # update tanks
            tanks = list(self.tanks)
            self.rand.shuffle(tanks)

            for tank in tanks:
                tank.update(dt)
                
                # check for tank collision w/ bullets
                # slow but i'm in a hurry and it's python anyway lol
                trect = tank.rect()
                
                for bullet in self.bullets:
                    #print "checking", tank.color, "against", bullet.tank.color, "'s bullet"
                    if bullet.tank is not tank and bullet.rect().touches(trect):
                        tank.kill()
                        self.detonate(tank)

    def detonate(self, thing, pos=None):
        '''Detonate (destroy) an object on the map, optionally clearing the item at pos'''
        
        print "blowing up", thing
        
        if thing in self.tanks:
            print "GAME OVER!"
            self.game_over = True

        if pos:
            tile, item = self.get_tile(pos[0], pos[1])
            self.__set_tile(pos, (tile, None))
        
    def add_bullet(self, bullet):
        self.bullets.append(bullet)
        
