import pygame
from scenes.basic_scene import SceneBase
from sprites.sprites import GameLogo, HowToPlayButton, PlayButton, BigDonut, BigDonutShadow
import constants
from utils.utils import button_pressed_name
from scenes.howtoplay_scene import HowToPlayScene
from scenes.gamescene import GameScene


class TitleScene(SceneBase):
    def __init__(self, screen):
        SceneBase.__init__(self, screen)
        self.game_logo = GameLogo(constants.game_logo_path, self.screen)
        self.big_donut_shadow = BigDonutShadow(constants.big_donut_shadow_path, self.screen)
        self.big_donut = BigDonut(constants.big_donut_path, self.screen)
        self.how_to_play_button = HowToPlayButton(constants.how_to_play_image_path, self.screen)
        self.play_button = PlayButton(constants.play_image_path, self.screen)

        self.SpriteGroupUnactive = pygame.sprite.Group(self.background, self.game_logo, self.big_donut_shadow, self.big_donut)
        self.SpriteGroupActive = pygame.sprite.Group(self.sound_button, self.play_button, self.how_to_play_button)

        self.SpritePointer = pygame.sprite.Group(self.PointerImg)

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                button_pressed = button_pressed_name(self.SpriteGroupActive, pos[0]-10, pos[1]-50)
                if button_pressed:
                    if button_pressed == 'SoundButton':
                        self.sound_button.changeSound()
                    elif button_pressed == 'HowToPlayButton':
                        self.SwitchToScene(HowToPlayScene(self.screen))
                    elif button_pressed == 'PlayButton':
                        self.SwitchToScene(GameScene())

    def Update(self):
        pass
    
    def Render(self, screen):
        # For the sake of brevity, the title scene is a blank red screen
        position_of_mouse = pygame.mouse.get_pos()
        self.PointerImg.Update(position_of_mouse)
        self.SpriteGroupUnactive.draw(screen)
        self.SpriteGroupActive.draw(screen)
        self.SpritePointer.draw(screen)
