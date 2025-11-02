import pygame
import sys
import json

pygame.init()

screen_width = 820
screen_height = 600

layar = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Music Player")

BACKGROUND_COLOR = (21, 36, 51)
PRIMARY_COLOR = (70, 130, 180)
ACCENT_COLOR = (255, 215, 0)
TEXT_COLOR = (255, 255, 255)
SECONDARY_TEXT_COLOR = (200, 200, 200)
PROGRESS_BG_COLOR = (50, 50, 50)
PROGRESS_FG_COLOR = (100, 200, 255)

musics_image = [
  "./album_image/back_to_friends_image.jpg",
  "./album_image/terlalu_tinggi_image.jpg",
  "./album_image/Versace_On_The_Floor_image.jpg",
  "./album_image/twenty_one_pilots_ride_image.jpg",
  "./album_image/im_not_the_only_one_image.jpg",
  "./album_image/red_taylor_swift_image.jpg"
]

music_titles = [
  "Back to Friends",
  "Terlalu Tinggi",
  "Versace On The Floor",
  "Ride",
  "I'm Not The Only One",
  "Red"
]

try:
    with open("./data/lyrics.json", "r") as f:
        lyrics_json = json.load(f)
    lyrics_data = {}
    for song in lyrics_json["songs"]:
        song_id = song["id"]
        lyrics_list = [(item["time"], item["text"]) for item in song["lyrics"]]
        lyrics_data[song_id] = lyrics_list
except FileNotFoundError:
    print("Lyrics file not found. Using default lyrics.")
    lyrics_data = {} 

try:
  back_to_friends = pygame.mixer.Sound("./music/sombr - back to friends (official audio).mp3")
  terlalu_tinggi = pygame.mixer.Sound("./music/Juicy Luicy - Terlalu Tinggi (Official Music Video).mp3")
  versace_on_the_floor = pygame.mixer.Sound("./music/Bruno Mars - Versace On The Floor (Lyrics).mp3")
  ride_twenty_one_pilot = pygame.mixer.Sound("./music/Ride - Twenty One Pilots (Lirik Lagu Terjemahan).mp3")
  im_not_the_only_one = pygame.mixer.Sound("./music/Sam Smith - I'm Not The Only One (Lyrics).mp3")
  red_taylor_swift = pygame.mixer.Sound("./music/Red (Taylor's Version).mp3")
  musics = [back_to_friends, terlalu_tinggi, versace_on_the_floor, ride_twenty_one_pilot, im_not_the_only_one, red_taylor_swift]
  
  music_lengths = [
    back_to_friends.get_length(),
    terlalu_tinggi.get_length(),
    versace_on_the_floor.get_length(),
    ride_twenty_one_pilot.get_length(),
    im_not_the_only_one.get_length(),
    red_taylor_swift.get_length()
  ]
except:
  back_to_friends = None
  terlalu_tinggi = None
  versace_on_the_floor = None
  ride_twenty_one_pilot = None
  im_not_the_only_one = None
  red_taylor_swift = None
  musics = []
  music_lengths = []
  print("Suara tidak ditemukan!")

music_images = []
music_rects = []
title_surfaces = []
title_rects = []
DEFAULT_IMAGE_SIZE = (128, 128)

back_button_rect = pygame.Rect(0, 0, 0, 0)

font = pygame.font.Font(None, 20)
title_font = pygame.font.Font(None, 24)
lyric_font = pygame.font.Font(None, 36)
music_bar_font = pygame.font.Font(None, 28)

COLUMNS = 3
START_X = 200
START_Y = 140 
SPACING_X = 210
SPACING_Y = 180  

for i in range(len(musics)):
  music = pygame.image.load(musics_image[i])
  music = pygame.transform.scale(music, DEFAULT_IMAGE_SIZE)
  music_rect = music.get_rect()
  
  row = i // COLUMNS
  col = i % COLUMNS   
  
  music_rect.center = (START_X + col * SPACING_X, START_Y + row * SPACING_Y)
  music_images.append(music)
  music_rects.append(music_rect)
  
  title_surface = font.render(music_titles[i], True, TEXT_COLOR)
  title_rect = title_surface.get_rect()
  title_rect.centerx = music_rect.centerx
  title_rect.top = music_rect.bottom + 12
  title_surfaces.append(title_surface)
  title_rects.append(title_rect)

MUSIC_BAR_HEIGHT = 140
music_bar_rect = pygame.Rect(0, screen_height - MUSIC_BAR_HEIGHT, screen_width, MUSIC_BAR_HEIGHT)
progress_bar_rect = pygame.Rect(20, screen_height - 25, screen_width - 40, 10)

running = True
clock = pygame.time.Clock()
current_music_index = None
music_start_time = 0
current_lyric = ""
is_music_bar_visible = False

while running:
  current_time = pygame.time.get_ticks() / 1000.0 
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
      sys.exit()
    
    if event.type == pygame.MOUSEBUTTONDOWN:
      mouse_pos = pygame.mouse.get_pos()
      for i, rect in enumerate(music_rects):
        if rect.collidepoint(mouse_pos):
          pygame.mixer.stop()
          if i < len(musics):
            musics[i].play()
            current_music_index = i
            music_start_time = pygame.time.get_ticks() / 1000.0 
            current_lyric = ""
            is_music_bar_visible = True
      
      if is_music_bar_visible and back_button_rect and back_button_rect.collidepoint(mouse_pos):
        is_music_bar_visible = False
        pygame.mixer.stop()
        current_music_index = None

  back_button_rect = None

  layar.fill(BACKGROUND_COLOR)
  
  if not is_music_bar_visible:
    for i in range(len(music_images)):
      border_rect = music_rects[i].inflate(10, 10)
      pygame.draw.rect(layar, PRIMARY_COLOR, border_rect, 2, border_radius=5)
      layar.blit(music_images[i], music_rects[i])
      layar.blit(title_surfaces[i], title_rects[i])
  else:
    pygame.draw.rect(layar, (30, 40, 50), music_bar_rect)
    pygame.draw.rect(layar, PRIMARY_COLOR, music_bar_rect, 2)
    
    if current_music_index is not None and current_music_index < len(music_images):
      small_album = pygame.transform.scale(music_images[current_music_index], (80, 80))
      album_rect = small_album.get_rect()
      album_rect.centery = music_bar_rect.centery
      album_rect.left = 20
      layar.blit(small_album, album_rect)
      
      title_surface = music_bar_font.render(music_titles[current_music_index], True, TEXT_COLOR)
      title_rect = title_surface.get_rect()
      title_rect.left = album_rect.right + 15
      title_rect.top = album_rect.top + 5
      layar.blit(title_surface, title_rect)
      
      pygame.draw.rect(layar, PROGRESS_BG_COLOR, progress_bar_rect)
      
      if current_music_index < len(music_lengths):
        elapsed_time = current_time - music_start_time
        progress = min(elapsed_time / music_lengths[current_music_index], 1.0)
        progress_width = int(progress * (progress_bar_rect.width - 4))
        if progress_width > 0:
          progress_fill_rect = pygame.Rect(
            progress_bar_rect.left + 2, 
            progress_bar_rect.top + 2, 
            progress_width, 
            progress_bar_rect.height - 4
          )
          pygame.draw.rect(layar, PROGRESS_FG_COLOR, progress_fill_rect)
      
      if current_music_index < len(music_lengths):
        elapsed_time = current_time - music_start_time
        elapsed_minutes = int(elapsed_time // 60)
        elapsed_seconds = int(elapsed_time % 60)
        total_minutes = int(music_lengths[current_music_index] // 60)
        total_seconds = int(music_lengths[current_music_index] % 60)
        
        time_text = f"{elapsed_minutes:02d}:{elapsed_seconds:02d} / {total_minutes:02d}:{total_seconds:02d}"
        time_surface = font.render(time_text, True, SECONDARY_TEXT_COLOR)
        time_rect = time_surface.get_rect()
        time_rect.right = progress_bar_rect.right
        time_rect.top = progress_bar_rect.bottom - 26
        layar.blit(time_surface, time_rect)
    
    back_button_rect = pygame.Rect(screen_width - 160, music_bar_rect.top + 10, 120, 40)
    pygame.draw.rect(layar, PRIMARY_COLOR, back_button_rect, border_radius=6)
    back_text = font.render("Back", True, TEXT_COLOR)
    back_text_rect = back_text.get_rect()
    back_text_rect.center = back_button_rect.center
    layar.blit(back_text, back_text_rect)
  
  if current_music_index is not None and is_music_bar_visible:
    elapsed_time = current_time - music_start_time
    
    if current_music_index in lyrics_data:
      for timing, lyric_text in lyrics_data[current_music_index]:
        if elapsed_time >= timing:
          current_lyric = lyric_text
    
    if current_lyric:
      lyric_surface = lyric_font.render(current_lyric, True, ACCENT_COLOR)
      lyric_rect = lyric_surface.get_rect()
      lyric_rect.centerx = screen_width // 2
      lyric_rect.bottom = music_bar_rect.top - 20
      layar.blit(lyric_surface, lyric_rect)
  
  pygame.display.flip()
  clock.tick(60)

pygame.quit()