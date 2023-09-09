from setup import *
from game import SpaceRace, GameOver, Splash

is_running = True

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

previous_time = current_time = pygame.time.get_ticks()

current_scene = Splash()

SOUND_MUSIC.play(-1)

while is_running:
    
    current_time = pygame.time.get_ticks()
    delta_time = current_time - previous_time
    previous_time = current_time

    screen.fill((0, 0, 0))

    status = current_scene.update(delta_time)
    current_scene.draw(screen)

    if status is not None:
        if isinstance(current_scene, Splash):
            current_scene = SpaceRace()
        elif isinstance(current_scene, SpaceRace):
            current_scene = GameOver(status)
        elif isinstance(current_scene, GameOver):
            current_scene = Splash()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
            
    pygame.display.update()

pygame.quit()
