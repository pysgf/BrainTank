#!/usr/bin/python
# -*- coding: utf-8 -*-

###############################################################################
# Python AI Battle
#
# Copyright 2012 James Vann
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

'''
James Vann's Brain.

This is my first publicly avaible code, and I would apprecaite any comments on my methods/style. 

Ideas for Improvement:

1) Create a proxy class that would set between the calls to game functions, and cache certain things like radar requests.  This way, once a tile type has been determined, it does not have to be checked again- the proxy class caches the result.  This would give the brain a memory :)

2) Some of the logic could be turned into additional functions, making manteniance a bit easier.

'''
class Intelligence(object):
    def __init__(self):
        self.world_dimension_x = 10
        self.world_dimension_y = 8
    
    def tile_safe(self,game,direction):
        ''' returns True if tile is safe to enter, returns False if it is not, fires if it contains an obstacle, then returns True
        '''
        if direction == game.UP:
            radar_result = game.radar(game.position[0],game.position[1]-1)
        elif direction == game.DOWN:
            radar_result = game.radar(game.position[0],game.position[1]+1)
        elif direction == game.RIGHT:
            radar_result = game.radar(game.position[0]+1,game.position[1])
        elif direction == game.LEFT:
            radar_result = game.radar(game.position[0]-1,game.position[1])
        else:
            print('{0} is not a valid direction'.format(direction))
            return False
            
        print('Vann looks {0} and sees {1} and {2}'.format(direction,radar_result[0],radar_result[1]))
        if radar_result[0] in [game.GRASS, game.DIRT, game.PLAIN]:  #all safe tiles
            if radar_result[1] == None:
                return True
            else:
                self.face(game,direction)
                self.shoot(game)
                return True
        else:
            return False
                
    def move_x(self,game):
        if game.tank_positions[0][0] > game.position[0]:
            if self.tile_safe(game,game.RIGHT):
                self.face(game,game.RIGHT)
                print('Vann moving Right')
                self.forward(game)
                print("Vann's commands are {0}".format(game.memory))
            else:
                self.face(game,game.RIGHT)
                self.shoot(game)
                print("Vann's commands are {0}".format(game.memory))

        else:
            self.shoot(game)
            print("Vann's commands are {0}".format(game.memory))
    
   
    def face(self,game,direction):
        ''' This function checks to see if tank is already facing direction (UP,DOWN,LEFT,RIGHT) and if not it changes direction, if it is, it does nothing. Also filters to make sure it only has one such command in queue.
        '''
        if game.facing == direction:
            pass
        else:
            if direction not in game.memory:
                game.face(direction)
            
    def forward(self,game):
        ''' This function wraps the game.forward() function in an attempt to prevent the command queue from filling up.  It checks to see if a command already exists to perform an action before adding it again'''
        if game.FORWARD not in game.memory:
            game.forward()
        else:
            print('Already queued')
            
    def shoot(self,game):
        ''' This function wraps the game.shoot() function in an attempt to prevent the command queue from filling up.  It checks to see if a command already exists to perform an action before adding it again'''
        if game.SHOOT not in game.memory:
            game.shoot()
        else:
            print('Already queued')

    def get_action(self,game):
        ''' This is where the real logic goes- what does the tank do?'''
        print("Vann's commands are {0}".format(game.memory))
        if game.tank_positions[0][0] == game.position[0]:
            if game.tank_positions[0][1] > game.position[1]:
                self.face(game,game.DOWN)
                self.shoot(game)
                print("Vann's commands are {0}".format(game.memory))
            else:
                self.face(game,game.UP)
                self.shoot(game)
                print("Vann's commands are {0}".format(game.memory))

        elif game.tank_positions[0][1] == game.position[1]:
            if game.tank_positions[0][0] > game.position[0]:
                self.face(game,game.RIGHT)
                self.shoot(game)
                print("Vann's commands are {0}".format(game.memory))
            else:
                self.face(game,game.LEFT)
                self.shoot(game)
                print("Vann's commands are {0}".format(game.memory))
        
        else:
            if game.tank_positions[0][1] > game.position[1]:
                if self.tile_safe(game,game.DOWN):
                    self.face(game,game.DOWN)
                    print('Vann moving DOWN')
                    self.forward(game)
                    print("Vann's commands are {0}".format(game.memory))
                else:
                    self.move_x(game)
            
            elif game.tank_positions[0][1] < game.position[1]:
                if self.tile_safe(game,game.UP):
                    self.face(game,game.UP)
                    print('Vann moving UP')
                    self.forward(game)
                    print("Vann's commands are {0}".format(game.memory))
                else:
                    self.move_x(game)
        
                    
    
# create an instance of intelligence

my_brain = Intelligence()   
def think(game):
    
    my_brain.get_action(game)

       
        
    


