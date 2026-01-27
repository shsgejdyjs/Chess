import pygame
import board


b = board.Board()

rook = b.find_piece((0,0))
king = b.kings["White"]

k = b.find_piece((1,0))
print(rook.bdiagonal())
print(k.bdiagonal())

