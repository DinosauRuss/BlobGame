
from blobSettingsV2 import *
import math
import pygame as pg
import random
vect = pg.math.Vector2

class Blob(pg.sprite.Sprite):
    def __init__(self,
                 color=(0, 0, 255),
                 radius_range=(4,8),
                 move_range=50,
                 speed=5):
                     
        super().__init__()
        
        self.color = color
        self.radius = random.randint(*radius_range)
        self.move_range = move_range
        
        self.pos = vect(0,0)
        self.vel = vect(speed,0).rotate(random.uniform(0,360))
        self.maxSpeed = speed
        self.acc = (0,0)
        
        self.lastMove = 0
        self.target = vect(random.randint(0,800), random.randint(0,600))
        
        self.image = pg.Surface((self.radius*2, self.radius*2))
        self.image.set_colorkey(self.image.get_at((1,1)))
        self.rect = self.image.get_rect()
        pg.draw.circle(self.image, self.color, self.rect.center, self.radius)
        
    def move(self):
        now = pg.time.get_ticks()
        if now - self.lastMove > 1000:
            self.lastMove = now
            # New target within movement radius of blob
            self.target = (random.randint(int(self.pos.x)-self.move_range, int(self.pos.x)+self.move_range),\
                           random.randint(int(self.pos.y)-self.move_range, int(self.pos.y)+self.move_range))
            
        self.acc = (self.target - self.pos).normalize()*.25
        self.vel += self.acc
        self.pos += self.vel
        if self.vel.length() >= self.maxSpeed:
            self.vel.scale_to_length(self.maxSpeed)
        self.rect.center = self.pos
        
    def update(self):
        self.move()
    
class Explosion(pg.sprite.Sprite):
    def __init__(self, center, color):
        super().__init__()
        
        self.color = color
        self.image = explosion_anim[self.color][0]
        self.rect = self.image.get_rect()
        self.pos = center
        self.rect.center = self.pos
        self.radius =0
        self.currentFrame = 0
        self.last_update = 0
        self.frameRate = 50
    
    def update(self):
        animate(self, explosion_anim, self.color, True)
        
class Powerup(pg.sprite.Sprite):
    def __init__(self, loc, whichOne, animate, radius=25):
        super().__init__()
        
        self.whichOne = whichOne
        self.animate = animate
        self.image = powerup_anim[self.whichOne][0]
        self.rect = self.image.get_rect()
        self.pos = loc
        self.rect.center = self.pos
        self.radius = radius
        self.currentFrame = 0
        self.last_update = 0
        self.frameRate = 100

    def update(self):
        if self.animate == True:
            animate(self, powerup_anim, self.whichOne)
        

def animate(sprite, dictionary, whichList, delete=False):
    now = pg.time.get_ticks()
    if now - sprite.last_update > sprite.frameRate:
        sprite.last_update = now
        sprite.currentFrame += 1
        if sprite.currentFrame == len(dictionary[whichList]):
            if delete == True:
                sprite.kill()
        sprite.currentFrame %= (len(dictionary[whichList]))
        currentPos = sprite.rect.center
        sprite.image = dictionary[whichList][sprite.currentFrame]
        sprite.rect = sprite.image.get_rect()
        sprite.rect.center = currentPos
        
