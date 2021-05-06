import pygame
import os
import sys
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Rangers")

FPS = 60
velocity = 9
bullets_vel = 11
max_bullets = 10

white_color = (255, 255, 255)
black_color = (0, 0, 0)
red_color = (255, 0, 0)
blue_color = (0, 0, 255)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 1, HEIGHT)

background_music = pygame.mixer.Sound(os.path.join('Assets', 'background.mp3'))
bullet_hit_sound = pygame.mixer.Sound(os.path.join('Assets', 'Ship+hit.mp3'))
bullet_fire_sound = pygame.mixer.Sound(os.path.join('Assets', 'Gun+sound.mp3'))

health_font = pygame.font.SysFont('chiller', 50)
winner_font = pygame.font.SysFont('chiller', 270)

red_hit = pygame.USEREVENT + 1
blue_hit = pygame.USEREVENT + 2

BLUE_SPACESHIP_IMG = pygame.image.load(os.path.join('Assets', 'spaceship_blue.png'))
RED_SPACESHIP_IMG = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


def draw_window(red, blue, red_bullets, blue_bullets, red_health, blue_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, black_color, BORDER)

    red_health_text = health_font.render('Health: ' + str(red_health), True, white_color)
    blue_health_text = health_font.render('Health: ' + str(blue_health), True, white_color)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(blue_health_text, (10, 10))

    WIN.blit(RED_SPACESHIP_IMG, (red.x, red.y))
    WIN.blit(BLUE_SPACESHIP_IMG, (blue.x, blue.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, red_color, bullet)

    for bullet in blue_bullets:
        pygame.draw.rect(WIN, blue_color, bullet)

    pygame.display.update()


# Left side
def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_a] and red.x - velocity > 0:
        red.x -= velocity
    if keys_pressed[pygame.K_d] and red.x + velocity + red.width/2 < BORDER.x:
        red.x += velocity
    if keys_pressed[pygame.K_w] and red.y - velocity > -30:
        red.y -= velocity
    if keys_pressed[pygame.K_s] and red.y + velocity + red.height < HEIGHT + 240:
        red.y += velocity


# Right side
def blue_movement(keys_pressed, blue):
    if keys_pressed[pygame.K_LEFT] and blue.x - velocity > BORDER.x:
        blue.x -= velocity
    if keys_pressed[pygame.K_RIGHT] and blue.x + velocity < WIDTH - 84:
        blue.x += velocity
    if keys_pressed[pygame.K_UP] and blue.y - velocity > 5:
        blue.y -= velocity
    if keys_pressed[pygame.K_DOWN] and blue.y + velocity + blue.height < HEIGHT + 271:
        blue.y += velocity


def handle_bullets(red_bullets, blue_bullets, red, blue):
    for bullet in red_bullets:
        bullet.x += bullets_vel
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(red_hit))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)

    for bullet in blue_bullets:
        bullet.x -= bullets_vel
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(blue_hit))
            blue_bullets.remove(bullet)
        elif bullet.x < 0:
            blue_bullets.remove(bullet)


def draw_winner(text):
    draw_text = winner_font.render(text, True, white_color)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_width()/2))
    pygame.display.update()
    pygame.time.delay(3000)


def main():
    red_ship = pygame.Rect(200, 335, 200, 335)
    blue_ship = pygame.Rect(900, 350, 900, 350)

    red_bullets = []
    blue_bullets = []

    red_health = 10
    blue_health = 10

    background_music.set_volume(0.01)
    background_music.play(-1)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(red_bullets) < max_bullets:
                    bullet = pygame.Rect(red_ship.x + red_ship.width//2.3, red_ship.y + red_ship.height // 6.5 + 5, 7, 5)
                    red_bullets.append(bullet)
                    bullet_fire_sound.set_volume(0.02)
                    bullet_fire_sound.play()

                if event.key == pygame.K_RCTRL and len(blue_bullets) < max_bullets:
                    bullet = pygame.Rect(blue_ship.x, blue_ship.y + blue_ship.height // 12 + 5, 7, 5)
                    blue_bullets.append(bullet)
                    bullet_fire_sound.set_volume(0.02)
                    bullet_fire_sound.play()

            if event.type == red_hit:
                red_health -= 1
                bullet_hit_sound.set_volume(0.02)
                bullet_hit_sound.play()
            if event.type == blue_hit:
                blue_health -= 1
                bullet_hit_sound.set_volume(0.02)
                bullet_hit_sound.play()

        winner_text = ''
        if red_health <= 0:
            winner_text = 'Red wins!'
        if blue_health <= 0:
            winner_text = 'Blue wins!'
        if winner_text != '':
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        red_movement(keys_pressed, red_ship)
        blue_movement(keys_pressed, blue_ship)
        handle_bullets(red_bullets, blue_bullets, red_ship, blue_ship)
        draw_window(red_ship, blue_ship, red_bullets, blue_bullets, red_health, blue_health)

    main()


if __name__ == '__main__':
    main()
