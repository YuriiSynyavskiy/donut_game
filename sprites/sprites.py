import os
import pygame
import constants


class GameLogo(pygame.sprite.Sprite):
    def __init__(self, image_file, screen):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left = (screen.width/2) - (int(self.rect.right/2))    # Move object to center
        self.rect.top = screen.height * 0.05                            # Move object down on 5% from screen's size

    def __str__(self):
        return 'Logo'


class Cursor(pygame.sprite.Sprite):
    def __init__(self, image_file, screen):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = screen

    def __str__(self):
        return 'Cursor'

    def Update(self, position_of_mouse):
        self.rect.center  = (position_of_mouse[0] + 20, position_of_mouse[1] + 60)


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location, screen):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        loaded_image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(loaded_image, screen.get_screen())
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

    def __str__(self):
        return 'Background'


class BigDonut(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
    def __str__(self):
        return 'BigDonut'


class BigDonutShadow(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
    def __str__(self):
        return 'BigDonutShadow'


class PlayButton(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
    def __str__(self):
        return 'PlayButton'


class HowToPlayButton(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
    def __str__(self):
        return 'HowToPlayButton'


class SoundButton(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        if os.environ.get('ACTIVE_SOUND', ''):
            self.image = pygame.image.load(constants.sound_on_image_path)
        else:
            self.image  = pygame.image.load(constants.sound_off_image_path)
        self.rect = self.image.get_rect()
        self.rect.left = screen.height*0.05
        self.rect.top = screen.height*0.05

    def __str__(self):
        return 'SoundButton'

    def changeSound(self):
        if os.environ.get('ACTIVE_SOUND', ''):
            os.environ['ACTIVE_SOUND']=''
            pygame.mixer.music.pause()
            self.image  = pygame.image.load(constants.sound_off_image_path)
        else:
            os.environ['ACTIVE_SOUND']='Active'    
            pygame.mixer.music.unpause()
            self.image  = pygame.image.load(constants.sound_on_image_path)

class ReturnButton(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
    def __str__(self):
        return 'ReturnButton'

class Donut(pygame.sprite.Sprite):
    def __init__(self, image_file, location, i, j, type_of_donut):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.start_pos_top = self.rect.top
        self.start_pos_left = self.rect.left
        self.pos_x_in_matrix = i
        self.pos_y_in_matrix = j
        self.color_index = type_of_donut
        self.free_space_under = 0
    def update(self):
        self.rect.top += 10
    def __str__(self):
        return 'Donut'
    def move(self, change_of_x = 0, change_of_y = 0):
        self.rect.top+=change_of_y
        self.rect.left+=change_of_x
    def current_pos(self):
        return (self.rect.left, self.rect.top)