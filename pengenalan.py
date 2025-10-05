import pygame
import math

# panggil plugin (module(grafik, audio, input))
pygame.init()

# membuat screen (layar)
screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption("Pengenalan PyGame")

# durasi tampil screen
running = True

clock = pygame.time.Clock()

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
  screen.fill("#7096FF")
  
  # objek
  # pygame.draw.circle(screen, ("#ffee56"), (250, 200), 100)
  # pygame.draw.polygon(screen, ("#5eff00"), [[300, 300], [100, 500], [200, 200]])
  # pygame.draw.rect(screen, ("#ff0000"), (100, 150, 200, 80))
  # pygame.draw.rect(screen, ("#ffffff"), (100, 230, 200, 80))
  pygame.draw.rect(screen, ("#FFC06D"), (80, 50, 10, 300))
  
  # animasi
  time = pygame.time.get_ticks() / 200
  flag_width = 200
  flag_height = 120
  start_x = 90
  start_y = 60
  
  for y in range(flag_height):
    # tentukan warna 
    if y < flag_height // 2:
      color = (255, 0, 0)
    else:
      color = (255, 255, 255)
    
    offset = int(10 * math.cos((y / 30) + time) ** 2)
    pygame.draw.line(screen, color, (start_x, start_y + y), (start_x + flag_width + offset, start_y + y))
  
  # update tampilan 
  pygame.display.flip()
  clock.tick(60)

pygame.quit()