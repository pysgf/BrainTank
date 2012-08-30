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

2) Add in more intelligent scanning for enemy location- have it start with last kown location and spiral out from there.  If enemy has not yet been spotted, start along the outer border and spiral inward.

3) Some of the logic could be turned into additional functions, making manteniance a bit easier.

'''
class intelligence(object):
    def __init__(self):
        self.world_dimension_x = 10
        self.world_dimension_y = 8
        self.enemy_location = None
        self.scan_x = 1
        self.scan_y = 1
    
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
                game.shoot()
                return True
        else:
            return False
                
    def move_x(self,game):
        if self.enemy_location[0] > game.position[0]:
            if self.tile_safe(game,game.RIGHT):
                self.face(game,game.RIGHT)
                print('Vann moving Right')
                game.forward()
                self.enemy = False
            else:
                self.face(game,game.RIGHT)
                game.shoot()
                self.enemy = False

        else:
            game.shoot()
            self.enemy = False
    
    def scan_map(self,game):
        ''' scan the entire map searching for enemy tank, returns a tuple with the x,y coordinates of enemy tank
        '''
        
        enemy = True
        enemy_tanks = ['TANK_RED','TANK_BLUE']  #If more tanks are added, we must add them here
        if game.color == 'blue':
            enemy_tanks.remove('TANK_BLUE')
        else:
            enemy_tanks.remove('TANK_RED')
            
        print('Searching for enemy tanks {0}'.format(enemy_tanks[0]))


        if enemy:  #scan until we find the enemy
            print('Scanning {0}, {1}'.format(self.scan_x,self.scan_y))
            result = game.radar(self.scan_x,self.scan_y)
            if result[1] == enemy_tanks:
                print('Enemy detected at {0}.{1}'.format(self.scan_x,self.scan_y))
                enemy = False
            else:
                if self.scan_x == self.world_dimension_x:
                    self.scan_x = 1
                    if self.scan_y == self.world_dimension_y:
                        self.scan_y = 1
                    else:
                        self.scan_y += 1
                else:
                    self.scan_x += 1
            
        return self.scan_x,self.scan_y
    
    def face(self,game,direction):
        ''' This function checks to see if tank is already facing direction (UP,DOWN,LEFT,RIGHT) and if not it changes direction, if it is, it does nothing.
        '''
        if game.facing == direction:
            pass
        else:
            game.face(direction)
        

    def get_action(self,game):
        if  self.enemy_location == None:
            #self.enemy_location = self.scan_map(game)
            self.enemy_location = game.tank_positions[0]
        else:
            if self.enemy_location[0] == game.position[0]:
                if self.enemy_location[1] < game.postion[1]:
                    self.face(game,game.DOWN)
                    game.shoot()
                    self.enemy = False
                else:
                    self.face(game,game.UP)
                    game.shoot()
                    self.enemy = False
                    
            elif self.enemy_location[1] == game.position[1]:
                if self.enemy_location[0] > game.postion[0]:
                    self.face(game,game.RIGHT)
                    game.shoot()
                    self.enemy = False
                else:
                    self.face(game,game.LEFT)
                    game.shoot()
                    self.enemy = False
            
            else:

                if self.enemy_location[1] > game.position[1]:
                    if self.tile_safe(game,game.UP):
                        self.face(game,game.UP)
                        print('Vann moving up')
                        game.forward()
                        self.enemy = False
                    else:
                        self.move_x(game)
                
                elif self.enemy_location[1] < game.position[1]:
                    if self.tile_safe(game,game.DOWN):
                        self.face(game,game.DOWN)
                        print('Vann moving Down')
                        game.forward()
                        self.enemy = False
                    else:
                        self.move_x(game)
                    
    
# create an instance of intelligence

my_brain = intelligence()   
def think(game):
    
    print('{0} is Vann'.format(game.color))
    my_brain.get_action(game)

       
        
    


