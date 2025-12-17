
# core game loop
# input
# update
# draw

# why? what? how?

#imports
import math
import random
import sys
import pygame as pg
from settings import *
from sprites import *
from os import path
from utils import *

# overview - CONCISE AND INFORMATIVE
# This class handles the main game functionality
class Game:
   def __init__(self):
      pg.init()
      self.clock = pg.time.Clock()
      self.screen = pg.display.set_mode((WIDTH, HEIGHT))
      pg.display.set_caption("Super Star Runner")
      self.playing = True
      self.bg_speed = 4
   
   # sets up a game folder directory path using the current folder containing THIS file
   # give the Game class a map property which uses the Map class to parse the level1.txt file
   def load_data(self):
      self.game_folder = path.dirname(__file__)
      self.map = Map(path.join(self.game_folder, 'level1.txt'))
      # load background image
      bg_path = path.join(self.game_folder, "images", "bg_image.png")

      # load and convert for better performance
      self.bg_image = pg.image.load(bg_path).convert()
      # scale to fit screen
      self.bg_image = pg.transform.scale(self.bg_image, (WIDTH, HEIGHT))

      # set initial background scroll values
      self.bg_scroll = 0       
      self.bg_speed = 9 
      

   # new game setup
   def new(self):
      self.player = None
      self.load_data()

      # create sprite groups
      self.all_sprites = pg.sprite.Group()
      self.all_mobs = pg.sprite.Group()
      self.all_coins = pg.sprite.Group()
      self.all_walls = pg.sprite.Group()
      self.all_obstacles = pg.sprite.Group()
      self.all_heal_tomatoes = pg.sprite.Group()
      self.all_empty = pg.sprite.Group()

      # create objects wbased on the map data
      for row, tiles in enumerate(self.map.data):
         for col, tile in enumerate(tiles):
               if tile == '1':
                  Wall(self, col, row, "")
               elif tile == 'P':
                  self.player = Player(self, col, row)
               elif tile == 'O':
                     Obstacle(self, col, row, "")
               elif tile == 'C':
                  Coin(self, col, row)

               elif tile == 'H':
                  heal_tomato(self, col, row)
               elif tile in ('.', ' '): 
                  Empty(self, col, row)
                  



      
   # core game loop
   def run(self):
      while self.playing == True:
         # delta time
         if self.player.health > 0:
            self.dt = self.clock.tick(FPS) / 1000
         else:
            self.dt = 0
         
         # input
         self.events()
         # process
         self.update()
         # output
         self.draw()
      pg.quit()

# input handling
   def events(self):
      for event in pg.event.get():
        if event.type == pg.QUIT:
         #  print("this is happening")
          self.playing = False
        if event.type == pg.MOUSEBUTTONDOWN:
           print("I can get input from mousey mouse mouse mousekerson")


# update game state
   def update(self):

      self.all_sprites.update()
      seconds = pg.time.get_ticks() // 1000
      countdown = 0 
      self.time = countdown + seconds
      if self.time >= 15:
         self.bg_speed = 15   # increase speed after 15 seconds
      if self.time >= 30:
         self.bg_speed = 20   # increase speed after 30 seconds
      if self.time >= 45:
         self.bg_speed = 25   # increase speed after 45 seconds
      if self.time >= 60:
         self.bg_speed = 30   # increase speed after 60 seconds 
              
      if self.player.health < 0:

         self.bg_image = pg.image.load(path.join(self.game_folder, "images", "game_over.png")).convert()
         self.bg_image = pg.transform.scale(self.bg_image, (WIDTH, HEIGHT))
         #pauses timer
         self.dt = 0
         #pauses timer
         
         #obstacles become opaque
         for obstacle in self.all_obstacles:
            obstacle.image.set_alpha(0)
         for heal_tomato in self.all_heal_tomatoes:
            heal_tomato.image.set_alpha(0)

         


# draw everything on the screen
   def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surface.blit(text_surface, text_rect)
        
   # draw function
   def draw(self):
         # Draw scrolling background 
         #https://www.geeksforgeeks.org/python/creating-a-scrolling-background-in-pygame/
         # scroll plus speed modulas width of image
         self.bg_scroll = (self.bg_scroll + self.bg_speed) % self.bg_image.get_width()
         # draw two images to create a seamless loop
         self.screen.blit(self.bg_image, (-self.bg_scroll, 0))
         # draw second image next to first
         self.screen.blit(self.bg_image, (self.bg_image.get_width() - self.bg_scroll, 0))
         
         # Draw sprites on top of bg
         self.all_sprites.draw(self.screen)
         
         # Draw text
         if self.player.health > 0:
            
            self.draw_text(self.screen, "TIME: " + str(self.time), 24, BLACK, 500, 100)
            self.draw_text(self.screen, "Health: " + str(self.player.health), 24, RED, 70, 10)
            self.draw_text(self.screen, "Get tomatoes if your running low on health and dodge the boxes!", 20, BLACK, 500, 150)
      
         
         # Update display
         pg.display.flip()
      

      

# entry point
if __name__ == "__main__":
#    creating an instance or instantiating the Game class
   g = Game()
   g.new()
   g.run()
