import pieces
import pygame
import os
from constants import *

class Square(pygame.sprite.Sprite):
    highlight = False
    hover = False
    outline = False
    def __init__(self, coord, board_length, colour):
        pygame.sprite.Sprite.__init__(self)
        self.length = board_length
        self.colour = colour
        self.coord = coord
        self.image = pygame.Surface((board_length/8, board_length/8), pygame.SRCALPHA)
        self.image.fill((*colour, 255))
        self.rect = self.image.get_rect()
        self.rect.center = self.coord.convert((0,0), board_length)

        
        
    def update(self, surface):
        surface.blit(self.image, self.rect)

        if self.hover:
            self.rectangle = pygame.Surface((self.length/8, self.length/8), pygame.SRCALPHA)
            pygame.draw.rect(self.rectangle, self.hover, self.rectangle.get_rect())

            surface.blit(self.rectangle, self.rect)
        
        elif self.outline:
            self.rectangle = pygame.Surface((self.length/8, self.length/8), pygame.SRCALPHA)
            pygame.draw.rect(self.rectangle,self.outline, self.rectangle.get_rect(),3 )
            surface.blit(self.rectangle, self.rect)

        elif self.highlight:
            self.circle = pygame.Surface((self.length/8, self.length/8), pygame.SRCALPHA)
            pygame.draw.circle(self.circle, (0,128,0,200) ,(self.length/16, self.length/16), self.length/48 )

            surface.blit(self.circle,self.rect)
            
        
            

class Board():
    def __init__(self, Pieces = None, length = 400):
        self.piece_sprites = pygame.sprite.Group()
        self.squares = pygame.sprite.Group()
        self.length = length
        for i in range(8):
            for j in range(8):
                colour = (200,157,124) if (i+j)%2 == 0 else (237,232,208)
                square = Square(pieces.Coordinate((i,j)), length, colour)
                self.squares.add(square)
                
                
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
        self.knights = {"White":[], "Black":[]}
        for coord in self.Pieces:
            if (piece := self.Pieces[coord]).name == "K":
                self.kings[piece.colour] = piece
            elif piece.name == "N":
                self.knights[piece.colour].append(piece)

        for coord in self.Pieces:
            if (piece := self.Pieces[coord]):
                piece.set_king(self.kings[piece.colour])
                self.piece_sprites.add(piece)
                piece.set_board(self)
                
                
    

    
    
    def find_piece(self, coordinate) -> pieces.Piece:
        return self.Pieces[coordinate]  
    
    def highlight_squares(self, coords, piece_coord):
        for square in self.squares:
            if square.coord == piece_coord:
                square.hover = (0,0,200,200)
            elif self.find_piece(square.coord) and square.coord in coords:
                square.outline = (0,128,0,255)
            elif square.coord in coords:
                square.highlight = (0,0,128,128)
            else:
                square.highlight = False
    def unhighlight_squares(self):
        for square in self.squares:
            square.hover = False
            square.highlight = False
            square.outline = False

    def move_piece(self, piece: pieces.Piece, new):
        piece.moved = True
        
        if piece.name == "P" and abs((new - piece.coord)[1]) == 2:
            piece.moved_twice = True
        
        for p in self.Pieces.values():
            if piece.colour == p.colour and p.name == "P" and p != piece:
                p.moved_twice = False

        
        if piece.name == "P" and abs((new-piece.coord)[0]) ==1 and not self.Pieces[new]:
            
            direction = 1 if piece.colour == "White" else -1
            c = new + (0, -direction)
            p = self.Pieces[c]
            self.Pieces[c] = pieces.None_piece(c, self)
            self.piece_sprites.remove(p)

        if piece.name == "K" and abs(diff:=(new-piece.coord)[0]) >= 2:
            c = 7 if diff > 0 else 0
            
            rook = self.Pieces[(c,piece.coord[1])]
            self.move_piece(rook, piece.coord + (int(diff/abs(diff)),0))
            if abs(diff) > 2:
                    k = 2 if diff > 0 else -2
                    new = piece.coord + (k,0)



        self.Pieces[piece.coord] = pieces.None_piece(piece.coord.coord, self)
        self.piece_sprites.remove(self.Pieces[new])
        for k in self.knights:
            for knight in self.knights[k]:
                if self.Pieces[new] == knight:
                    self.knights[k].remove(knight)
        # if piece.pinned and self.Pieces[new].attacking:
        #     piece.pinned = False
        
        self.Pieces[new] = piece
        self.Pieces[new].rect.center = new.convert((0,0), self.length)
        piece.coord.coord = new

        if not piece.king:
            piece.set_king(self.kings[piece.colour])
        # if not self.piece_sprites.has(piece):
        self.piece_sprites.add(piece)
        

        

    
    def __repr__(self):
        out = ""
        for j in range(8):
            out += "|".join([self.Pieces[i,7-j].__repr__() for i in range(8)]) + "\n"
        return out

