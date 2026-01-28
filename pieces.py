from collections import deque
   
class Piece():
    name = "a"
    king = None
    def __init__(self, Colour, Coordinates, Board):
        self.colour = Colour
        self.coord = Coordinates
        self.Board = Board
        if Colour == "White":
            self.Opposite = "Black"
        else:
            self.Opposite = "White"


    def findPiece(self, coord):
        return self.Board.find_piece(coord)

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
                up.appendleft(piece)
            else:
                down.append(piece)
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
                right.appendleft(piece)
            else:
                left.append(piece)
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
                ne.appendleft(piece)
            else:
                sw.append(piece)

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
                se.appendleft(piece)
            else:
                nw.append(piece)
        return nw, se


    def directions(self):
        """
        down up left right ne sw nw se
        """
        return *self.vertical(), *self.horizontal(), *self.bdiagonal(), *self.wdiagonal()

    def movement(self):
        pass
    def valid_moves(self):
        valid = []
        moves = self.movement()

        #first need to check if any of the moves block a check
        #then if a piece is pinned

        for move in moves:
            pass

        for d in self.Board.kings[self.colour].direction:
            pass
            


        

#The none_piece is a dummy piece that represents an empty square.
#This is used to prevent checking if a square comtains a piece every time
class None_piece(Piece):
    name = "X"

    def __init__(self, Coordinates, Board):
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
    def Movement(self):
        possible_moves = []
        coord = []
class Bishop(Piece):
    name = "B"
class Knight(Piece):
    name = "N"
class Queen(Piece):
    name = "Q"
class King(Piece):
    name = "K"

    inCheck = False 

    

    def check_in_check(self):
        attacks = []

        
            

                


