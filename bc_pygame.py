import pygame
import sys
import os

pygame.init()

# path audio
audio_file = "./music/MONTAGEM LADRAO SLOWED.mp3"

# ukuran layar
width, height = 600, 300

# warna layar
bg_color = (10,10,10)
text_color = (100,100,100) 
highlight_lyrics = (255,215,0)
font_size = 30
line_spacing = 10

lyrics = [
  [0, "Esse é o ATLXS, é o bra- , é o brabo da putaria", False],
  [5, "Tá gostosa, só quer Sosa, Sosa, senta pra ladrão", False],
  [8, "Tá gostosa, só quer Sosa, Sosa, senta pra ladrão", False],
  [12, "Tá gostosa, só quer Sosa, Sosa, senta pra ladrão", False],
  [25, "Tá gostosa, só quer Sosa, Sosa, senta pra ladrão", False]
]

lyrics.sort(key=lambda x: x[0])

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption("Lirik lagu")  
font = pygame.font.Font(None, font_size)

# load audio
if not os.path.exists(audio_file):
  print("File audio tidak ditemukan:", audio_file)
  pygame.quit()
  sys.exit()
  
try:
  pygame.mixer.init()
  pygame.mixer.music.load(audio_file)
except Exception as e:
  print("Gagal memuat file audio:", e)
  pygame.quit()
  sys.exit()

# mencari index lirik di dalam audio berdasarkan waktu
def index_lyrics(t, lyrics_list):
  idx = None
  for i in range(len(lyrics_list)):
    start = lyrics_list[i][0]
    # jika ada baris berikutnya
    if i + 1 < len(lyrics_list):
      next_start = lyrics_list[i + 1][0]
      if start <= t < next_start:
        idx = i
        break
    else:
      # baris terakhir
      if t >= start:
        idx = i
  return idx

def update_lyrics(t, lyrics_list):
  idx = index_lyrics(t, lyrics_list)
  # Reset semua lirik ke non-aktif
  for i in range(len(lyrics_list)):
    lyrics_list[i][2] = False
  # Aktifkan lirik yang sesuai dengan waktu
  if idx is not None:
    lyrics_list[idx][2] = True

# memulai audio
pygame.mixer.music.play()
music_start_time = pygame.time.get_ticks()

running = True

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
      pygame.mixer.music.stop()
      pygame.quit()
      sys.exit()
  
  # Hitung waktu yang telah berlalu sejak musik dimulai (dalam detik)
  elapsed_time = (pygame.time.get_ticks() - music_start_time) / 1000.0
  
  # Update status lirik berdasarkan waktu
  update_lyrics(elapsed_time, lyrics)
  
  # Tampilkan semua lirik
  y_position = 10
  for i in range(len(lyrics)):
    text = lyrics[i][1]
    is_active = lyrics[i][2]
    color = highlight_lyrics if is_active else text_color
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (10, y_position))
    y_position += font_size + line_spacing
  
  pygame.display.flip()
  
  screen.fill(bg_color)
  clock.tick(30)