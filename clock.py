import pygame
import io
from constants import *


pygame.init()
window = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()


class s(pygame.sprite.Sprite):
    def __init__(self, size):
        pygame.sprite.Sprite.__init__(self)
        self.image= pygame.surface.Surface((50,200), pygame.SRCALPHA)
        self.image.blit(load_and_scale_svg('assets/wQ.svg', size), (0,0))
        self.rect = self.image.get_rect()
    def update(self):
        self.image = pygame.surface.Surface((50,200), pygame.SRCALPHA)
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image.blit(load_and_scale_svg('assets/wQ.svg', 1.4), (0,0))
            
            
        else:
            self.image.blit(load_and_scale_svg('assets/wQ.svg', 1), (0,0))


run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    window.fill((127, 127, 127))
    a = s(1)
    b = pygame.sprite.Group()
    b.add(a)
    b.update()
    b.draw(window)
    window.blit(c, (0,0))
    pygame.display.flip()

pygame.quit()
exit()
