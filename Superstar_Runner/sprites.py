

# The sprites module contains all the sprites
# Sprites include: player, mob - moving object


import os
import pygame as pg
from pygame.sprite import Sprite
from settings import *
from utils import Cooldown
from random import randint
vec = pg.math.Vector2

#https://python-forum.io/thread-406.html
# Animated Player Sprite
class Player(Sprite):
    # Initialize the player sprite
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        Sprite.__init__(self, self.groups)
        self.game = game
        # Load animation frames
        self.load_frames()
        self.image = self.frames[0]
        self.current_frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 100
        # Set up player properties
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE[0]
        self.speed = 250
        self.health = 100
        self.coins = 0
        self.cd = Cooldown(1000)
        # Get player input
    def get_keys(self):
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.vel.y = -self.speed*self.game.dt
            # self.rect.y -= self.speed
            # self.bullet_direction = "up"
        if keys[pg.K_a]:
            self.vel.x = -self.speed*self.game.dt
            # self.rect.x -= self.speed
            # self.bullet_direction = "left"
        if keys[pg.K_s]:
            self.vel.y = self.speed*self.game.dt
            # self.rect.y += self.speed
            # self.bullet_direction = "down"  
        if keys[pg.K_d]:
            self.vel.x = self.speed*self.game.dt
            # self.rect.x += self.speed
            # self.bullet_direction = "right"
        # accounting for diagonal
        if self.vel[0] != 0 and self.vel[1] != 0:
            self.vel *= 0.7071

    # Handle collisions with walls
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                print(self.pos)
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    # Load animation frames from files
    def load_frames(self):
        self.frames = []
        base_folder = os.path.dirname(__file__)  
        image_folder = os.path.join(base_folder, "images")
        # Load two frames for animation
        for i in range(0,2):
            img_path = os.path.join(image_folder, f"player_frame_{i}.png")
            img = pg.image.load(img_path).convert_alpha()
            img = pg.transform.scale(img, TILESIZE)
            self.frames.append(img)
    # Scale image to fit tile size
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
    # Scale images to fit tile size            
    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits: 
            if str(hits[0].__class__.__name__) == "Mob":
                if self.cd.ready():
                    self.health -= 10
                    self.cd.start()
                print("Ouch!")
            if str(hits[0].__class__.__name__) == "Coin":
                self.coins += 1
                print(self.coins)
    # Update player state
    def update(self):
        self.get_keys()
        self.pos += self.vel
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')
        self.animate()
        self.collide_with_stuff(self.game.all_mobs, False)
        self.collide_with_stuff(self.game.all_coins, True)
        # print(self.cd.ready())
        
# Enemy Mob Sprite
class Mob(Sprite):
    # Initialize the mob sprite
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface(TILESIZE)
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vel = vec(1,1)
        self.pos = vec(x,y)*TILESIZE[0]
        # self.rect.x = x * TILESIZE[0]
        # self.rect.y = y * TILESIZE[1]
        self.speed = 3
        print(self.pos)
    # Handle collisions with walls
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                # print(self.pos)
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                # self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                # self.vel.y = 0
                self.rect.y = self.pos.y
    # Update mob state
    def update(self):
        # mob behavior
        if self.game.player.pos.x > self.pos.x:
            self.vel.x = 1
        else:
            self.vel.x = -1
            # print("I don't need to chase the player x")
        if self.game.player.pos.y > self.pos.y:
            self.vel.y = 1
        else:
            self.vel.y = -1
            # print("I don't need to chase the player x")
        self.pos += self.vel * self.speed
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')

# Coin Sprite
class Coin(Sprite):
    # Initialize the coin sprite
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface(TILESIZE)
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE[0]
        self.rect.y = y *TILESIZE[1]
        # coin behavior
        pass

# Wall Sprite
class Wall(Sprite):
    # Initialize the wall sprite
    def __init__(self, game, x, y, state):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface(TILESIZE)
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.x = x*TILESIZE[0]
        self.rect.y = y*TILESIZE[1]
        self.state = state
        # print("wall created at", str(self.rect.x), str(self.rect.y))
    # Update wall state
    def update(self):
        if self.state == "moving":
            self.rect.x += 1
        elif self.state == "moveable":
            hits = pg.sprites.collide_rect(self.rect, self.game.player.rect)
            if hits:
                print("wall was encountered by the player.")
# Pew_Pew Sprite
class Pew_Pew(Sprite):
    # Initialize the Pew_Pew sprite
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((16, 16))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.vel = vec(1,1)
        self.pos = vec(x,y)*TILESIZE[0]
        self.speed = 5
        print(self.pos)
    # Update Pew_Pew state
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                # print(self.pos)
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                # self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                # self.vel.y = 0
                self.rect.y = self.pos.y
class Obstacle(Sprite):
    # Initialize the wall sprite
    def __init__(self, game, x, y, state):
        self.groups = game.all_sprites, game.all_obstacles
        Sprite.__init__(self, self.groups)
        self.game = game
        #Scales and loads obstacle image
        image_path = os.path.join(self.game.game_folder, "images", "obstacle.png")
        self.image = pg.image.load(image_path).convert_alpha()
        self.image = pg.transform.scale(self.image, TILESIZE)
        
        self.rect = self.image.get_rect()
        self.rect.x = x*TILESIZE[0]
        self.rect.y = y*TILESIZE[1]
        self.state = state

    def update(self):
        if self.state == "moving":
            self.rect.x += 1
        elif self.state == "moveable":
            hits = pg.sprites.collide_rect(self.rect, self.game.player.rect)
            if hits:
                print("obstacle was encountered by the player.")