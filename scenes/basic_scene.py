import pygame
import random
import constants
from sprites.sprites import Cursor, Background, SoundButton
from utils.utils import button_pressed_name


class SceneBase:
    def __init__(self, screen):
        self.screen = screen
        self.next = self
        self.PointerImg = Cursor(constants.cursor_image_path, [0, 0])
        self.background = Background(constants.background_image_path, [0, 0], self.screen)
        self.sound_button = SoundButton(self.screen)
        self.SpriteGroupUnactive = pygame.sprite.Group(self.background) 
        self.SpriteGroupActive = pygame.sprite.Group(self.sound_button)
        self.SpritePointer = pygame.sprite.Group(self.PointerImg)

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                button_pressed = button_pressed_name(self.SpriteGroupActive, pos[0]-10, pos[1]-50)
                if button_pressed:
                    if button_pressed == 'SoundButton':
                        self.sound_button.changeSound()

    def Update(self):
        print("uh-oh, you didn't override this in the child class")

    def Render(self, screen):
        position_of_mouse = pygame.mouse.get_pos()
        self.PointerImg.Update(position_of_mouse)
        self.SpriteGroupUnactive.draw(screen)
        self.SpriteGroupActive.draw(screen)
        self.SpritePointer.draw(screen)

    def SwitchToScene(self, next_scene):
        self.next = next_scene
    
    def Terminate(self):
        self.SwitchToScene(None)
