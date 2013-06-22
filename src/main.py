#!/usr/bin/env python2
# Copyright (C) 2013 Thomas Chace <tchace1@student.gsu.edu>

# Baazi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Baazi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Baazi. If not, see <http://www.gnu.org/licenses/>.

import pygame
import sys
import os
import time
from pygame.locals import *
from characters import *

WIN_WIDTH = 640
WIN_HEIGHT = 480
HALF_WIDTH = 320
HALF_HEIGHT = 240

def camera_func(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)


class Camera(object):
    def __init__(self):
        self.camera_func = camera_func
        self.state = Rect(0, 0, 640*32, 480*32)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

class TestGame():
    def __init__(self):
        pygame.display.init()

        self.camera = Camera()

        self.load_map()
        pygame.display.set_caption("Test Game")

        self.characters = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        
        self.town1()

        self.player= Hero()
        self.player.image = pygame.image.load("images/sprite1.png")
        self.player.rect = pygame.Rect(320, 240, 16, 32)
        self.player.position = [320,240]
        self.player.image.convert()
        self.characters.add(self.player)

    def load_map(self):
        self.window = pygame.display.set_mode((640, 480), 0, 0)
        self.screen = pygame.display.get_surface()
        fullname = os.path.join('images', "map1.png")
        fullname = os.path.realpath(fullname)

        self.background = pygame.image.load(fullname)
        self.background.convert()


    def town1(self):
        self.house = Entity()
        self.house.image = pygame.image.load("images/house1.png")
        self.house.rect = self.house.image.get_rect()
        self.house.image.convert()
        self.house.position = (0,0)
        self.house.rect = pygame.Rect(0, 0, 64, 64)
        self.obstacles.add(self.house)

        self.house2 = Entity()
        self.house2.image = pygame.image.load("images/house1.png")
        self.house2.rect = self.house2.image.get_rect()
        self.house2.image.convert()
        self.house2.position = (132,0)
        self.house2.rect = pygame.Rect(132, 0, 64, 64)
        self.obstacles.add(self.house2)

        self.house3 = Entity()
        self.house3.image = pygame.image.load("images/house1.png")
        self.house3.rect = self.house3.image.get_rect()
        self.house3.image.convert()
        self.house3.position = (264,0)
        self.house3.rect = pygame.Rect(264, 0, 64, 64)
        self.obstacles.add(self.house3)


    def show(self):
        self.eventInput(pygame.event.get())
        
        self.screen = pygame.display.get_surface()
        self.screen.blit(self.background, (0, 0))

        self.camera.update(self.player)
        self.player.update(self.obstacles)

        for e in self.characters:
            e.update(self.obstacles)
            self.screen.blit(e.image, self.camera.apply(e))

        for e in self.obstacles:
            e.update(self.obstacles)
            self.screen.blit(e.image, self.camera.apply(e))

        pygame.display.update()

    def eventInput(self, events):
        for event in events: 
            if event.type == QUIT: 
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_LEFT:
                self.player.move_right()
                print("down")
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                self.player.move_left()
            elif event.type == KEYDOWN and event.key == K_UP:
                self.player.move_up()
            elif event.type == KEYDOWN and event.key == K_DOWN:
                self.player.move_down()
            elif event.type == KEYUP and (event.key == K_LEFT or event.key == K_RIGHT):
                self.player.horizontal_stop()
            elif event.type == KEYUP and (event.key == K_UP or event.key == K_DOWN):
                self.player.vertical_stop()
            elif event.type == KEYUP and event.key == K_SPACE:
                self.player.shoot()
                
                #missle = Missle()
                #missle.position = self.spaceShip.position
                #self.missles.append(missle)
            else: 
                print(event)

if __name__ == '__main__':
    test_game = TestGame()
    while True:
        clock = pygame.time.Clock()
        clock.tick(60)
        test_game.show()
        #main()