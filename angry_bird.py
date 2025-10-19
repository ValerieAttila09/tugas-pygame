import pygame
import random

pygame.init()
X = 720
Y = 480
size = width, height = X, Y
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


bg_image = pygame.image.load("images/bg_angry_bird.png").convert()
bg_image = pygame.transform.scale(bg_image, (X, Y))

# angry bird
image_bird = pygame.image.load('images/angry_bird.png')
DEFAULT_IMAGE_SIZE = (80, 80)
image_bird = pygame.transform.scale(image_bird, DEFAULT_IMAGE_SIZE)
DEFAULT_IMAGE_POSITION = (200, 200)
rect = image_bird.get_rect()
rect.center = (200, 300)

# king
image_king = pygame.image.load('images/king_pig.png')
DEFAULT_IMAGE_SIZE = (100, 125)
image_king = pygame.transform.scale(image_king, DEFAULT_IMAGE_SIZE)
DEFAULT_IMAGE_POSITION = (500, 200)
rect_king = image_king.get_rect()
rect_king.center = (500, 300)

# boom effect
image_boom = pygame.image.load('images/boom.png')
DEFAULT_IMAGE_SIZE = (400, 400)
image_boom = pygame.transform.scale(image_boom, DEFAULT_IMAGE_SIZE)
DEFAULT_IMAGE_POSITION = (500, 200)
rect_boom = image_boom.get_rect()
rect_boom.center = (500, 300)

running = False
score = 0
boom_timer = 0

def movement(player):
  button = pygame.key.get_pressed()
  if button[pygame.K_LEFT] and player.x > 0: player.x -= 5
  if button[pygame.K_RIGHT] and player.x < X - player.width: player.x += 5
  if button[pygame.K_UP] and player.y > 0: player.y -= 5
  if button[pygame.K_DOWN] and player.y < Y - player.height: player.y += 5 

while not running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = True
   
   
  screen.blit(bg_image, (0, 0))
  screen.blit(image_bird, rect)
  
  movement(rect)
  
  if rect.colliderect(rect_king):
    screen.blit(image_boom, rect_boom)
    boom_timer = 45
    score += 1
    rect_king.x = random.randint(100, 500)
    rect_king.y = random.randint(100, 400)
    rect_boom.x = rect_king.x - 125
    rect_boom.y = rect_king.y - 125
  else:
    screen.blit(image_king, rect_king)
  
  if boom_timer > 0:
    screen.blit(image_boom, rect_boom)
    boom_timer -= 1
  else:
    screen.blit(image_king, rect_king)
  
  font = pygame.font.Font(None, 30)
  text = font.render(f"Score: {score}", True, (255, 255, 255))
  screen.blit(text, (10, 10))
  
  pygame.display.flip()
  clock.tick(60)