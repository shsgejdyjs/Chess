from __future__ import annotations
from collections import deque
from typing import TYPE_CHECKING
import pygame
import os
from constants import *
if TYPE_CHECKING:
    from board import Board






class Coordinate():
    def __init__(self, coord):
        self.coord = coord
    def __add__(self, other):
        return  Coordinate((self.coord[0] + other[0], self.coord[1] + other[1]))
    def __sub__(self, other):
        return Coordinate((self.coord[0]-other[0], self.coord[1]-other[1]))
    def __rsub__(self, other):
        return Coordinate((other[0]-self.coord[0], other[1] - self.coord[1]))
    def __getitem__(self, i):
        return self.coord[i]
    def __repr__(self):
        return str(self.coord)
    def __setitem__(self, i):
        return Coordinate((self.coord[0] if i[0] == 0 else i[0], self.coord[1] if i[1] == 0 else i[1]))
    def __hash__(self):
        return hash(self.coord)
    def __eq__(self, other):
        if isinstance(other, tuple):
            return self.coord == other
        return NotImplemented
        
    def __lt__(self, other):
        return self.coord[0]**2 + self.coord[1]**2 < other[0]**2 + other[1]**2

    def __mul__(self, other):
        return Coordinate((self.coord[0]*other[0], self.coord[1]*other[1]))

def normalise(vector):
    return (int(abs(vector[0])/vector[0]) if vector[0] else 0, int(abs(vector[1])/vector[1]) if vector[1] else 0)
 
class Piece(pygame.sprite.Sprite):
    name = "a"
    king : King = None
    attacking = False
    pinned = []
    move_direction = []
    valid = []
    def __init__(self, Colour, Coordinates, board, image):
        pygame.sprite.Sprite.__init__(self)
        
        self.colour = Colour
        self.coord = Coordinate(Coordinates)
        self.board : Board = board
        if Colour == "White":
            self.Opposite = "Black"
        else:
            self.Opposite = "White"
        
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(GAME_FOLDER, 'assets', image)).convert_alpha(),(30,30))
        self.rect = self.image.get_rect()
        self.rect.center = ((25,375) - self.coord*(-50,50)).coord

    
    
    def findPiece(self, coord):
        return self.board.find_piece(coord)
        
    
    def __repr__(self):
        colourCode = {"White":"W", "Black":"B", "None":" "}
        return colourCode[self.colour] + self.name
    def vertical(self):

        """down up"""

        up = deque()
        down = deque()
        for i in range(8):
            if i == self.coord[1]:
                continue
            
            piece = self.findPiece((self.coord[0],i))

            
            if i - self.coord[1] > 0:
                up.append(piece)
            else:
                down.appendleft(piece)


    
        return down, up      
    def horizontal(self):

        """left right"""

        left = deque()
        right = deque()

        for i in range(8):
            if i == self.coord[0]:
                continue
            
            piece = self.findPiece((i,self.coord[1]))

            
            if i - self.coord[0] > 0:
                right.append(piece)
            else:
                left.appendleft(piece)

        return left, right
    def bdiagonal(self):
         
        """ne sw"""
        ne = deque()
        sw = deque()

        diff = self.coord[0] - self.coord[1]
        
        xstart = diff if diff > 0 else 0
        ystart = -diff if diff < 0 else 0
        

        for i in range(8-abs(diff)):
            if xstart + i == self.coord[0]:
                continue
            piece = self.findPiece((xstart + i, ystart + i))
            
            if xstart + i > self.coord[0]:
                ne.append(piece)
            else:
                sw.appendleft(piece)

       
        return ne, sw        
    def wdiagonal(self):

        """nw se"""
        nw = deque()
        se = deque()
        total = self.coord[0] + self.coord[1]

        xstart = 0 if total -7 < 0 else total - 7
        ystart = 7 if total -7 > 0 else total

        for i in range(8 - abs(total - 7)):
            if xstart + i == self.coord[0]:
                continue
            piece = self.findPiece((xstart + i, ystart - i))
            
            if xstart + i > self.coord[0]:
                se.append(piece)
            else:
                nw.appendleft(piece)

       
        return nw, se
    
    def set_king(self, k):
        self.king = k   
    def valid_moves(self):
        valid = []
        moves = self.movement()
        
        
        old_distance = self.coord - self.king.coord

        for move in moves:
            #vector from king to the new coord
            new_distance = move - self.king.coord

            if self.king.attacks:
                if (d:=normalise(new_distance)) in self.king.attacks:
                    
                    if new_distance < (self.king.attacks[d].coord -self.king.coord):
                        valid.append(move)
                
            elif self.pinned:
                if not(new_distance[0] * new_distance[1] !=0 and abs(new_distance[0]) != abs(new_distance[1])) and normalise(new_distance) == normalise(old_distance):
                    valid.append(move)
            
            else:
                valid.append(move)
        
        self.valid = valid
        return valid

    
    def movement(self, *possible_directions) -> list:
        moves = []
        
        directions = dict(zip(self.move_direction, (possible_directions)))  
        
        for d in directions:
            
            for piece in directions[d]:
                piece : Piece
                if piece:
                    if piece.colour == self.colour:
                        break
                    elif piece.colour == self.Opposite:
                        moves.append(piece.coord)
                        break
                moves.append(piece.coord)
        return moves
#The none_piece is a dummy piece that represents an empty square.
#This is used to prevent checking if a square comtains a piece every time
class None_piece(Piece):
    name = "X"

    def __bool__(self):
        return False

    def __init__(self, Coordinates, board):
        self.colour = "None"
        self.coord = Coordinates
        self.board = board
      
class Pawn(Piece):
    moved = False
    movedTwice = False
    name = "P"
    def __init__(self, Colour, Coordinates, board):
        image = "white_pawn.png" if Colour == "White" else "black_pawn.png"
        super().__init__(Colour, Coordinates, board, image)
    def movement(self):
        moves = []
        for i in range(-1,2):
            newCoord = self.coord + (i,1)
            if -1 < newCoord[0] < 8:
                if i != 0 and self.findPiece(newCoord).colour == self.Opposite:
                    moves.append(newCoord)
                elif i == 0 and not self.findPiece(newCoord):
                    moves.append(newCoord)
                    if not self.moved and not self.findPiece(newCoord := newCoord + (0,1)):
                        moves.append(newCoord)
                        
        
        for i in range(-1,2,2):
            newCoord = self.coord + (i,0)
            if -1 < newCoord[0] < 8:
                if (piece := self.findPiece(newCoord)).name == "P" and piece.colour == self.Opposite and piece.movedTwice:
                    moves.append(newCoord + (0,1))
        return moves
                
class Rook(Piece):
    name = "R"
    moved = False
    move_direction = [(-1,0),(1,0),(0,-1),(0,1)]
    def __init__(self, Colour, Coordinates, board):
        image = "white_rook.png" if Colour == "White" else "black_rook.png"
        super().__init__(Colour, Coordinates, board, image)
        
        
    def movement(self):
        return super().movement(*self.horizontal(), *self.vertical())

               
    
class Bishop(Piece):
    name = "B"
    move_direction = [(1,1),(-1,-1),(1,-1),(-1,1)]
    def __init__(self, Colour, Coordinates, board):
        image = "white_bishop.png" if Colour == "White" else "black_bishop.png"
        super().__init__(Colour, Coordinates, board, image)

    def movement(self):
        return super().movement(*self.bdiagonal(), *self.wdiagonal())
class Knight(Piece):
    name = "N"
    def __init__(self, Colour, Coordinates, board):
        image = "white_knight.png" if Colour == "white" else "black_knight.png"
        super().__init__(Colour, Coordinates, board, image)

class Queen(Piece):
    name = "Q"
    move_direction = [(1,1),(-1,-1),(1,-1),(-1,1),(-1,0),(1,0),(0,-1),(0,1)]
    def __init__(self, Colour, Coordinates, board):
        image = "white_queen.png" if Colour == "White" else "black_queen.png"
        super().__init__(Colour, Coordinates, board, image)
    def movement(self):
        return super().movement(*self.bdiagonal(), *self.wdiagonal(), *self.horizontal(), *self.vertical() )
class King(Piece):
    name = "K"

    inCheck = False 
    
    attacks = {}

    def __init__(self, Colour, Coordinates, board):
        image = "white_king.png" if Colour == "White" else "black_king.png"
        super().__init__(Colour, Coordinates, board, image)
        
    def check_in_check(self):
        #this needs to check what directions the king is being checked from if any
        
        self.direction = dict(zip([(0,-1), (0,1), (-1,0), (1,0), (1,1), (-1,-1), (-1,1), (1,-1)], (*self.vertical(), *self.horizontal(), *self.bdiagonal(), *self.wdiagonal())))

        for d in self.direction:
            first : Piece = None_piece()
            
            second : Piece = None_piece()
            for check_piece in self.direction[d]:
                check_piece : Piece

                if not first:
                    if check_piece:
                        first = check_piece
                    if check_piece.colour == self.Opposite:
                        if d in check_piece.move_direction:
                            check_piece.attacking = True
                            self.attacks[d] = check_piece
                            
                if second == None and first:
                    if check_piece:
                        second = check_piece
                    if first.colour == self.colour and check_piece.colour == self.Opposite:
                        if d in check_piece.move_direction:
                            first.pinned = d

                        



        
            

                


