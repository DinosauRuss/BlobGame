import random

class Blob:

    def __init__(self,
                 color=(0, 0, 255),
                 x_boundary=800,
                 y_boundary=600,
                 size_range=(4,8),
                 move_range=(-3, 3)):
        self.color = color
        self.x = random.randint(0, x_boundary)
        self.y = random.randint(0, y_boundary)
        self.x_boundary = x_boundary
        self.y_boundary = y_boundary
        self.move_range = move_range
        self.size = random.randint(size_range[0], size_range[1])

    def move(self):
        '''move a random number of pixels each frame'''
        self.x += random.randint(self.move_range[0], self.move_range[1])
        self.y += random.randint(self.move_range[0], self.move_range[1])

    def check_bounds(self):
        '''don't let blobs leave boundary area'''
        if self.x < self.size:
            self.x = self.size
        elif self.x > (self.x_boundary - self.size):
            self.x = (self.x_boundary - self.size)

        if self.y <  self.size:
            self.y = self.size
        elif self.y > (self.y_boundary - self.size):
            self.y = (self.y_boundary - self.size)

    def __add__(self, other_blob):
        self.size += other_blob.size
        other_blob.size = 0




    
