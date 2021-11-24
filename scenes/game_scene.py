import pygame
import random
from sprites.sprites import Donut
from scenes.basic_scene import SceneBase
from utils.donuts import ARRAY_OF_DONUTS


class GameScene(SceneBase):
    def __init__(self, screen):
        SceneBase.__init__(self, screen)

        # Generating of donuts
        self.DonutGroupArray = [[None, None, None, None, None, None],
                                [None, None, None, None, None, None],
                                [None, None, None, None, None, None],
                                [None, None, None, None, None, None],
                                [None, None, None, None, None, None],
                                [None, None, None, None, None, None]]
        self.DonutGroup = pygame.sprite.Group()
        startX = 200
        startY = 300
        i = 5; j = 0
        while i>=0:
            while j<=5:
                rand_index  = random.randint(0, 5)
                temp_donut = Donut(ARRAY_OF_DONUTS[rand_index], [startX, startY], i, j, rand_index)
                self.DonutGroup.add(temp_donut)
                self.DonutGroupArray[i][j]=temp_donut
                startX+=100
                j+=1
            i-=1; j=0
            startX= 200
            startY-=100
    def ProcessInput(self, events, pressed_keys):
        super().ProcessInput(events, pressed_keys)
        
    def Update(self):
        pass
    
    def Render(self, screen):
        super().Render(screen)
        #position_of_mouse = pygame.mouse.get_pos()
        #self.PointerImg.Update(position_of_mouse)
        self.DonutGroup.draw(screen)
        #self.SpriteGroupActive.draw(screen)
        #self.SpritePointer.draw(screen)
