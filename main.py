import pygame
import board
import pieces

pygame.init()
screen = pygame.display.set_mode((1280,720), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True
b = board.Board()
b.all_sprites.add(b.find_piece((0,0)))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill("white")
    screen.blit(b.surface, (20,20))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()