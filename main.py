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
import math, os, os.path, sys, traceback

import pyglet
from pyglet.window import key
import pyglet.gl as gl

import config
from world import World
from tank import Tank
from brain import thinker_import, thinker_think

class Game(pyglet.window.Window):
    def __init__(self, thinker_colors, thinkers):
        config = pyglet.gl.Config(buffer_size=32,
                                  alpha_size=8,
                                  double_buffer=True)
        super(Game, self).__init__(width=1024, height=768,
                                   config=config, resizable=True)

        self.world = World(10, 8)
        self.thinker_colors = thinker_colors
        self.thinkers = thinkers
        self.world.add_tanks(thinker_colors)

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
            for tank, thinker in zip(self.world.tanks, self.thinkers):
                # only think on tanks that aren't doing anything
                if tank.brain and tank.is_idle():
                    thinker_think(tank, thinker)
            self.world.update(dt)

        return update

    def on_draw(self):
        self.clear()

        self.world.draw()

        self.fps_display.draw()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Simulate tank battles.')
    parser.add_argument('thinkers', metavar='brain', type=str, nargs='+',
                        help='thinker file to power a brain')
    parser.add_argument('--debug', dest='debug', action='store_true',
                        help='print simulation debugging')

    args = parser.parse_args()
    config.DEBUG = args.debug
    if config.DEBUG:
        print "debugging is ENABLED!"

    num_tanks = len(args.thinkers)
    colors = ['blue', 'red', 'yellow']
    if num_tanks > len(colors):
        sys.exit("too many tanks! only %d tanks supported" % len(colors))
    colors = colors[:num_tanks]

    def modname(color, filename):
        return "%s_%s" % (color, os.path.basename(filename).replace('.py',''))

    thinkers = zip(colors, args.thinkers)
    thinkers = [thinker_import(modname(col, f), f) for col, f in thinkers]

    Game(colors, thinkers)
    pyglet.clock.set_fps_limit(60)
    pyglet.app.run()
