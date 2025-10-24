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
projectiles = []
shoot_timer = 0
SHOOT_INTERVAL = 45 
PROJECTILE_SPEED = 8

# Proyektil angry bird
bird_projectiles = []
bird_shoot_cooldown = 0 
BIRD_SHOOT_DELAY = 60
BIRD_PROJECTILE_SPEED = 7

running = False
score = 0
boom_timer = 0
lives = 3
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
    dx = (dx / jarak) * PROJECTILE_SPEED
    dy = (dy / jarak) * PROJECTILE_SPEED
  else:
    dx = PROJECTILE_SPEED
    dy = 0
  
  projectile_rect = pygame.Rect(rect_king.centerx - 10, rect_king.centery - 10, 20, 20)
  projectile = {'rect': projectile_rect, 'dx': dx, 'dy': dy}
  projectiles.append(projectile)

def update_proyektil():
  for projectile in projectiles[:]:
    projectile['rect'].x += projectile['dx']
    projectile['rect'].y += projectile['dy']
    
    if (projectile['rect'].x < -20 or projectile['rect'].x > X + 20 or 
        projectile['rect'].y < -20 or projectile['rect'].y > Y + 20):
      projectiles.remove(projectile)

def draw_projectiles():
  for projectile in projectiles:
    pygame.draw.circle(screen, (255, 0, 0), projectile['rect'].center, 10)

def shoot_bird_projectile():
  projectile_rect = pygame.Rect(rect.centerx + 40, rect.centery - 5, 15, 10)
  projectile = {'rect': projectile_rect, 'dx': BIRD_PROJECTILE_SPEED, 'dy': 0}
  bird_projectiles.append(projectile)

def update_bird_projectiles():
  for projectile in bird_projectiles[:]:
    projectile['rect'].x += projectile['dx']
    if projectile['rect'].x > X + 20:
      bird_projectiles.remove(projectile)

def draw_bird_projectiles():
  for projectile in bird_projectiles:
    pygame.draw.rect(screen, (255, 255, 0), projectile['rect'])

def show_splash():
  screen.fill("#ffffff")
  title_text = font_big.render("Watch Out!", True, "#2030d7")
  info_text = font_small.render("Tekan 'Spasi' untuk memulai", True, "#000000")
  
  # tempel / memindahkan font
  screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 140))
  screen.blit(info_text, (width // 2 - info_text.get_width() // 2, 140 + 50))
  
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
      if event.key == pygame.K_f and bird_shoot_cooldown == 0 and not game_over:
        shoot_bird_projectile()
        bird_shoot_cooldown = BIRD_SHOOT_DELAY
   
  screen.blit(bg_image, (0, 0))
  screen.blit(image_bird, rect)
  
  movement(rect)
  
  if bird_shoot_cooldown > 0:
    bird_shoot_cooldown -= 1
  
  shoot_timer += 1
  if shoot_timer >= SHOOT_INTERVAL:
    tembak_proyektil()
    shoot_timer = 0
  
  update_proyektil()
  draw_projectiles()
  
  update_bird_projectiles()
  draw_bird_projectiles()
  
  for projectile in projectiles[:]:
    if rect.colliderect(projectile['rect']):
      projectiles.remove(projectile)
      lives -= 1
      if lives <= 0:
        game_over = True
  
  for projectile in bird_projectiles[:]:
    if rect_king.colliderect(projectile['rect']):
      bird_projectiles.remove(projectile)
      score += 2
      
      rect_king.y = random.randint(100, Y - 150)
      rect_king.x = KING_PIG_X - rect_king.width // 2 
      boom_timer = 45
      rect_boom.x = rect_king.x - 125
      rect_boom.y = rect_king.y - 125
      if hit_sound:
        hit_sound.play()
  
  if rect.colliderect(rect_king):
    screen.blit(image_boom, rect_boom)
    boom_timer = 45
    score += 1
    rect_king.y = random.randint(100, Y - 150)
    rect_king.x = KING_PIG_X - rect_king.width // 2 
    rect_boom.x = rect_king.x - 125
    rect_boom.y = rect_king.y - 125
  else:
    screen.blit(image_king, rect_king)
  
  if boom_timer > 0:
    screen.blit(image_boom, rect_boom)
    boom_timer -= 1
  else:
    screen.blit(image_king, rect_king)
  
  font = pygame.font.Font(None, 30)
  text_score = font.render(f"Score: {score}", True, (255, 255, 255))
  text_lives = font.render(f"Lives: {lives}", True, (255, 255, 255))
  screen.blit(text_score, (10, 10))
  screen.blit(text_lives, (10, 40))
  
  if game_over:
    game_over_text = font_big.render("GAME OVER!", True, (255, 0, 0))
    restart_text = font_small.render("Tekan 'R' untuk restart atau 'Q' untuk keluar", True, (255, 255, 255))
    screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - 50))
    screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 20))
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
      lives = 3
      score = 0
      game_over = False
      projectiles.clear()
      bird_projectiles.clear()
      bird_shoot_cooldown = 0
      rect.center = (200, 300)
      rect_king.center = (KING_PIG_X, 300)
    elif keys[pygame.K_q]:
      running = True
  
  pygame.display.flip()
  clock.tick(60)