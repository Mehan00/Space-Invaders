# okno główne
import pygame, os
SIZESCREEN = WIDTH, HEIGHT = 1366, 740


# kolory
DARKGREEN = pygame.color.THECOLORS['darkgreen']
LIGHTBLUE = pygame.color.THECOLORS['lightblue']


screen = pygame.display.set_mode(SIZESCREEN)

# grafika  - wczytywanie grafik
path = os.path.join(os.pardir, 'images')
path1 = os.path.join(os.pardir, 'sounds')

file_names = sorted(os.listdir(path))
file_names.remove('background.jpg')
BACKGROUND = pygame.image.load(os.path.join(path, 'background.jpg')).convert()
for file_name in file_names:
    image_name = file_name[:-4].upper()
    globals().__setitem__(image_name, pygame.image.load(
        os.path.join(path, file_name)).convert_alpha(BACKGROUND))


ENEMY_LIST = [EN1_1, EN1_2, EXPLO_1]
ENEMY_LIST2 = [EN2_1, EN2_2, EXPLO_1]
ENEMY_LIST3 = [EN3_1, EN3_2, EXPLO_1]
SHIELD_LIST = [SH1, SH2, SH2]
