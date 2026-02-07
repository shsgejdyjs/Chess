import pygame
import board
import pieces
from collections import deque

b = board.Board()


k = b.kings["White"]

k.set_direction()


p = b.find_piece((0,1))

print(p.movement())
print(p.valid_moves())

