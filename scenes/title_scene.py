import pygame
from scenes.basic_scene import SceneBase
from sprites.sprites import GameLogo, HowToPlayButton, PlayButton, BigDonut, BigDonutShadow
import constants
from utils.utils import button_pressed_name
from scenes.howtoplay_scene import HowToPlayScene
from scenes.game_scene import GameScene


class TitleScene(SceneBase):
    def __init__(self, screen):
        SceneBase.__init__(self, screen)
        self.game_logo = GameLogo(constants.game_logo_path, self.screen)
        self.big_donut_shadow = BigDonutShadow(constants.big_donut_shadow_path, self.screen)
        self.big_donut = BigDonut(constants.big_donut_path, self.screen)
        self.how_to_play_button = HowToPlayButton(constants.how_to_play_image_path, self.screen)
        self.play_button = PlayButton(constants.play_image_path, self.screen)

        self.SpriteGroupUnactive.add(self.game_logo)
        self.SpriteGroupUnactive.add(self.big_donut_shadow)
        self.SpriteGroupUnactive.add(self.big_donut)
        self.SpriteGroupActive.add(self.play_button)
        self.SpriteGroupActive.add(self.how_to_play_button)

    def ProcessInput(self, events, pressed_keys):
        super().ProcessInput(events, pressed_keys)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                button_pressed = button_pressed_name(self.SpriteGroupActive, pos[0]-10, pos[1]-50)
                if button_pressed:
                    if button_pressed == 'HowToPlayButton':
                        self.SwitchToScene(HowToPlayScene(self.screen))
                    elif button_pressed == 'PlayButton':
                        self.SwitchToScene(GameScene(self.screen))

    def Update(self):
        pass
    
    def Render(self, screen):
        # For the sake of brevity, the title scene is a blank red screen
        super().Render(screen)
