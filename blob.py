import pygame, random, math
from blobber import Blob

width = 800
height = 600
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)

game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Blob World')
clock = pygame.time.Clock()

class BlueBlob(Blob):
    def __init__(self, x_boundary, y_boundary):
        super().__init__(blue, x_boundary, y_boundary)

class RedBlob(Blob):
    def __init__(self, x_boundary, y_boundary):
        super().__init__(red, x_boundary, y_boundary)

class GreenBlob(Blob):
    def __init__(self, x_boundary, y_boundary):
        super().__init__(green, x_boundary, y_boundary)

def is_touching(b1, b2):
    '''determine if 2 blobs are 'touching' each other'''
    
    distance = math.sqrt(((b1.x-b2.x)**2) + ((b1.y-b2.y)**2))
    return distance < (b1.size + b2.size)

def handle_collision(dict1, dict2):
    for id1, blob1 in dict1.copy().items():
        for id, blob in dict2.copy().items():
            if is_touching(blob1, blob):
                blob1 + blob
                del dict2[id]
    
def draw_environment(list_of_blobs):
    game_display.fill((0,0,0))

    reds, greens, blues = list_of_blobs
    handle_collision(reds, greens)
    handle_collision(blues, reds)
    handle_collision(greens, blues)
    
    # draw blobs on the screen
    for blobContainer in list_of_blobs:
        for id in blobContainer:
            blob = blobContainer[id]
            pygame.draw.circle(game_display, blob.color, [blob.x, blob.y], blob.size)
            blob.move()
            blob.check_bounds()
            
    pygame.display.update()


def main():
    # generate blobs
    red_blobs = dict(enumerate([(RedBlob(width, height)) for i in range(10)]))
    blue_blobs = dict(enumerate([(BlueBlob(width, height)) for i in range(10)]))
    green_blobs = dict(enumerate([(GreenBlob(width, height)) for i in range(10)]))
    blobs_list = [red_blobs, green_blobs, blue_blobs] # list containg the blob dictionaries
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        draw_environment(blobs_list)
        clock.tick(30)


if __name__ == '__main__':
    main()



        
            
