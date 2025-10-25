import pygame
import sys
pygame.init()

# layar
layar = pygame.display.set_mode((500, 400))
# waktu
clock = pygame.time.Clock()
jalan = True

player = pygame.Rect(100, 100, 50, 50)
heroes = pygame.Rect(300, 100, 50, 50)

while jalan:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      jalan = False
      pygame.quit()
      sys.exit()
        
  # background layar
  layar.fill("#ffffff")
  
  button = pygame.key.get_pressed()
  
  if button[pygame.K_LEFT]: player.x -= 5
  if button[pygame.K_RIGHT]: player.x += 5
  if button[pygame.K_UP]: player.y -= 5
  if button[pygame.K_DOWN]: player.y += 5
  
  
  # deteksi tabrakan/collision
  if player.colliderect(heroes):
    print("Woioooooooiiii!")
  
  pygame.draw.rect(layar, (0,0,255), player)
  pygame.draw.circle(layar, (255,0,0), heroes, 50)
    
  pygame.display.flip()
  clock.tick(60)

pygame.quit()