import board
import os
import pygame



class game():
    def __init__(self):
        self.Board = board.Board()
        self.start = "White"

    def move_piece(self):
        c = input()
        coord = (int(c[0]), int(c[1]))

        if (piece:=self.Board.find_piece(coord)):
            print("TRUE")
            c = input()
            coord = (int(c[0]), int(c[1]))
            print(piece.valid_moves())
            if coord in piece.valid_moves():
                os.system("clear")
                self.Board.move_piece(piece, coord)
                print(self.Board)

g = game()
while True:
    g.move_piece()
    
