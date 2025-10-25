import pygame
import sys

pygame.init()

screen_width = 700
screen_height = 500

layar = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Music Player")


musics_image = [
  "./album_image/back_to_friends_image.jpg",
  "./album_image/terlalu_tinggi_image.jpg",
  "./album_image/Versace_On_The_Floor_image.jpg",
  "./album_image/red_taylor_swift_image.jpg",
  "./album_image/twenty_one_pilots_ride_image.jpg",
  "./album_image/im_not_the_only_one_image.jpg"
]

music_titles = [
  "Back to Friends",
  "Terlalu Tinggi",
  "Versace On The Floor",
  "Red",
  "Ride",
  "I'm Not The Only One"
] 

try:
  back_to_friends = pygame.mixer.Sound("./music/sombr - back to friends (official audio).mp3")
  terlalu_tinggi = pygame.mixer.Sound("./music/Juicy Luicy - Terlalu Tinggi (Official Music Video).mp3")
  versace_on_the_floor = pygame.mixer.Sound("./music/Bruno Mars - Versace On The Floor (Lyrics).mp3")
  ride_twenty_one_pilot = pygame.mixer.Sound("./music/Ride - Twenty One Pilots (Lirik Lagu Terjemahan).mp3")
  im_not_the_only_one = pygame.mixer.Sound("./music/Sam Smith - I'm Not The Only One (Lyrics).mp3")
  red_taylor_swift = pygame.mixer.Sound("./music/Red (Taylor's Version).mp3")
  musics = [back_to_friends, terlalu_tinggi, versace_on_the_floor, ride_twenty_one_pilot, im_not_the_only_one, red_taylor_swift]
except:
  back_to_friends = None
  terlalu_tinggi = None
  versace_on_the_floor = None
  ride_twenty_one_pilot = None
  im_not_the_only_one = None
  red_taylor_swift = None
  musics = []
  print("Suara tidak ditemukan!")



music_images = []
music_rects = []
title_surfaces = []
title_rects = []
DEFAULT_IMAGE_SIZE = (100, 100)

# Font for song titles
font = pygame.font.Font(None, 20)

# Grid layout: 3 columns x 2 rows
COLUMNS = 3
START_X = 150  # Starting X position
START_Y = 150  # Starting Y position
SPACING_X = 150  # Horizontal spacing between images
SPACING_Y = 150  # Vertical spacing between rows

for i in range(len(musics)):
  music = pygame.image.load(musics_image[i])
  music = pygame.transform.scale(music, DEFAULT_IMAGE_SIZE)
  music_rect = music.get_rect()
  
  # Calculate grid position
  row = i // COLUMNS  # Integer division to get row (0 or 1)
  col = i % COLUMNS   # Modulo to get column (0, 1, or 2)
  
  music_rect.center = (START_X + col * SPACING_X, START_Y + row * SPACING_Y)
  music_images.append(music)
  music_rects.append(music_rect)
  
  # Create title text
  title_surface = font.render(music_titles[i], True, (255, 255, 255))
  title_rect = title_surface.get_rect()
  title_rect.centerx = music_rect.centerx
  title_rect.top = music_rect.bottom + 5
  title_surfaces.append(title_surface)
  title_rects.append(title_rect)
  

running = True
clock = pygame.time.Clock()

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
      sys.exit()
  
  layar.fill("#152433")
  
  for i in range(len(music_images)):
    layar.blit(music_images[i], music_rects[i])
    layar.blit(title_surfaces[i], title_rects[i])
  
  pygame.display.flip()
  clock.tick(60)
