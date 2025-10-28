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

# Lyrics with timing (in seconds)
lyrics_data = {
  0: [  # Back to Friends
    (0, "Song starting..."),
    (5, "First verse"),
    (10, "Music playing..."),
    (15, "Chorus coming..."),
  ],
  1: [  # Terlalu Tinggi
    (0, "Terlalu tinggi"),
    (5, "Untuk ku raih"),
    (10, "Terlalu jauh"),
    (15, "Untuk ku kejar"),
  ],
  2: [  # Versace On The Floor
    (0, "Song begins..."),
    (5, "Let's take our time tonight"),
    (10, "Above us all the stars are watching"),
    (15, "There's no place I'd rather be"),
  ],
  3: [  # Red
    (0, "Loving him is like..."),
    (5, "Driving a new Maserati"),
    (10, "Down a dead-end street"),
    (15, "Faster than the wind"),
  ],
  4: [  # Ride
    (0, "I just wanna stay"),
    (5, "In the sun where I find"),
    (10, "I know it's hard sometimes"),
    (15, "Pieces of peace in the sun's peace of mind"),
  ],
  5: [  # I'm Not The Only One
    (0, "You and me we made a vow"),
    (5, "For better or for worse"),
    (10, "I can't believe you let me down"),
    (15, "But the proof is in the way it hurts"),
  ]
} 

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

font = pygame.font.Font(None, 20)

COLUMNS = 3
START_X = 150
START_Y = 150 
SPACING_X = 150  
SPACING_Y = 150  

for i in range(len(musics)):
  music = pygame.image.load(musics_image[i])
  music = pygame.transform.scale(music, DEFAULT_IMAGE_SIZE)
  music_rect = music.get_rect()
  
  row = i // COLUMNS
  col = i % COLUMNS   
  
  music_rect.center = (START_X + col * SPACING_X, START_Y + row * SPACING_Y)
  music_images.append(music)
  music_rects.append(music_rect)
  
  title_surface = font.render(music_titles[i], True, (255, 255, 255))
  title_rect = title_surface.get_rect()
  title_rect.centerx = music_rect.centerx
  title_rect.top = music_rect.bottom + 5
  title_surfaces.append(title_surface)
  title_rects.append(title_rect)
  

running = True
clock = pygame.time.Clock()
current_music_index = None
music_start_time = 0
current_lyric = ""
lyric_font = pygame.font.Font(None, 36)

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
      sys.exit()
    
    # Check for mouse clicks on music images
    if event.type == pygame.MOUSEBUTTONDOWN:
      mouse_pos = pygame.mouse.get_pos()
      for i, rect in enumerate(music_rects):
        if rect.collidepoint(mouse_pos):
          # Stop all music
          pygame.mixer.stop()
          # Play selected music
          if i < len(musics):
            musics[i].play()
            current_music_index = i
            music_start_time = pygame.time.get_ticks() / 1000.0  # Convert to seconds
            current_lyric = ""
  
  layar.fill("#152433")
  
  for i in range(len(music_images)):
    layar.blit(music_images[i], music_rects[i])
    layar.blit(title_surfaces[i], title_rects[i])
  
  # Update and display lyrics
  if current_music_index is not None:
    current_time = pygame.time.get_ticks() / 1000.0  # Current time in seconds
    elapsed_time = current_time - music_start_time
    
    # Find the appropriate lyric based on elapsed time
    if current_music_index in lyrics_data:
      for timing, lyric_text in lyrics_data[current_music_index]:
        if elapsed_time >= timing:
          current_lyric = lyric_text
    
    # Display the current lyric
    if current_lyric:
      lyric_surface = lyric_font.render(current_lyric, True, (255, 255, 100))
      lyric_rect = lyric_surface.get_rect()
      lyric_rect.centerx = screen_width // 2
      lyric_rect.bottom = screen_height - 30
      layar.blit(lyric_surface, lyric_rect)
  
  pygame.display.flip()
  clock.tick(60)
