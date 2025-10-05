import pygame
import math

pygame.init()

X, Y = 900, 600

screen = pygame.display.set_mode((X, Y))
pygame.display.set_caption('Display Image')
image = pygame.image.load("images/building3.jpg").convert()
image = pygame.transform.scale(image, (X, Y))
running = True

clock = pygame.time.Clock()

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
      
  screen.blit(image, (0, 0))
  time = pygame.time.get_ticks() / 200
  
  # bendera 1
  pygame.draw.rect(screen, ("#FFC06D"), (111, 10, 4, 189))
  
  flag_width1 = 120
  flag_height1 = 70
  start_x1 = 115
  start_y1 = 10
  
  for y in range(flag_height1):
    if y < flag_height1 // 2:
      color = (255, 0, 0)
    else:
      color = (255, 255, 255)
    
    offset = int(5 * math.cos((y / 15) + time) * 2)
    pygame.draw.line(screen, color, (start_x1, start_y1 + y), (start_x1 + flag_width1 + offset, start_y1 + y))
  
  # bendera 2 (Belanda)
  pygame.draw.rect(screen, ("#FFC06D"), (420, 30, 4, 189))
  flag_width2 = 120
  flag_height2 = 70
  start_x2 = 424
  start_y2 = 30

  for y in range(flag_height2):
    if y < flag_height2 // 3:
      color = (255, 0, 0)
    elif y < 2 * flag_height2 // 3:
      color = (255, 255, 255)
    else:
      color = (0, 0, 255)
    offset = int(5 * math.cos((y / 15) + time) * 2)
    pygame.draw.line(screen, color, (start_x2, start_y2 + y), (start_x2 + flag_width2 + offset, start_y2 + y))

  # bendera 3 
  pygame.draw.rect(screen, ("#FFC06D"), (711, 60, 4, 189))
  flag_width3 = 120
  flag_height3 = 70
  start_x3 = 715
  start_y3 = 60

  for y in range(flag_height3):
    if y < flag_height3 // 3:
      color = (255, 255, 255)
    elif y < 2 * flag_height3 // 3:
      color = (0, 0, 255)
    else:
      color = (255, 0, 0)         
    offset = int(5 * math.cos((y / 15) + time) * 2)
    pygame.draw.line(screen, color, (start_x3, start_y3 + y), (start_x3 + flag_width3 + offset, start_y3 + y))

  pygame.display.flip()
  clock.tick(60)

pygame.quit()