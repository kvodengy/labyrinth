import pygame

FPS = pygame.time.Clock()
win_width = 1280
win_height = 665
p_size = 50


window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Лабіринт")

class Settings():
    def __init__(self, image, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Settings):
    def __init__(self, image, x, y, w, h, s):
        super().__init__(image, x, y, w, h)
        self.speed = s
        self.flipped_image = pygame.transform.flip(self.image, True, False)
        self.no_flip_image = self.image
        self.flip = True

    def move(self):
        if self.flip:
            self.image = self.no_flip_image
        else:
            self.image = self.flipped_image
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.y>0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y<win_height-self.rect.height:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT] and self.rect.x>0:
            self.rect.x -= self.speed
            self.flip = False
        if keys[pygame.K_RIGHT] and self.rect.x<win_width-self.rect.width:
            self.rect.x += self.speed 
            self.flip = True
    def crash(self, l):
        for w in l:
            if self.rect.colliderect(w.rect):
                return True
            else:
                return False


class Enemy(Player):
    def __init__(self, image, x, y, w, h, s):
        super().__init__(image, x, y, w, h, s)
        self.direction = True #right

    def move(self, x1, x2):
        if self.rect.x<x1:
            self.direction = True
        elif self.rect.x>x2:
            self.direction = False

        if self.direction:
            self.image = self.no_flip_image
            self.rect.x += self.speed
        else:
            self.image = self.flipped_image
            self.rect.x -= self.speed

class Wall:
    def __init__ (self, x,y,w,h, color):
        self.rect = pygame.Rect(x,y,w,h)
        self.color = color
    def draw(self):
        pygame.draw.rect(window ,self.color, self.rect)
        
        
        


bg = Settings("background.png", 0, 0, win_width, win_height)
p1 = Player("sprite1.png", 0, win_height//2, p_size, p_size, 3)
enemy = Enemy("sprite2.png", win_width//1.3, win_height//1.7, p_size*3, p_size*3, 4)
gold = Settings("gold.png", win_width//1.15, win_height//1.2, p_size*1.5, p_size*1.5)
walls = [
    Wall(win_width//4,win_height//8, win_width//2, 5, (0,200,255)),
    Wall(win_width//4,win_height//1.1, win_width//2, 5, (0,200,255)),
    Wall(win_width//3,win_height//1.27, win_width//2.97, 5, (0,200,255)),
    Wall(win_width//4,win_height//8, 5, win_height//3.5, (0,200,255)),
    Wall(win_width//4,win_height//1.8, 5, win_height//2.8, (0,200,255)),
    Wall(win_width//2.5,win_height//1.5, win_width//5.5, 5, (0,200,255)),
    Wall(win_width//3,win_height//1.8, 5, win_width//8.1, (0,200,255)),
    Wall(win_width//3,win_height//1.8, win_width//5.5, 5, (0,200,255)),
    Wall(win_width//4,win_height//2.5, win_width//5.5, 5, (0,200,255)),
    Wall(win_width//1.34,win_height//8, 5, win_height//3.5, (0,200,255)),
    Wall(win_width//1.34,win_height//1.8, 5, win_height//2.8, (0,200,255)),
    Wall(win_width//3,win_height//3.7, win_width//5.5, 5, (0,200,255)),
    Wall(win_width//1.95,win_height//3.7, 5, win_width//6.5, (0,200,255)),
    Wall(win_width//1.5,win_height//1.5, 5, win_width//15, (0,200,255)),
    Wall(win_width//1.5,win_height//3.5, 5, win_width//15, (0,200,255)),
    Wall(win_width//1.7,win_height//7.5, 5, win_width//15, (0,200,255)),
    Wall(win_width//1.73,win_height//1.8, 5, win_width//17, (0,200,255)),
    Wall(win_width//1.95,win_height//2.45, win_width//4.2, 5, (0,200,255)),
    Wall(win_width//1.73,win_height//1.8, win_width//5.8, 5, (0,200,255))

]    

game = True

pygame.mixer.init()
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play()

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    bg.draw()
    p1.move()
    p1.draw()
    for w in walls:
        w.draw()
        if p1.rect.colliderect(w.rect):
            p1 = Player("sprite1.png", 0, win_height//2, p_size, p_size, 3)
    enemy.move(win_width//1.3, win_width//1.12)
    enemy.draw()
    gold.draw()
    pygame.display.flip()
    FPS.tick(40)