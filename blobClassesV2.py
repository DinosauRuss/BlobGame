
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
    def __init__(self, center):
        super().__init__()
        
        self.image = explosion_anim['frames'][0]
        self.rect = self.image.get_rect()
        #~ self.rect.center = center
        self.pos = center
        self.rect.center = self.pos
        self.radius = 0
        self.frame = 0
        self.last_update = 0
        self.frameRate = 25
    
    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frameRate:
            self.frame += 1
            self.last_update = now
            if self.frame == len(explosion_anim['frames']):
                self.kill()
            else:
                currentPos = self.rect.center
                self.image = explosion_anim['frames'][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = currentPos
        
        
