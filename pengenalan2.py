import pygame
import sys

pygame.init()

# ukuran layar

lebar, tinggi = 600, 400
layar = pygame.display.set_mode((lebar, tinggi))
pygame.display.set_caption("Move Object")

# warna
putih = (255, 255, 255)
biru = (0, 128, 255)

clock = pygame.time.Clock()

# perulangan
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
  
  # ambil posisi mouse
  x, y = pygame.mouse.get_pos() # ambil posisi kursor
  
  # background layar
  layar.fill(putih)
  
  # object
  pygame.draw.circle(layar, biru, (x, y), (50))
  
  pygame.display.flip()
  clock.tick(60)