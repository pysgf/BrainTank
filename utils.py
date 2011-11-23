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

import sys, time

class Enum(object):
    '''Crappy enum emulator'''
    
    class Item(object):
        def __init__(self, name):
            self.__name = str(name)
        
        def __repr__(self):
            return self.__name
    
    def __init__(self, *args):
        self.values = []
        for name in args:
            item = Enum.Item(name)
            setattr(self, name, item)
            self.values.append(item)
    
class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
    def touches(self, o):
        # important: y is inverted in our projection...
        if o.x + o.w < self.x:
            return False
        if o.y + o.h > self.y:
            return False
        if o.x > self.x + self.w:
            return False
        if o.y < self.y + self.h:
            return False
            
        return True
        
    def debug_draw(self):
        import pyglet
        import pyglet.gl as gl
        
        x,y,w,h = self.x, self.y, self.w, self.h
        vertex_list = pyglet.graphics.vertex_list(4,    
            ('v2f', (x,y, x+w,y, x+w,y+h, x,y+h)),
            ('c3B', (255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0))
        )
        vertex_list.draw(gl.GL_LINE_LOOP)

        
class Animation:
    '''Handle a linear animation of a given value.'''
    
    def __init__(self, start, stop, speed):
        self.start = start
        self.value = start
        self.stop = stop
        self.speed = speed
        self.done = False
        
    def unit(self):
        return self.value / (self.stop - self.start)
        
    def update(self, dt):
        if not self.done:
            self.value += self.speed * dt
            if self.value >= self.stop:
                self.done = True
                
    def __str__(self):
        return "Animation at %.2f of %.2f (+%.2f)" % (self.value, self.stop, self.speed)            


class DebugWriter:
    def __init__(self, label):
        self.label = label
        self.sink = sys.__stdout__
        self.newline = True

    def write(self, msg):
        if self.newline:
            s = "%5s [%4.4f]: %s" % (self.label, time.clock(), msg)
            self.newline = False
        else:
            s = "%s" % msg

        if msg.find('\n') != -1:
            self.newline = True

        self.sink.write(s)

