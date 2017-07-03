
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
        
        self.winner = None
        self.winningFlag = False
        self.startTime = pg.time.get_ticks()
        
        self.colors = ['red', 'green', 'blue']
        self.lastCoin = 0
        self.coinDelay = 5000
        self.lastMelon = 0
        self.melonDelay = 1000
        
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
                
                # Remove entire blob group, for testing    
                if event.key == pg.K_b:
                    self.all_sprites.remove(self.blue_blobs)
                    self.blue_blobs.empty()
                if event.key == pg.K_g:
                    self.all_sprites.remove(self.green_blobs)
                    self.green_blobs.empty()
                if event.key == pg.K_r:
                    self.all_sprites.remove(self.red_blobs)
                    self.red_blobs.empty()
    
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
        
        # Spawn coins randomly
        self.lastCoin, self.coinDelay = self.spawnRandomPowerup(\
            'gold_coin', self.lastCoin, self.coinDelay, True, 20)
            
        # Spawn watermelons randomly
        self.lastMelon, self.melonDelay = self.spawnRandomPowerup(\
            'watermelon', self.lastMelon, self.melonDelay, False)
            
        # Touching powerup adds sprites of same color,
        # watermelon explodes on contact taking blob with it
        p_collide = pg.sprite.groupcollide(self.all_sprites, self.powerups,\
            False, True, pg.sprite.collide_circle)
        for blob, pUp in p_collide.items():
            if pUp[0].whichOne == 'gold_coin':
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
            if pUp[0].whichOne == 'watermelon':
                blob.kill()
                expl = Explosion(pUp[0].pos, 'watermelon')
                expl.frameRate = 30
                self.all_sprites.add(expl)
                
        self.checkForWinner()
    
    def spawnRandomPowerup(self, powerup, prev_spawn, delay, animate, *args):
        # Spawn powerup randomly
        now = pg.time.get_ticks()
        if now - prev_spawn > delay:
            prev_spawn = now
            delay = random.randrange(20000, 60000, 5000)
            
            # Don't let spawn onto current blob
            touching = True
            while touching:
                randLocation =\
                        (random.randrange(20, sWidth-20),\
                         random.randrange(20, sHeight-20))
                steven = Powerup(vect(randLocation), powerup, animate, *args)
                if pg.sprite.spritecollide(steven, self.all_sprites,\
                    False, pg.sprite.collide_circle):
                        
                    steven.kill()
                    continue
                touching = False
            self.powerups.add(steven)
            
        return prev_spawn, delay
        
    def draw(self):
        #draw graphics
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.powerups.draw(self.screen)
        
        # Draw 'scores' on screen
        pg.draw.line(self.screen, GREY, (0,25), (sWidth,25), 3)
        r = self.drawText('Reds: {:02d}'.format(len(self.red_blobs)), 25,\
            RED, 10, 5)
        g = self.drawText('Greens: {:02d}'.format(len(self.green_blobs)),\
            25, GREEN, r.width+15, 5)
        b = self.drawText('Blues: {:02d}'.format(len(self.blue_blobs)),\
            25, BLUE, r.width+g.width+20, 5)
            
        self.drawText(self.timer(), 25, WHITE, sWidth-10, 5, 'topright')
            
        pg.display.flip()
    
    def drawText(self, text, size, color, x, y, where='topleft'):
        # Draw some text to the screen
        font = pg.font.Font(self.fontName, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        
        if where == 'topright':
            text_rect.topright = (x,y)
        elif where == 'center':
            text_rect.center = (x,y)
        else:
            text_rect.topleft = (x,y)
            
        self.screen.blit(text_surface, text_rect)
        return text_rect
    
    def timer(self):
        now = pg.time.get_ticks()
        secs = int((now - self.startTime)/1000)
        seconds = '{:02d}'.format(secs % 60)
        minutes = '{:02d}'.format(secs // 60)
        return '{}:{}'.format(minutes, seconds)
    
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
                if i.pos.y < 25 + (i.radius):
                    i.pos.y = 25 + (i.radius)
                    i.vel.y += 1
                if i.pos.y > sHeight - (i.radius):
                    i.pos.y = sHeight - (i.radius)
                    i.vel.y -= 1
            except:
                pass
    
    def checkForWinner(self):
        # Check for winning color
        zeros = 0
        blobs = {'Blues': self.blue_blobs, 
                  'Greens': self.green_blobs, 
                  'Reds': self.red_blobs}
        for k,v in blobs.items():
            if len(v) == 0:
                zeros += 1
        
        if zeros == 2:
            for k, v in blobs.items():
                if len(v) != 0:
                    self.winner = k
            self.winningFlag = True
            self.playing = False
            self.program_running = False
    
    def showEndScreen(self):
        # Display when winning color emerges
        winner = self.drawText('{} win!'.format(self.winner), 75, GREY,\
            sWidth/2, sHeight/2, 'center')
                        
        pg.display.flip()
        self.waitForKey()
    
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
            filename = 'powerups/coin/gold_{}.png'.format(i)
            img = pg.image.load(os.path.join(img_dir, filename)).convert_alpha()
            img = self.scaleImg(img, None, 35)
            powerup_anim['gold_coin'].append(img)
            
        # Load watermelon explosion
        for i in range(10):
            filename = 'powerups/watermelon/watermelon_{}.png'.format(i)
            img = pg.image.load(os.path.join(img_dir, filename)).convert_alpha()
            #~ img = self.scaleImg(img, None, 35)
            explosion_anim['watermelon'].append(img)
        
        # Watermelon powerup image
        powerup_anim['watermelon'].append(explosion_anim['watermelon'][0])
            
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
                
                if event.type == pg.KEYDOWN:
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
    if game.winningFlag == True:
        game.showEndScreen()

    pg.quit()
    sys.exit()
    

if __name__ == '__main__':
    mainLoop()

