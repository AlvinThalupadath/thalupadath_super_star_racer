
# core game loop
# input
# update
# draw

# why? what? how?

import math
import random
import sys
import pygame as pg
from Game.settings import *
from Game.sprites import *
from os import path
from Game.utils import *

# overview - CONCISE AND INFORMATIVE
class Game:
   def __init__(self):
      pg.init()
      self.clock = pg.time.Clock()
      self.screen = pg.display.set_mode((WIDTH, HEIGHT))
      pg.display.set_caption("Alvin's awesome game!!!!!")
      self.playing = True
   
   # sets up a game folder directory path using the current folder containing THIS file
   # give the Game class a map property which uses the Map class to parse the level1.txt file
   def load_data(self):
      self.game_folder = path.dirname(__file__)
      self.map = Map(path.join(self.game_folder, 'level1.txt'))

   def new(self):
      self.player = None
      self.load_data()

      self.all_sprites = pg.sprite.Group()
      self.all_mobs = pg.sprite.Group()
      self.all_coins = pg.sprite.Group()
      self.all_walls = pg.sprite.Group()

      for row, tiles in enumerate(self.map.data):
         for col, tile in enumerate(tiles):
               if tile == '1':
                  Wall(self, col, row, "")
               elif tile == 'C':
                  Coin(self, col, row)
               elif tile == 'P':
                  self.player = Player(self, col, row)
               elif tile == 'M':
                  Mob(self, col, row)
     
     
   def run(self):
      while self.playing == True:
         self.dt = self.clock.tick(FPS) / 1000
         # input
         self.events()
         # process
         self.update()
         # output
         self.draw()
      pg.quit()

   def events(self):
      for event in pg.event.get():
        if event.type == pg.QUIT:
         #  print("this is happening")
          self.playing = False
        if event.type == pg.MOUSEBUTTONDOWN:
           print("I can get input from mousey mouse mouse mousekerson")
   def update(self):

      self.all_sprites.update()
      seconds = pg.time.get_ticks() // 1000
      countdown = 10
      self.time = countdown - seconds


   def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surface.blit(text_surface, text_rect)
   def draw(self):
      self.screen.fill(WHITE)
      if self.player:
         self.draw_text(self.screen, str(self.player.health), 24, BLACK, 100, 100)
         self.draw_text(self.screen, str(self.player.coins), 24, BLACK, 400, 100)
      self.draw_text(self.screen, str(self.time), 24, BLACK, 500, 100)
      self.all_sprites.draw(self.screen)
      pg.display.flip()
      self.all_sprites.draw(self.screen)


if __name__ == "__main__":
#    creating an instance or instantiating the Game class
   g = Game()
   g.new()
   g.run()
