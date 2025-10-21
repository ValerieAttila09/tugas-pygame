import pygame
import sys

pygame.init()

# layar
screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption("Sound HOREG")
clock = pygame.time.Clock()

# Warna object
# red, blue, white, black
red = "#FF0000"
blue = "#0020FF"
white = "#FFFFFF"
black = "#13131A"

# posisi objek
player = pygame.Rect(200, 300, 50, 50)
obstacle = pygame.Rect(220, 0, 50, 50)
speed_y = 12
lives = 3
game_over = False

# mwmasukkan suara / efek suara
try:
  splash_sound = pygame.mixer.Sound("./sounds/intro-music-black-box-simple-guitar-12701.mp3")
  hit_sound = pygame.mixer.Sound("./sounds/boom-356126.mp3")
except:
  splash_sound = None
  hit_sound = None
  print("Suara tidak ditemukan!")

# font
font_big = pygame.font.Font(None, 60)
font_small = pygame.font.Font(None, 36)

# memasukkan gambar untuk nyawa
try:
  icon = pygame.image.load("./images/heart.png")
  icon = pygame.transform.scale(icon, (30, 30))  
except:
  icon = None
  print("Icon tidak ditemukan!")

# fungsi untuk splash screen
def show_splash():
  screen.fill(white)
  title_text = font_big.render("Watch Out!", True, blue)
  info_text = font_small.render("Tekan 'Spasi' untuk memulai", True, black)
  
  # tempel / memindahkan font
  screen.blit(title_text, (500 // 2 - title_text.get_width() // 2, 140))
  screen.blit(info_text, (500 // 2 - info_text.get_width() // 2, 140 + 50))
  
  pygame.display.flip()
  
  if splash_sound:
    splash_sound.play()
  waiting = True
  while waiting:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      # spasi akan masuk ke halaman berikutnya
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          waiting = False 
          if splash_sound: 
            splash_sound.stop()
      if splash_sound and not pygame.mixer.get_busy():
        waiting = False
        
        clock.tick(60)

show_splash()

# halaman game
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
  keys = pygame.key.get_pressed()
  if not game_over:
    if keys[pygame.K_LEFT]:
      player.x -= 8
    if keys[pygame.K_RIGHT]:
      player.x += 8
    # atur kecepatan obstacles
    obstacle.y += speed_y
    if obstacle.y > 400:
      obstacle.y = -50
    
    if player.colliderect(obstacle):
      lives -= 1
      if hit_sound:
        hit_sound.play()
      screen.fill(red) 
      pygame.display.flip()
      pygame.time.delay(400)
      obstacle.y = -50
      player.x = 200
      if lives <= 0:
        game_over = True
  # gambar layar
  screen.fill(white)
  pygame.draw.rect(screen, blue, player)
  pygame.draw.rect(screen, red, obstacle)
  
  # membuat nyawa dalam avatar / gambar
  if icon:
    for i in range(lives):
      screen.blit(icon, (20 + i * 40, 20))
  else:
    text = font_small.render(f"nyawa : {lives}", True, black)
    screen.blit(text, (20, 20))
  
  # game over
  if game_over:
    over_text = font_small.render("GAME OVER", True, blue)
    restart_text = font_small.render("Tekan [R] untuk main lagi...", True, black)
    
    screen.blit(over_text, (180, 160))
    screen.blit(restart_text, (150, 210))

    if keys[pygame.K_r]:
      lives = 3
      game_over = False
      obstacle.y = -50
  
  pygame.display.flip()
  clock.tick(60)
      