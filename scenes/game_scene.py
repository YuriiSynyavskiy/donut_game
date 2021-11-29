from os import close
import pygame
import random
from sprites.sprites import Donut
from scenes.basic_scene import SceneBase
from utils.donuts import ARRAY_OF_DONUTS
from utils.utils import check_for_possible_matches, donut_pressed, close_to_active_donut


class GameScene(SceneBase):
    def __init__(self, screen):
        SceneBase.__init__(self, screen)

        self.count_of_donuts = 6

        # Empty array of donuts
        self.DonutGroupArray = [[None for j in range(self.count_of_donuts)] for i in range(self.count_of_donuts)]
        
        # Donut group for dispayinh
        self.DonutGroup = pygame.sprite.Group()

        donut_size = Donut(ARRAY_OF_DONUTS[0], [0, 0], 0, 0, 0).image.get_size()
        #import pdb; pdb.set_trace()
        x_width = (self.count_of_donuts) * donut_size[0]

        self.start_of_donuts_x = int((screen.width - x_width) / 2)
        start_x = self.start_of_donuts_x

        startY = 300

        # Generating of donuts
        i = self.count_of_donuts - 1
        j = 0
        while i >= 0:
            while j <= self.count_of_donuts-1:
                rand_index  = random.randint(0, 5)
                temp_donut = Donut(ARRAY_OF_DONUTS[rand_index], [start_x, startY], i, j, rand_index)
                self.DonutGroup.add(temp_donut)
                self.DonutGroupArray[i][j]=temp_donut
                start_x += donut_size[0]
                j += 1
            i -= 1
            j = 0
            start_x = self.start_of_donuts_x
            startY -= donut_size[1]
        
        # Dropping of donuts animation
        self.animation_of_generation = True
        self.animation_of_swap = False

        self.step = 10

        # Swap
        self.active_donut_1 = None
        self.active_donut_2 = None
        self.number_of_animations = 20
        self.swap_step = donut_size[0] / self.number_of_animations


    def ProcessInput(self, events, pressed_keys):
        super().ProcessInput(events, pressed_keys)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and not self.animation_of_generation and not self.animation_of_swap:
                pos = pygame.mouse.get_pos()

                pressed_donut = donut_pressed(self.DonutGroup, pos)
                if pressed_donut and not self.active_donut_1:
                    self.active_donut_1 = pressed_donut

    def Update(self):
        # Animation of generation
        if self.animation_of_generation:
            if self.DonutGroupArray[self.count_of_donuts - 1][self.count_of_donuts - 1].rect.top < self.screen.height * 0.8:
                self.DonutGroup.update(self.step)
            else:
                self.animation_of_generation = False

        # Animation of swap
        if self.animation_of_swap:
            if self.number_of_animations > 0:

                change_y = self.active_donut_1.pos_x_in_matrix - self.active_donut_2.pos_x_in_matrix
                change_x = self.active_donut_1.pos_y_in_matrix - self.active_donut_2.pos_y_in_matrix

                self.active_donut_1.move((-1) * change_x * self.swap_step, (-1) * change_y * self.swap_step)
                self.active_donut_2.move(change_x * self.swap_step, change_y * self.swap_step)

                self.number_of_animations -= 1

            else:
                self.swap_donuts()
                matches = check_for_possible_matches(self.DonutGroupArray)
                if len(matches):
                    self.active_donut_1 = None
                    self.active_donut_2 = None
                    self.animation_of_swap = False
                else:
                    self.number_of_animations = 20
        
        # Waiting for selected second donut for swap
        if self.active_donut_1 and not self.active_donut_2:
            
            position_of_mouse = pygame.mouse.get_pos()
            potential_second_donut = donut_pressed(self.DonutGroup, position_of_mouse)

            if potential_second_donut and \
                (not self.active_donut_1.pos_x_in_matrix == potential_second_donut.pos_x_in_matrix or \
                 not self.active_donut_1.pos_y_in_matrix == potential_second_donut.pos_y_in_matrix):

                if close_to_active_donut(self.active_donut_1, potential_second_donut):
                    self.active_donut_2 = potential_second_donut
                    self.animation_of_swap = True
                    self.number_of_animations = 20

                else:
                    self.active_donut_1 = None

    def Render(self, screen):
        super().Render(screen)
        self.DonutGroup.draw(screen)
        position_of_mouse = pygame.mouse.get_pos()
        self.PointerImg.Update(position_of_mouse)
        self.SpritePointer.draw(screen)

    def swap_donuts(self):
        donut1X= self.active_donut_1.pos_x_in_matrix
        donut1Y= self.active_donut_1.pos_y_in_matrix
        donut2X= self.active_donut_2.pos_x_in_matrix
        donut2Y= self.active_donut_2.pos_y_in_matrix
        self.DonutGroupArray[donut1X][donut1Y], self.DonutGroupArray[donut2X][donut2Y] = self.DonutGroupArray[donut2X][donut2Y], self.DonutGroupArray[donut1X][donut1Y]
        
        self.DonutGroupArray[donut1X][donut1Y].pos_x_in_matrix = donut1X
        self.DonutGroupArray[donut1X][donut1Y].pos_y_in_matrix = donut1Y

        self.DonutGroupArray[donut2X][donut2Y].pos_x_in_matrix = donut2X
        self.DonutGroupArray[donut2X][donut2Y].pos_y_in_matrix = donut2Y