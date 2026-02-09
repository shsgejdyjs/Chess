import pieces
import pygame
import os
from constants import *

class Board():
    def __init__(self, Pieces = None):
        self.all_sprites = pygame.sprite.Group()
        
        self.surface = pygame.Surface((400,400))
        self.surface.fill("white")
        for i in range(8):
            for j in range(8):
                if (i + j)%2 == 0:
                    pygame.draw.rect(self.surface, "black", pygame.Rect(i*50, j*50, 50,50))
        
        
        if Pieces == None:
            #initialises a dictionary with no pieces
            self.Pieces = {(i,j): pieces.None_piece((i,j), self) for i in range(8) for j in range(8)}
            
            #white pawns
            for i in range(8):
                self.Pieces[i,1] = pieces.Pawn("White", (i,1), self)
            
            #black pawns
            for i in range(8):
                self.Pieces[i,6] = pieces.Pawn("Black", (i,6), self)

            #white rooks
            for i in range(0,8,7):
                self.Pieces[i,0] = pieces.Rook("White", (i,0), self)

            #black rooks
            for i in range(0,8,7):
                self.Pieces[i,7] = pieces.Rook("Black", (i,7), self)

            #white knights
            for i in range(1,7,5):
                self.Pieces[i,0] = pieces.Knight("White", (i,0), self)

            #black knights
            for i in range(1,7,5):
                self.Pieces[i,7] = pieces.Knight("Black", (i,7), self)
            
            #white bishops
            for i in range(2,6,3):
                self.Pieces[i,0] = pieces.Bishop("White", (i,0), self)

            #black bishops
            for i in range(2,6,3):
                self.Pieces[i,7] = pieces.Bishop("Black", (i,7), self)

            self.Pieces[4,0] = pieces.King("White", (4,0), self)
            self.Pieces[4,7] = pieces.King("Black", (4,7), self)
            self.Pieces[3,0] = pieces.Queen("White", (3,0), self)
            self.Pieces[3,7] = pieces.Queen("Black", (3,7), self)
            
        else:
            self.Pieces = Pieces

        
        #need to identify the kings
        self.kings = {"White":pieces.King, "Black":pieces.King}
        
        for coord in self.Pieces:
            if (king := self.Pieces[coord]).name == "K":
                self.kings[king.colour] = king

        for coord in self.Pieces:
            if (piece := self.Pieces[coord]):
                piece.set_king(self.kings[piece.colour])
            if piece:
                
                self.surface.blit(piece.image, (((10,360) - piece.coord*(-50,50)).coord))
            
        

    def display_board(self):
        
        pass
    
    def find_piece(self, coordinate) -> pieces.Piece:
        return self.Pieces[coordinate]  

    def move_piece(self, piece: pieces.Piece, new):
        self.Pieces[piece.coord] = pieces.None_piece()
        self.Pieces[new] = piece
        piece.coord.coord = new

    
    def __repr__(self):
        out = ""
        for j in range(8):
            out += "|".join([self.Pieces[i,7-j].__repr__() for i in range(8)]) + "\n"
        return out

