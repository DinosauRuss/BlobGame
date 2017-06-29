
from blobClassesV2 import *
from blobSettingsV2 import *
import os
import pygame as pg
import sys


class Game():
    def __init__(self, screen):
        self.clock = pg.time.Clock()
        self.fontName = pg.font.match_font(FONT_NAME)
        self.screen = screen
        self.program_running = True
        
    def new(self):
        self.loadData()

        # Create sprite groups
        self.all_sprites = pg.sprite.Group()
        self.blue_blobs = pg.sprite.Group()
        self.red_blobs = pg.sprite.Group()
        self.green_blobs = pg.sprite.Group()
        
        #Create sprites
        for i in range(15):
            # Create blobs
            bob = Blob()
            self.all_sprites.add(bob)
            self.blue_blobs.add(bob)
            # Place randomly around screen
            bob.pos = \
                (random.randrange(bob.radius, sWidth-bob.radius),\
                 random.randrange(bob.radius, sHeight-bob.radius))
            
            george = Blob(color=RED)
            self.all_sprites.add(george)
            self.red_blobs.add(george)
            george.pos = \
                (random.randrange(george.radius, sWidth-george.radius),\
                 random.randrange(george.radius, sHeight-george.radius))
            
            #~ bill = Blob(color=GREEN)
            #~ self.all_sprites.add(bill)
            #~ self.green_blobs.add(bill)
            #~ bill.pos = \
                #~ (random.randrange(bill.radius, sWidth-bill.radius),\
                 #~ random.randrange(bill.radius, sHeight-bill.radius))
                 
        #~ # Single testing blob         
        #~ self.bob = Blob(GREEN, (15,15), (-10,10))
        #~ self.all_sprites.add(self.bob)
        #~ self.bob.pos = sWidth/2, sHeight/2
        
        self.run()       
        
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            self.waitForEsc()
        
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.program_running = False
    
    def update(self):
        # run all sprites update functions
        self.all_sprites.update()
        self.checkBounds()
        
        # Blue blobs destroy red blobs
        br_collide = pg.sprite.groupcollide(self.blue_blobs, self.red_blobs,\
            False, True, pg.sprite.collide_circle)
        # Explostion animation
        for crash in  br_collide.values():
            expl = Explosion(crash[0].pos)
            self.all_sprites.add(expl)
        
    def draw(self):
        #draw graphics
        self.screen.fill(BLACK)
        
        #~ pos = (int(self.bob.target[0]), int(self.bob.target[1]))
        #~ pg.draw.circle(self.screen, RED, pos, 5)
        
        self.all_sprites.draw(self.screen)
        pg.display.flip()
    
    def drawText(self, text, size, color, x, y):
        # Draw some text to the screen
        font = pg.font.Font(self.fontName, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)
    
    def checkBounds(self):
        # Stay within screen bounds and \
        # slow vel away from boundary
        for i in self.all_sprites:
            if i.pos.x < 0 + (i.radius):
                i.pos.x = 0 + (i.radius)
                i.vel.x += 1
            if i.pos.x > sWidth - (i.radius):
                i.pos.x = sWidth - (i.radius)
                i.vel.x -= 1
            if i.pos.y < 0 + (i.radius):
                i.pos.y = 0 + (i.radius)
                i.vel.y += 1
            if i.pos.y > sHeight - (i.radius):
                i.pos.y = sHeight - (i.radius)
                i.vel.y -= 1
            
    def loadData(self):
        explosion_anim['red'] = []
        for i in range(9):
            filename = 'redExplosion0{}.png'.format(i)
            img = pg.image.load(os.path.join(\
                img_dir, filename)).convert_alpha()
            img = pg.transform.scale(img, (50,50))
            explosion_anim['red'].append(img)
    
    def waitForEsc(self):
        pressed = pg.key.get_pressed()
        if pressed[pg.K_ESCAPE]:
            self.playing = False
            self.program_running = False

def mainLoop():
    pg.init()
    os.environ['SDL_VIDEO_CENTERED'] = 'True'
    screen = pg.display.set_mode((sWidth, sHeight))
    pg.display.set_caption('Blobs Eating Blobs')
    
    game = Game(screen)
    while game.program_running:
        game.new()

    pg.quit()
    sys.exit()
    

if __name__ == '__main__':
    mainLoop()

