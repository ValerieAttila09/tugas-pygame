import pygame
import sys
import random

pygame.init()

screen_width = int(900 - (900 * 20 / 100))
screen_height = int(790 - (790 * 20 / 100))

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Refleksi - Pygame")

bg_image = pygame.image.load("images/space_bg.jpg").convert()
bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))

plane = pygame.image.load('images/aircraft.png')
plane = pygame.transform.scale(plane, (80, 80))
rect = plane.get_rect()
rect.center = (200, 300)

asteroid_img = pygame.image.load('images/asteroid.png')
asteroid_img = pygame.transform.scale(asteroid_img, (80, 80))

nyawa_img = pygame.image.load('images/heart.png')
nyawa_img = pygame.transform.scale(nyawa_img, (30, 30))

running = True
clock = pygame.time.Clock()
nyawa = 5
score = 0
game_over = False

font_big = pygame.font.Font(None, 60)
font_small = pygame.font.Font(None, 36)

proyektil_jet = []
KECEPATAN_PROYEKTIL_JET = 10

asteroids = []
ASTEROID_SPAWN_RATE = 60 
astroid_spawn_counter = 0

try:
    splash_sound = pygame.mixer.Sound("./sounds/space_song.mp3")
    hit_sound = pygame.mixer.Sound("./sounds/boom-356126.mp3")
    shot_sound = pygame.mixer.Sound("./sounds/zip-laser-94333.mp3")
except:
    splash_sound = None
    hit_sound = None
    shot_sound = None
    print("Suara tidak ditemukan!")


def tembak_proyektil_jet():
    rect_proyektil = pygame.Rect(rect.centerx, rect.centery - 5, 15, 10)
    proyektil = {'rect': rect_proyektil, 'dx': 0, 'dy': KECEPATAN_PROYEKTIL_JET}
    proyektil_jet.append(proyektil)
    if shot_sound:
        shot_sound.play()


def update_animasi_tembak():
    for proyektil in proyektil_jet[:]:
        proyektil['rect'].y -= proyektil['dy']
        if proyektil['rect'].y > screen_height + 20:
            proyektil_jet.remove(proyektil)


def objek_proyektil_jet():
    for proyektil in proyektil_jet:
        pygame.draw.rect(screen, (255, 255, 0), proyektil['rect'])


def spawn_asteroid():
    x_pos = random.randint(0, screen_width - 80)
    asteroid_rect = asteroid_img.get_rect()
    asteroid_rect.center = (x_pos, -40) 
    asteroid = {
        'rect': asteroid_rect,
        'speed': random.randint(3, 7) 
    }
    asteroids.append(asteroid)


def update_asteroids():
    global score
    for asteroid in asteroids[:]:
        asteroid['rect'].y += asteroid['speed']
        if asteroid['rect'].y > screen_height + 50:
            asteroids.remove(asteroid)
            score += 1


def draw_asteroids():
    for asteroid in asteroids:
        screen.blit(asteroid_img, asteroid['rect'])


def check_collisions():
    global nyawa, score, game_over
    for proyektil in proyektil_jet[:]:
        for asteroid in asteroids[:]:
            if proyektil['rect'].colliderect(asteroid['rect']):
                if proyektil in proyektil_jet:
                    proyektil_jet.remove(proyektil)
                asteroids.remove(asteroid)
                score += 10 
                if hit_sound:
                    hit_sound.play()
                break
    
    for asteroid in asteroids[:]:
        if rect.colliderect(asteroid['rect']):
            asteroids.remove(asteroid)
            nyawa -= 1
            if hit_sound:
                hit_sound.play()
            if nyawa <= 0:
                game_over = True
            break


def movement(player):
    button = pygame.key.get_pressed()
    if button[pygame.K_LEFT] and player.x > 0:
        player.x -= 10
    if button[pygame.K_RIGHT] and player.x < screen_width - player.width:
        player.x += 10
    if button[pygame.K_UP] and player.y > 0:
        player.y -= 10
    if button[pygame.K_DOWN] and player.y < screen_height - player.height:
        player.y += 10


def show_splash():
    screen.blit(bg_image, (0, 0))
    
    title_text = font_big.render("Watch Out!", True, "#FFFFFF")
    info_text = font_small.render("Tekan 'Spasi' untuk memulai", True, "#FFFFFF")
    info_fire = font_small.render("Tekan 'F' untuk menembak", True, "#FFFFFF")
    
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 140))
    screen.blit(info_text, (screen_width // 2 - info_text.get_width() // 2, 140 + 50))
    screen.blit(info_fire, (screen_width // 2 - info_fire.get_width() // 2, 140 + 90))
    
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
        clock.tick(60)


def draw_lives():
    for i in range(nyawa):
        screen.blit(nyawa_img, (10 + i * 40, 10))


show_splash()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if not game_over and event.key == pygame.K_f:
                tembak_proyektil_jet()
    
    if not game_over:
        astroid_spawn_counter += 1
        if astroid_spawn_counter >= ASTEROID_SPAWN_RATE:
            spawn_asteroid()
            astroid_spawn_counter = 0
        
        movement(rect)
        update_animasi_tembak()
        update_asteroids()
        check_collisions()
        
    screen.blit(bg_image, (0, 0))
    screen.blit(plane, rect)
    draw_asteroids()
    objek_proyektil_jet()
    
    font = pygame.font.Font(None, 30)
    text_score = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text_score, (10, 70))
    
    draw_lives()
    
    
    if game_over:
        game_over_text = font_big.render("GAME OVER!", True, (255, 0, 0))
        restart_text = font_small.render("Tekan 'R' untuk restart atau 'Q' untuk keluar", True, (255, 255, 255))
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 50))
        screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + 20))
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            nyawa = 3
            score = 0
            game_over = False
            proyektil_jet.clear()
            asteroids.clear()
            rect.center = (200, 300)
        elif keys[pygame.K_q]:
            running = False
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()