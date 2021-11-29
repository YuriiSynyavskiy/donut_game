import pygame, os
from scenes.basic_scene import SceneBase
from sprites.sprites import GameLogo, HowToPlayButton, PlayButton, BigDonut, BigDonutShadow, ReturnButton, Donut
import constants
from utils.utils import button_pressed_name, donut_pressed, get_indexes_of_donut, is_in_bounds, check_for_possible_matches, column_of_matrix_by_index 
import random


##################################################################################################################
class TitleScene(SceneBase):



    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                button_pressed = button_pressed_name(self.SpriteGroupActive, pos[0]-10, pos[1]-50)
                if button_pressed:
                    if button_pressed == 'SoundButton':
                        self.sound_button.changeSound()
                    elif button_pressed == 'HowToPlayButton':
                        self.SwitchToScene(HowToPlayScene())
                    elif button_pressed == 'PlayButton':
                        self.SwitchToScene(GameScene())
                        
                        
    def Update(self):
        pass
    
    def Render(self, screen):
       
        position_of_mouse = pygame.mouse.get_pos()
        self.PointerImg.Update(position_of_mouse)
        self.SpriteGroupUnactive.draw(screen)
        self.SpriteGroupActive.draw(screen)
        self.SpritePointer.draw(screen)



##################################################################################################################
class HowToPlayScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.return_button = ReturnButton(constants.return_image_path, [100,100])
        self.SpriteGroupUnactive = pygame.sprite.Group(self.background) 
        self.SpriteGroupActive = pygame.sprite.Group(self.sound_button, self.return_button)
        self.SpritePointer = pygame.sprite.Group(self.PointerImg)
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                button_pressed = button_pressed_name(self.SpriteGroupActive, pos[0]-10, pos[1]-50)
                if button_pressed:
                    if button_pressed == 'SoundButton':
                        self.sound_button.changeSound()
                    elif button_pressed == 'ReturnButton':
                        self.SwitchToScene(TitleScene())
        
    def Update(self):
        pass
    
    def Render(self, screen):
        
        position_of_mouse = pygame.mouse.get_pos()
        self.PointerImg.Update(position_of_mouse)
        self.SpriteGroupUnactive.draw(screen)
        self.SpriteGroupActive.draw(screen)
        self.SpritePointer.draw(screen)



##############################################################################################################################################################################################
class GameScene(SceneBase):
    
    def __init__(self):
        SceneBase.__init__(self)
        self.check_donut = Donut(constants.red_donut_image_path, [200,200], -1, -1, -1)
        self.matches = []
        self.SpriteGroupUnactive = pygame.sprite.Group(self.background) 
        self.SpriteGroupActive = pygame.sprite.Group(self.sound_button)
        self.regeneratedArrayGroup = pygame.sprite.Group() 
        self.donutsFromUpToDOwnGroup  = pygame.sprite.Group()
        self.start_pos_y = {}
        self.index_x_donut1 = -1
        self.index_y_donut1 = -1
        self.index_x_donut2 = -1
        self.index_y_donut2 = -1
        self.activeDonut1 = None
        self.activeDonut2 = None
        self.startAnimation = True
        self.animationOfSwap = False
        self.animation_of_generation = False
        self.animation_of_X = 0 
        self.animation_of_Y = 0 
        self.back_swap = False
        self.count_of_animation = 0
        self.SpritePointer = pygame.sprite.Group(self.PointerImg)
        
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                pressed_donut = donut_pressed(self.DonutGroup, pos)    
                button_pressed = button_pressed_name(self.SpriteGroupActive, pos[0], pos[1])
                if pressed_donut and not self.activeDonut1:

                    self.activeDonut1 = pressed_donut

                elif button_pressed:
                    if button_pressed == 'SoundButton':
                        self.sound_button.changeSound()
                
                                           

    def Update(self):
        if self.startAnimation:
            if self.check_donut.rect.top - self.check_donut.start_pos_top < 400:
                self.check_donut.update()
                self.DonutGroup.update()
            else:
                self.startAnimation=False
                self.matches = check_for_possible_matches(self.DonutGroupArray)
                if self.matches:
                    self.count_of_animation = 0
                    self.check_donut = Donut(constants.red_donut_image_path, [200,200], -1, -1, -1)

                    self.destroy_and_regenarate()
                       
                    self.animation_of_generation = True

                    self.animationOfSwap = False
                    self.matches = []
        if self.animation_of_generation:
            for donut in self.donutsFromUpToDOwnGroup:
                if donut.rect.top<self.start_pos_y[str(donut.pos_x_in_matrix)+str(donut.pos_y_in_matrix)]+ 100*donut.free_space_under:              # FIND ARRAY WITH SAME INDEX AND CHECK IF CURRENT POS < START POS + 100*free_under_space
                    donut.update()          #
            if self.check_donut.rect.top - self.check_donut.start_pos_top < 400:
                self.check_donut.update()
                self.regeneratedArrayGroup.update()
                
            else:
                self.animation_of_generation=False
                self.regeneratedArrayGroup.empty()
                for donut in self.donutsFromUpToDOwnGroup:
                    donut.free_space_under = 0
                self.donutsFromUpToDOwnGroup.empty()
                self.matches = check_for_possible_matches(self.DonutGroupArray)
                if self.matches:
                    self.count_of_animation = 0
                    self.check_donut = Donut(constants.red_donut_image_path, [200,200], -1, -1, -1)

                    self.destroy_and_regenarate()
                       
                    self.animation_of_generation = True

                    self.animationOfSwap = False
                    self.matches = []  

        if self.animationOfSwap:
            if self.count_of_animation < 100:
                self.count_of_animation+=5
                self.activeDonut1.move(self.animation_of_X*(-1), self.animation_of_Y*(-1))
                self.activeDonut2.move(self.animation_of_X, self.animation_of_Y)
            elif self.back_swap:
                self.count_of_animation = 0
                self.animationOfSwap = False
                self.back_swap = False
                self.activeDonut1 = None
                self.activeDonut2 = None   
                self.animation_of_X = 0 
                self.animation_of_Y = 0 
            else:
                self.matches = check_for_possible_matches(self.DonutGroupArray)
                if self.matches:
                    self.count_of_animation = 0
                    self.check_donut = Donut(constants.red_donut_image_path, [200,200], -1, -1, -1)

                    self.destroy_and_regenarate()
                       
                    self.animation_of_generation = True

                    self.animationOfSwap = False
                    self.activeDonut1 = None
                    self.activeDonut2 = None  
                    self.matches = []

                else:
                    self.count_of_animation = 0
                    self.animation_of_X,self.animation_of_Y = (self.activeDonut1.rect.left - self.activeDonut2.rect.left)/20, (self.activeDonut1.rect.top - self.activeDonut2.rect.top)/20
                    self.swapDonuts()
                    self.back_swap = True
        
        elif self.activeDonut1 and self.activeDonut2:
            self.activeDonut1, self.activeDonut2 = self.activeDonut2, self.activeDonut1
            self.swapDonuts()
            self.animation_of_X, self.animation_of_Y = (self.activeDonut1.rect.left - self.activeDonut2.rect.left)/20, (self.activeDonut1.rect.top - self.activeDonut2.rect.top)/20
            self.animationOfSwap = True
           
                               
            
        if self.activeDonut1 and self.animationOfSwap == False:
            
            position_of_mouse = pygame.mouse.get_pos()
            index_in_array_x = (position_of_mouse[0] - 200)/100
            index_in_array_y = (position_of_mouse[1] - 200)/100
            if is_in_bounds(index_in_array_x, index_in_array_y):
                tempY, tempX = get_indexes_of_donut(self.activeDonut1)
                #print(f'IndexInArrayX, IndexInArrayXY - {int(index_in_array_x)}{int(index_in_array_y)}')
                if abs(int(index_in_array_x) - tempX) + abs(int(index_in_array_y) - tempY) == 1:
                    self.activeDonut2 = self.DonutGroupArray[int(index_in_array_y)][int(index_in_array_x)]
                    
                elif abs(int(index_in_array_x) - tempX) + abs(int(index_in_array_y) - tempY)>1:
                    self.activeDonut1 = None
            else:
                self.activeDonut1 = None
       
    def Render(self, screen):
        position_of_mouse = pygame.mouse.get_pos()
        self.PointerImg.Update(position_of_mouse)
        self.SpriteGroupUnactive.draw(screen)
        self.SpriteGroupActive.draw(screen)
        self.DonutGroup.draw(screen)
        self.SpritePointer.draw(screen)
    def swapDonuts(self):
        #print(f"Donut1: X, Y    -  {self.activeDonut1.pos_x_in_matrix}  {self.activeDonut1.pos_y_in_matrix}")
        #print(f"Donut2: X, Y    -  {self.activeDonut2.pos_x_in_matrix}  {self.activeDonut2.pos_y_in_matrix}")
        donut1X= self.activeDonut1.pos_x_in_matrix
        donut1Y= self.activeDonut1.pos_y_in_matrix
        donut2X= self.activeDonut2.pos_x_in_matrix
        donut2Y= self.activeDonut2.pos_y_in_matrix
        self.DonutGroupArray[donut1X][donut1Y], self.DonutGroupArray[donut2X][donut2Y] = self.DonutGroupArray[donut2X][donut2Y], self.DonutGroupArray[donut1X][donut1Y]
        
        self.DonutGroupArray[donut1X][donut1Y].pos_x_in_matrix = donut1X
        self.DonutGroupArray[donut1X][donut1Y].pos_y_in_matrix = donut1Y

        self.DonutGroupArray[donut2X][donut2Y].pos_x_in_matrix = donut2X
        self.DonutGroupArray[donut2X][donut2Y].pos_y_in_matrix = donut2Y
    def kill_matches(self):
        for i in self.matches:
            for j in i:
                if self.DonutGroupArray[j.pos_x_in_matrix][j.pos_y_in_matrix]:
                    self.DonutGroupArray[j.pos_x_in_matrix][j.pos_y_in_matrix].kill()
                    self.DonutGroupArray[j.pos_x_in_matrix][j.pos_y_in_matrix] = None
        
    def regenerate_array(self):
        startX = 200
        startY = 300
        i = 5; j = 0
        while i>=0:
            while j<=5:
                if not self.DonutGroupArray[i][j]:
                    rand_index  = random.randint(0, 5)
                    temp_donut = Donut(self.ARRAY_OF_DONUTS[rand_index], [startX, startY], i, j, rand_index)
                    self.DonutGroup.add(temp_donut)
                    self.DonutGroupArray[i][j]=temp_donut
                    self.regeneratedArrayGroup.add(temp_donut)
                startX+=100
                j+=1
            i-=1; j=0
            startX= 200
            startY-=100
    def down_upper_donuts(self):
        i = 0; j = 0
        while i < len(self.DonutGroupArray):
            temp_column = column_of_matrix_by_index(self.DonutGroupArray, i)[::-1]
            while j<len(temp_column)-1:
                temp_j = j
                check = 1
                while (not temp_column[temp_j]) and (temp_column[temp_j+1]):
                    if check:
                        self.donutsFromUpToDOwnGroup.add(temp_column[temp_j+1])
                        check = 0
                    temp_column[temp_j+1].free_space_under+=1    
                    temp_column[temp_j+1].pos_x_in_matrix+=1
                    temp_column[temp_j], temp_column[temp_j+1] = temp_column[temp_j+1], temp_column[temp_j]
                    temp_j-=1
                check = 1                  
                j+=1 
            temp_counter = 0    
            for elem in temp_column[::-1]:
                self.DonutGroupArray[temp_counter][i]=elem
                temp_counter+=1 
            i+=1; j=0
        
    def destroy_and_regenarate(self):
        self.kill_matches()  
        self.down_upper_donuts()
        self.start_pos_y = {}
        for i in self.donutsFromUpToDOwnGroup:
            self.start_pos_y[str(i.pos_x_in_matrix)+str(i.pos_y_in_matrix)] = i.rect.top
        self.regenerate_array()