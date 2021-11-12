import pygame
import random
import constants
from sprites.sprites import Cursor, Background, SoundButton, Donut


class SceneBase:
    def __init__(self, screen):
        self.screen = screen
        self.DonutGroupArray = [[None, None, None, None, None, None], 
                                [None, None, None, None, None, None],
                                [None, None, None, None, None, None],
                                [None, None, None, None, None, None],
                                [None, None, None, None, None, None],
                                [None, None, None, None, None, None]]
        self.ARRAY_OF_DONUTS = [constants.red_donut_image_path,
                       constants.blue_donut_image_path,
                       constants.green_donut_image_path,
                       constants.sblue_donut_image_path,
                       constants.yellow_donut_image_path,
                       constants.pink_donut_image_path]
        self.next = self
        self.PointerImg = Cursor(constants.cursor_image_path, [0, 0])
        self.background = Background(constants.background_image_path, [0, 0], self.screen)
        self.sound_button = SoundButton(self.screen)

        self.DonutGroup = pygame.sprite.Group()
        startX = 200
        startY = 300
        i = 5; j = 0
        while i>=0:
            while j<=5:
                rand_index  = random.randint(0, 5)
                temp_donut = Donut(self.ARRAY_OF_DONUTS[rand_index], [startX, startY], i, j, rand_index)
                self.DonutGroup.add(temp_donut)
                self.DonutGroupArray[i][j]=temp_donut
                startX+=100
                j+=1
            i-=1; j=0
            startX= 200
            startY-=100

    def ProcessInput(self, events, pressed_keys):
        print("uh-oh, you didn't override this in the child class")

    def Update(self):
        print("uh-oh, you didn't override this in the child class")

    def Render(self, screen):
        print("uh-oh, you didn't override this in the child class")

    def SwitchToScene(self, next_scene):
        self.next = next_scene
    
    def Terminate(self):
        self.SwitchToScene(None)
