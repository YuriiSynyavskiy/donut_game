import pygame
from scenes.basic_scene import SceneBase


class HowToPlayScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.SpriteGroupUnactive = pygame.sprite.Group(self.background) 
        self.SpriteGroupActive = pygame.sprite.Group(self.sound_button)
        self.SpritePointer = pygame.sprite.Group(self.PointerImg)
    def ProcessInput(self, events, pressed_keys):
        pass
        
    def Update(self):
        pass
    
    def Render(self, screen):
        
        position_of_mouse = pygame.mouse.get_pos()
        self.PointerImg.Update(position_of_mouse)
        self.SpriteGroupUnactive.draw(screen)
        self.SpriteGroupActive.draw(screen)
        self.SpritePointer.draw(screen)
