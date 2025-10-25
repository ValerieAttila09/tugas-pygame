import pygame
import sys
import random

pygame.init()
X = 720
Y = 480
size = width, height = X, Y
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


bg_image = pygame.image.load("images/bg_angry_bird.png").convert()
bg_image = pygame.transform.scale(bg_image, (X, Y))

# angry bird
image_bird = pygame.image.load('images/angry_bird.png')
DEFAULT_IMAGE_SIZE = (80, 80)
image_bird = pygame.transform.scale(image_bird, DEFAULT_IMAGE_SIZE)
DEFAULT_IMAGE_POSITION = (200, 200)
rect = image_bird.get_rect()
rect.center = (200, 300)

# king
image_king = pygame.image.load('images/king_pig.png')
DEFAULT_IMAGE_SIZE = (100, 125)
image_king = pygame.transform.scale(image_king, DEFAULT_IMAGE_SIZE)
DEFAULT_IMAGE_POSITION = (500, 200)
rect_king = image_king.get_rect()
KING_PIG_X = 580  # Fixed X position for king pig (right side)
rect_king.center = (KING_PIG_X, 300)

# boom effect
image_boom = pygame.image.load('images/boom.png')
DEFAULT_IMAGE_SIZE = (400, 400)
image_boom = pygame.transform.scale(image_boom, DEFAULT_IMAGE_SIZE)
DEFAULT_IMAGE_POSITION = (500, 200)
rect_boom = image_boom.get_rect()
rect_boom.center = (500, 300)

# Proyektil king pig
array_proyektil = []
timer_tembakan = 0
INTERVAL_TEMBAKAN = 45 
KECEPATAN_PROYEKTIL = 8

# Proyektil angry bird
proyektil_angry_bird = []
angry_bird_cooldown_tembakan = 0 
ANGRY_BIRD_SHOOT_DELAY = 60
ANGRY_BIRD_KECEPATAN_PROYEKTIL = 7

running = False
score = 0
timer_ledakan = 0
nyawa = 3
game_over = False

# font
font_big = pygame.font.Font(None, 60)
font_small = pygame.font.Font(None, 36)

# memasukkan suara / efek suara
try:
  splash_sound = pygame.mixer.Sound("./sounds/intro-music-black-box-simple-guitar-12701.mp3")
  hit_sound = pygame.mixer.Sound("./sounds/boom-356126.mp3")
except:
  splash_sound = None
  hit_sound = None
  print("Suara tidak ditemukan!")


def movement(player):
  button = pygame.key.get_pressed()
  if button[pygame.K_LEFT] and player.x > 0: player.x -= 5
  if button[pygame.K_RIGHT] and player.x < X - player.width: player.x += 5
  if button[pygame.K_UP] and player.y > 0: player.y -= 5
  if button[pygame.K_DOWN] and player.y < Y - player.height: player.y += 5 

def tembak_proyektil():
  dx = rect.centerx - rect_king.centerx
  dy = rect.centery - rect_king.centery
  
  jarak = (dx**2 + dy**2)**0.5
  
  if jarak > 0:
    dx = (dx / jarak) * KECEPATAN_PROYEKTIL
    dy = (dy / jarak) * KECEPATAN_PROYEKTIL
  else:
    dx = KECEPATAN_PROYEKTIL
    dy = 0
  
  rect_proyektil = pygame.Rect(rect_king.centerx - 10, rect_king.centery - 10, 20, 20)
  proyektil = {'rect': rect_proyektil, 'dx': dx, 'dy': dy}
  array_proyektil.append(proyektil)

def update_proyektil():
  for proyektil in array_proyektil[:]:
    proyektil['rect'].x += proyektil['dx']
    proyektil['rect'].y += proyektil['dy']
    
    if (proyektil['rect'].x < -20 or proyektil['rect'].x > X + 20 or 
        proyektil['rect'].y < -20 or proyektil['rect'].y > Y + 20):
      array_proyektil.remove(proyektil)

def buat_proyektil():
  for proyektil in array_proyektil:
    pygame.draw.circle(screen, (255, 0, 0), proyektil['rect'].center, 10)

def tembak_proyektil_angry_bird():
  rect_proyektil = pygame.Rect(rect.centerx + 40, rect.centery - 5, 15, 10)
  proyektil = {'rect': rect_proyektil, 'dx': ANGRY_BIRD_KECEPATAN_PROYEKTIL, 'dy': 0}
  proyektil_angry_bird.append(proyektil)

def update_animasi_tembak():
  for proyektil in proyektil_angry_bird[:]:
    proyektil['rect'].x += proyektil['dx']
    if proyektil['rect'].x > X + 20:
      proyektil_angry_bird.remove(proyektil)

def objek_proyektil_angry_bird():
  for proyektil in proyektil_angry_bird:
    pygame.draw.rect(screen, (255, 255, 0), proyektil['rect'])

def show_splash():
  screen.fill("#ffffff")
  title_text = font_big.render("Watch Out!", True, "#2030d7")
  info_text = font_small.render("Tekan 'Spasi' untuk memulai", True, "#000000")
  info_fire = font_small.render("Tekan 'F' untuk menembak", True, "#243456")
  
  # tempel / memindahkan font
  screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 140))
  screen.blit(info_text, (width // 2 - info_text.get_width() // 2, 140 + 50))
  screen.blit(info_fire, (width // 2 - info_fire.get_width() // 2, 140 + 90))
  
  pygame.display.flip()
  
  if splash_sound:
    splash_sound.play()
  waiting = True
  while waiting:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          waiting = False 
          if splash_sound: 
            splash_sound.stop()
      if splash_sound and not pygame.mixer.get_busy():
        waiting = False
        
        clock.tick(60)
show_splash()

while not running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = True
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_f and angry_bird_cooldown_tembakan == 0 and not game_over:
        tembak_proyektil_angry_bird()
        angry_bird_cooldown_tembakan = ANGRY_BIRD_SHOOT_DELAY
   
  screen.blit(bg_image, (0, 0))
  screen.blit(image_bird, rect)
  
  movement(rect)
  
  if angry_bird_cooldown_tembakan > 0:
    angry_bird_cooldown_tembakan -= 1
  
  timer_tembakan += 1
  if timer_tembakan >= INTERVAL_TEMBAKAN:
    tembak_proyektil()
    timer_tembakan = 0
  
  update_proyektil()
  buat_proyektil()
  
  update_animasi_tembak()
  objek_proyektil_angry_bird()
  
  for proyektil in array_proyektil[:]:
    if rect.colliderect(proyektil['rect']):
      array_proyektil.remove(proyektil)
      nyawa -= 1
      if nyawa <= 0:
        game_over = True
  
  for proyektil in proyektil_angry_bird[:]:
    if rect_king.colliderect(proyektil['rect']):
      proyektil_angry_bird.remove(proyektil)
      score += 2
      
      rect_king.y = random.randint(100, Y - 150)
      rect_king.x = KING_PIG_X - rect_king.width // 2 
      timer_ledakan = 45
      rect_boom.x = rect_king.x - 125
      rect_boom.y = rect_king.y - 125
      if hit_sound:
        hit_sound.play()
  
  if rect.colliderect(rect_king):
    screen.blit(image_boom, rect_boom)
    timer_ledakan = 45
    score += 1
    rect_king.y = random.randint(100, Y - 150)
    rect_king.x = KING_PIG_X - rect_king.width // 2 
    rect_boom.x = rect_king.x - 125
    rect_boom.y = rect_king.y - 125
  else:
    screen.blit(image_king, rect_king)
  
  if timer_ledakan > 0:
    screen.blit(image_boom, rect_boom)
    timer_ledakan -= 1
  else:
    screen.blit(image_king, rect_king)
  
  font = pygame.font.Font(None, 30)
  text_score = font.render(f"Score: {score}", True, (255, 255, 255))
  text_nyawa = font.render(f"nyawa: {nyawa}", True, (255, 255, 255))
  screen.blit(text_score, (10, 10))
  screen.blit(text_nyawa, (10, 40))
  
  if game_over:
    game_over_text = font_big.render("GAME OVER!", True, (255, 0, 0))
    restart_text = font_small.render("Tekan 'R' untuk restart atau 'Q' untuk keluar", True, (30, 30, 30))
    screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - 50))
    screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 20))
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
      nyawa = 3
      score = 0
      game_over = False
      array_proyektil.clear()
      proyektil_angry_bird.clear()
      angry_bird_cooldown_tembakan = 0
      rect.center = (200, 300)
      rect_king.center = (KING_PIG_X, 300)
    elif keys[pygame.K_q]:
      running = True
  
  pygame.display.flip()
  clock.tick(60)