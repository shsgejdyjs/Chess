import os
import pygame
import io

GAME_FOLDER = os.path.dirname(__file__)

def load_and_scale_svg(filename, scale):
    svg_string = open(filename, "rt").read()    
    svg_string = svg_string[:5] + f'width="{45*scale}" height="{45*scale}"' + svg_string[4:]
    return  pygame.image.load(io.BytesIO(svg_string.encode()))




