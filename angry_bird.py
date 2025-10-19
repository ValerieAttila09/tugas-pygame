import pygame

pygame.init()
X = 720
Y = 480
size = width, height = X, Y
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


bg_image = pygame.image.load("images/bg_angry_bird.png").convert()
bg_image = pygame.transform.scale(bg_image, (X, Y))

image_bird = pygame.image.load('images/angry_bird.png')
DEFAULT_IMAGE_SIZE = (80, 80)
image_bird = pygame.transform.scale(image_bird, DEFAULT_IMAGE_SIZE)
DEFAULT_IMAGE_POSITION = (200, 200)

rect = image_bird.get_rect()
rect.center = (200, 300)

image_king = pygame.image.load('images/king_pig.png')
DEFAULT_IMAGE_SIZE = (100, 125)
image_king = pygame.transform.scale(image_king, DEFAULT_IMAGE_SIZE)
DEFAULT_IMAGE_POSITION = (500, 200)

rect_king = image_king.get_rect()
rect_king.center = (500, 300)

image_boom = pygame.image.load('images/boom.png')
DEFAULT_IMAGE_SIZE = (400, 400)
image_boom = pygame.transform.scale(image_boom, DEFAULT_IMAGE_SIZE)
DEFAULT_IMAGE_POSITION = (500, 200)

rect_boom = image_boom.get_rect()
rect_boom.center = (500, 300)

running = False


def movement(player):
  button = pygame.key.get_pressed()
  if button[pygame.K_LEFT]: player.x -= 5
  if button[pygame.K_RIGHT]: player.x += 5
  if button[pygame.K_UP]: player.y -= 5
  if button[pygame.K_DOWN]: player.y += 5 

while not running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = True
   
   
  screen.blit(bg_image, (0, 0))
  screen.blit(image_bird, rect)
  
  movement(rect)
  
  if rect.colliderect(rect_king):
    screen.blit(image_boom, rect_boom)
  else:
    screen.blit(image_king, rect_king)
    
  
  
  pygame.display.flip()
  clock.tick(60)