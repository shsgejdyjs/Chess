from __future__ import annotations
from collections import deque
from typing import TYPE_CHECKING
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
        return Coordinate(self.coord[0] if i[0] == 0 else i[0], self.coord[1] if i[1] == 0 else i[1])
    def __hash__(self):
        return hash(self.coord)
    def __eq__(self, other):
        if isinstance(other, tuple):
            return self.coord == other
        return NotImplemented
        

def normalise(vector):
    return (abs(vector[0])/vector[0] if vector[0] else 0, abs(vector[1])/vector[1] if vector[1] else 0)

class directions():
    def __init__(self, *pieces : deque):
        self.pieces = dict(zip([(0,-1), (0,1), (-1,0), (1,0), (1,1), (-1,-1), (-1,1), (1,-1)], pieces))
        self.attacks = {}
    def __repr__(self):
        return str(self.pieces)
    def get_directions(self, ds) -> list: 
        return self.pieces[ds]

    def __iter__(self):
        return self.pieces.__iter__()
    
    def __next__(self):
        return self.pieces.__next__()
    
    def __getitem__(self, i) -> list:
        return self.pieces[i]
    
class Piece():
    name = "a"
    king : King = None
    attacking = False
    pinned = []
    move_direction = []
    def __init__(self, Colour, Coordinates, board):
        self.colour = Colour
        self.coord = Coordinate(Coordinates)
        self.board : Board = board
        if Colour == "White":
            self.Opposite = "Black"
        else:
            self.Opposite = "White"
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
        

        for i in range(8-diff):
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
                
            if self.pinned:
                if not(new_distance[0] * new_distance[1] !=0 and abs(new_distance[0]) != abs(new_distance[1])) and normalise(new_distance) == normalise(old_distance):
                    valid.append(move)
            
            else:
                valid.append(move)
        
        return valid

    
    def movement(self) -> list:
        pass       
#The none_piece is a dummy piece that represents an empty square.
#This is used to prevent checking if a square comtains a piece every time
class None_piece(Piece):
    name = "X"

    def __init__(self, Coordinates = {9,9}, Board=None):
        super().__init__("None", Coordinates, Board)

    def __bool__(self):
        return False
    
      
class Pawn(Piece):
    moved = False
    movedTwice = False
    name = "P"
    def Movement(self):
        moves = []
        if self.moved == False:
            newCoord = (self.coord[0], self.coord[1] + 2)
            if not self.findPiece(newCoord):
                moves.append(newCoord)
        for i in range(-1,2):
            newCoord = (self.coord[0] + i, self.coord[1] + 1)
            if -1 < newCoord[0] < 8:
                if i != 0 and self.findPiece(newCoord).colour == self.Opposite:
                    moves.append(newCoord)
                elif i == 0 and not self.findPiece(newCoord):
                    moves.append(newCoord)
        
        for i in range(-1,2,2):
            newCoord = (self.coord[0] + i, self.coord[1])
            if -1 < newCoord[0] < 8:
                if piece := self.findPiece(newCoord).name == "P" and piece.colour == self.opposite and piece.movedTwice:
                    moves.append((newCoord[0], newCoord[1] + 1))
        return moves
                
class Rook(Piece):
    name = "R"
    moved = False
    move_direction = [(1,0),(0,1),(-1,0),(0,-1)]
    
class Bishop(Piece):
    name = "B"
    move_direction = [(1,1),(-1,-1),(1,-1),(-1,1)]
    
class Knight(Piece):
    name = "N"

class Queen(Piece):
    name = "Q"
    move_direction = [(1,1),(-1,-1),(1,-1),(-1,1),(1,0),(0,1),(-1,0),(0,-1)]
class King(Piece):
    name = "K"

    inCheck = False 
    direction: directions = None
    attacks = {}

    def set_direction(self):
        self.direction = directions(*self.vertical(), *self.horizontal(), *self.bdiagonal(), *self.wdiagonal())

    def check_in_check(self):
        #this needs to check what directions the king is being checked from if any
        for d in self.direction:
            first : Piece = None_piece()
            second : Piece = None_piece()
            for check_piece in self.directions[d]:
                check_piece : Piece

                if first == None:
                    if check_piece:
                        first == check_piece
                    if check_piece.colour == self.Opposite:
                        if d in check_piece.move_direction:
                            check_piece.attacking = True
                            
                if second == None and first:
                    if check_piece:
                        second = check_piece
                    if first.colour == self.colour and check_piece.colour == self.Opposite:
                        if d in check_piece.move_direction:
                            first.pinned = d

                        



        
            

                


