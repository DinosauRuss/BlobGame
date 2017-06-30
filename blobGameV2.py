
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
        self.colors = ['red', 'green', 'blue']
        self.lastPowerup = 0
        self.powerupDelay = 10000
        
    def new(self):
        self.loadData()

        # Create sprite groups
        self.all_sprites = pg.sprite.Group()
        self.blue_blobs = pg.sprite.Group()
        self.red_blobs = pg.sprite.Group()
        self.green_blobs = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        
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
            
            bill = Blob(color=GREEN)
            self.all_sprites.add(bill)
            self.green_blobs.add(bill)
            bill.pos = \
                (random.randrange(bill.radius, sWidth-bill.radius),\
                 random.randrange(bill.radius, sHeight-bill.radius))
        
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
            
            # Pause game with spacebar
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.waitForKey()
    
    def update(self):
        # run all sprites update functions
        self.all_sprites.update()
        self.powerups.update()
        self.checkBounds()
        
        # Blue blobs destroy red blobs
        br_collide = pg.sprite.groupcollide(self.blue_blobs, self.red_blobs,\
            False, True, pg.sprite.collide_circle)
        # Explostion animation
        for crash in  br_collide.values():
            expl = Explosion(crash[0].pos, 'red')
            self.all_sprites.add(expl)            
            
        # Red blobs destroy green blobs
        rg_collide = pg.sprite.groupcollide(self.red_blobs, self.green_blobs,\
            False, True, pg.sprite.collide_circle)
        for crash in  rg_collide.values():
            expl = Explosion(crash[0].pos, 'green')
            self.all_sprites.add(expl)
            
        # Green blobs destroy blue blobs
        rg_collide = pg.sprite.groupcollide(self.green_blobs, self.blue_blobs,\
            False, True, pg.sprite.collide_circle)
        for crash in  rg_collide.values():
            expl = Explosion(crash[0].pos, 'blue')
            self.all_sprites.add(expl)
        
        # Spawn powerup randomly
        now = pg.time.get_ticks()
        if now - self.lastPowerup > self.powerupDelay:
            self.lastPowerup = now
            self.powerupDelay = random.choice((20000, 40000, 60000))
            randLocation =\
                    (random.randrange(20, sWidth-20),\
                     random.randrange(20, sHeight-20))
            steven = Powerup(vect(randLocation), 'gold_coin')
            self.powerups.add(steven)
            
        # Touching powerup adds sprites of same color
        p_collide = pg.sprite.groupcollide(self.all_sprites, self.powerups, False, True)
        for blob in p_collide:
            for j in range(5):
                b = Blob(blob.color)
                self.all_sprites.add(b)
                b.pos = vect(random.randrange(20, sWidth-20),\
                         random.randrange(40, sHeight-20))
                if blob.color == RED:
                    self.red_blobs.add(b)
                elif blob.color == GREEN:
                    self.green_blobs.add(b)
                elif blob.color == BLUE:
                    self.blue_blobs.add(b)
        
    def draw(self):
        #draw graphics
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.powerups.draw(self.screen)
        pg.draw.line(self.screen, GREY, (0,25), (sWidth,20), 3)
        r = self.drawText('Reds: {:02d}'.format(len(self.red_blobs)), 25,\
            RED, 10, 5)
        g = self.drawText('Greens: {:02d}'.format(len(self.green_blobs)),\
            25, GREEN, r.width+15, 5)
        b = self.drawText('Blues: {:02d}'.format(len(self.blue_blobs)),\
            25, BLUE, r.width+g.width+20, 5)
        pg.display.flip()
    
    def drawText(self, text, size, color, x, y):
        # Draw some text to the screen
        font = pg.font.Font(self.fontName, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        self.screen.blit(text_surface, text_rect)
        return text_rect
    
    def checkBounds(self):
        # Stay within screen bounds and \
        # slow vel away from boundary
        for i in self.all_sprites:
            try:
                if i.pos.x < 0 + (i.radius):
                    i.pos.x = 0 + (i.radius)
                    i.vel.x += 1
                if i.pos.x > sWidth - (i.radius):
                    i.pos.x = sWidth - (i.radius)
                    i.vel.x -= 1
                if i.pos.y < 20 + (i.radius):
                    i.pos.y = 20 + (i.radius)
                    i.vel.y += 1
                if i.pos.y > sHeight - (i.radius):
                    i.pos.y = sHeight - (i.radius)
                    i.vel.y -= 1
            except:
                pass
    
    def scaleImg(self, image, maxWidth, maxHeight):
        # Scale images proportionally to a given width or height
        imgRect = image.get_rect()
        
        if maxWidth != None:
            if imgRect.width > maxWidth or imgRect.width < maxWidth:
                img = pg.transform.scale(image,\
                    (maxWidth, int((maxWidth*imgRect.height)/imgRect.width)))
                return img
        if maxHeight != None:
            if imgRect.height > maxHeight or imgRect.height < maxHeight:
                img = pg.transform.scale(image,\
                    (int((maxHeight*imgRect.width)/imgRect.height), maxHeight))
                return img
        return image

    def loadData(self):
        # Load colored explosion images into dict
        for color in self.colors:
            for i in range(9):
                filename = '{0}/{0}Explosion0{1}.png'.format(color, i)
                img = pg.image.load(os.path.join(\
                    img_dir, filename)).convert_alpha()
                #~ img = pg.transform.scale(img, (50,50))
                img = self.scaleImg(img, 50, 75)
                explosion_anim[color].append(img)
                
        # Load gold coin powerup images
        for i in range(6):
            filename = 'gold_{}.png'.format(i)
            img = pg.image.load(os.path.join(img_dir, filename)).convert_alpha()
            #~ img = pg.transform.scale(img, (75,75))
            img = self.scaleImg(img, None, 35)
            powerup_anim['gold_coin'].append(img)
    
    def waitForKey(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            self.waitForEsc()
            pg.time.delay(50)
            # Check for window close button
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.programRunning = False
                
                if event.type == pg.KEYUP:
                    waiting = False
    
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

