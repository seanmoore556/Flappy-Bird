import pygame
import sys
import random

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 800)) # First floor
    screen.blit(floor_surface, (floor_x_pos + 576, 800)) # Second floor (starts on the right)

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos -350)) # Gap between pipes
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5 # Takes all pipe rects and moves to the left
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 900:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True) # Flips pipe with y axis
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe): # checks if bird collides with any pipes
            death_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 780: # collision check for floor and top
        death_sound.play()
        return False
    
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 2, 1) # Third arg is the scale
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery)) #takes center y of the previous bird rect so postion isnt changed 
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(f"Score: {int(score)}", True, (255, 255, 0))
        score_rect = score_surface.get_rect(center = (288, 70))
        screen.blit(score_surface, score_rect)
    if game_state == "game_over":
        score_surface = game_font.render(f"Score: {int(score)}", True, (255, 255, 0))
        score_rect = score_surface.get_rect(center = (288, 70))
        screen.blit(score_surface, score_rect)
    
        high_score_surface = game_font.render(f"high Score: {int(high_score)}", True, (204, 102, 0))
        high_score_rect = high_score_surface.get_rect(center = (288,770))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()
screen = pygame.display.set_mode((576, 900))
clock = pygame.time.Clock()
game_font = pygame.font.Font("C:/Users/sean/Desktop/VsCode/flappy_bird/FlappyBird_Python-master/04B_19.ttf", 40)

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load("C:/Users/sean/Desktop/VsCode/flappy_bird/FlappyBird_Python-master/assets/background-night.png").convert() # converts image easier for pygame
bg_surface = pygame.transform.scale2x(bg_surface) # double display surface

floor_surface = pygame.image.load("C:/Users/sean/Desktop/VsCode/flappy_bird/FlappyBird_Python-master/assets/base.png").convert()
floor_surface = pygame.transform.scale2x(floor_surface) # double display surface
floor_x_pos = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load("C:/Users/sean/Desktop/VsCode/flappy_bird/FlappyBird_Python-master/assets/yellowbird-downflap.png").convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load("C:/Users/sean/Desktop/VsCode/flappy_bird/FlappyBird_Python-master/assets/yellowbird-midflap.png").convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load("C:/Users/sean/Desktop/VsCode/flappy_bird/FlappyBird_Python-master/assets/yellowbird-upflap.png").convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 450))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load("C:/Users/sean/Desktop/VsCode/flappy_bird/FlappyBird_Python-master/assets/pipe-red.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT # Trigger by timer instead of user input
pygame.time.set_timer(SPAWNPIPE, 1200) # in ms so its 1.2 secs
pipe_height = [400, 500, 600]

game_over_surface = pygame.image.load("C:/Users/sean/Desktop/VsCode/flappy_bird/FlappyBird_Python-master/assets/message.png").convert_alpha()
game_over_surface = pygame.transform.scale(game_over_surface, (280, 400))
game_over_rect = game_over_surface.get_rect(center = (288, 400))

flap_sound = pygame.mixer.Sound("C:/Users/sean/Desktop/VsCode/flappy_bird/FlappyBird_Python-master/sound/sfx_wing.wav")
death_sound = pygame.mixer.Sound("C:/Users/sean/Desktop/VsCode/flappy_bird/FlappyBird_Python-master/sound/sfx_hit.wav")
score_sound = pygame.mixer.Sound("C:/Users/sean/Desktop/VsCode/flappy_bird/FlappyBird_Python-master/sound/sfx_point.wav")
score_sound_countdown = 100
flap_sound.set_volume(0.03)
death_sound.set_volume(0.03)
score_sound.set_volume(0.03)


# Main loop
while True:
    for event in pygame.event.get(): # pygame looks for all events
        if event.type == pygame.QUIT:
            pygame.quit() # loop is still running
            sys.exit() # Need to completley stop loop
        
        if event.type == pygame.KEYDOWN: # Checks if any key is pressed
            if event.key == pygame.K_SPACE and game_active: # Jumping
                bird_movement = 0
                bird_movement -= 10
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False: # Reset
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 450)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe()) # Returns new pipe with the dimensions of pipe_surface

        if event.type == BIRDFLAP: # bird flap animation never more than 2 if so it is reset to 0
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0)) #puts one surface on another surface

    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)
    
        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # score
        score += 0.01
        score_display("main_game")
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display("game_over")

    #floor
    floor_x_pos -= 1 # moves floor to the left
    draw_floor()
    if floor_x_pos <= -576:
            floor_x_pos = 0
    

    pygame.display.update() # Updates portion of the screen 
    clock.tick(120) # Max FPS


