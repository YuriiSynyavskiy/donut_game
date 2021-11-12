import os
import pygame
from scenes.title_scene import TitleScene
from utils.screen import Screen
import constants
os.environ['ACTIVE_SOUND'] = 'Active'


def run_game(fps):
    pygame.init()
    pygame.display.set_caption("Donuts")
    background_sound = pygame.mixer.music.load(constants.background_sound_path)
    pygame.mixer.music.play(-1)
    pygame.mouse.set_visible(False)

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_params = Screen(pygame.display.Info().current_w, pygame.display.Info().current_h)


    clock = pygame.time.Clock()


    active_scene = TitleScene(screen_params)

    while active_scene:
        pressed_keys = pygame.key.get_pressed()
        
        # Event filtering
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or \
                              pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                elif event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True 
            if quit_attempt:
                active_scene.Terminate()
            else:
                filtered_events.append(event)
        
        active_scene.ProcessInput(filtered_events, pressed_keys)
        active_scene.Update()
        active_scene.Render(screen)
        
        active_scene = active_scene.next
        
        pygame.display.flip()
        clock.tick(fps)


if __name__ == "__main__":
    run_game(100)
