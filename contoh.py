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

x, y = 100, 100
radius = 50
mouse_click = False

warna_kotak = "#ff6528"

x_kotak, y_kotak = 300, 200
lebar_kotak, tinggi_kotak = 100, 100

clock = pygame.time.Clock()

def lingkaran_kena_kotak(cx, cy, r, rx, ry, rw, rh):
    # cari titik terdekat di kotak ke pusat lingkaran
    closest_x = max(rx, min(cx, rx + rw))
    closest_y = max(ry, min(cy, ry + rh))
    # hitung jarak ke pusat lingkaran
    distance = ((cx - closest_x) ** 2 + (cy - closest_y) ** 2) ** 0.5
    return distance < r

# perulangan
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            # cek apakah mouse di dalam lingkaran
            if (mx - x) ** 2 + (my - y) ** 2 <= radius ** 2:
                mouse_click = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_click = False

        if event.type == pygame.MOUSEMOTION and mouse_click:
            x, y = event.pos
    
    # background layar
    layar.fill(putih)
    
    # object
    pygame.draw.circle(layar, biru, (x, y), radius)
    
    if lingkaran_kena_kotak(x, y, radius, x_kotak, y_kotak, lebar_kotak, tinggi_kotak):
        warna_kotak = "#000000"
    else:
        warna_kotak = "#ff6528"
    
    pygame.draw.rect(layar, (warna_kotak), (x_kotak, y_kotak, lebar_kotak, tinggi_kotak))
    
    pygame.display.flip()
    clock.tick(60)