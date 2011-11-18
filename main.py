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

# set sample brains: if you have one put it here
from tank import Tank
from brain import thinker_import, thinker_think
import sys

sys.path.append('brains')
THINKER1 = thinker_import('wander')
THINKER2 = thinker_import('wander')

import pyglet
from pyglet.window import key
import pyglet.gl as gl
import os, traceback

from world import World

class Game(pyglet.window.Window):
    def __init__(self, thinkers):
        config = pyglet.gl.Config(buffer_size=32, 
                                  alpha_size=8, 
                                  double_buffer=True)
        super(Game, self).__init__(width=1024, height=768,
                                   config=config, resizable=True)
       
        self.world = World(10, 8)
        self.thinkers = thinkers
        
        pyglet.clock.schedule_interval(self.update_closure(), 1.0/60.0)
        
        font = pyglet.font.load("terminal", bold=True)
        color = (0.0, 1.0, 1.0, 1.0)
        fmt = '%(fps).1f'
        self.fps_display = pyglet.clock.ClockDisplay(font=font, 
                                                     color=color, 
                                                     format=fmt)
        
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)

    def update_closure(self):
        def update(dt):
            game_over = False

            for tank, thinker in zip(self.world.tanks, self.thinkers):
                if tank.brain:
                    try:
                        if tank.is_idle():
                            thinker_think(tank, thinker)
                    except Exception as e:
                        tank.brain.kill()
                        traceback.print_exc()

            self.world.update(dt)
                
        return update
 
    def on_draw(self):
        self.clear()
        
        self.world.draw()
        
        self.fps_display.draw()
        

if __name__ == '__main__':
    Game((THINKER1, THINKER2))
    pyglet.clock.set_fps_limit(60)
    pyglet.app.run()
