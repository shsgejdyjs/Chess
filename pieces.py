from __future__ import annotations
from collections import deque
from typing import TYPE_CHECKING
import pygame

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
    def replace(self, other):
        return Coordinate((self.coord[0] if other[0] == 0 else other[0], self.coord[1] if other[1] == 0 else other[1]))
    def __hash__(self):
        return hash(self.coord)
    def __eq__(self, other):
        if isinstance(other, tuple):
            return self.coord == other
        if isinstance(other, Coordinate):
            return self.coord == other.coord
        return NotImplemented
        
    def __lt__(self, other):
        return self.coord[0]**2 + self.coord[1]**2 < other[0]**2 + other[1]**2
    def __le__(self,other):
        return self < other or self == other
    def __mul__(self, other):
        if isinstance(other, tuple):
            return Coordinate((self.coord[0]*other[0], self.coord[1]*other[1]))
        elif isinstance(other, (int, float)):
            return Coordinate((self.coord[0]*other, self.coord[1]*other))
    
    def convert(self, start = (0,0), board_length=1) -> tuple:
        return (self * (board_length/8, -board_length/8) + (board_length/16, 15*board_length/16) + start).coord

    def out_of_bounds(self):
        if not -1<self[0]<8 or not -1<self[1]<8:
            return True
        return False
    def normalise(self):
        return (int(abs(self[0])/self[0]) if self[0] else 0, int(abs(self[1])/self[1]) if self[1] else 0)
    
class Piece(pygame.sprite.Sprite):
    name = "a"
    king : King = None
    attacking = False
    pinned = []
    move_direction = []
    valid = []
    moved = False
    
    click = False

    def __init__(self, Colour, Coordinates, board=None):
        pygame.sprite.Sprite.__init__(self)
        self.moved = False
        self.colour = Colour
        self.coord = Coordinate(Coordinates)
        self.board : Board = board
        if Colour == "White":
            self.Opposite = "Black"
        else:
            self.Opposite = "White"
        
        length = 400 if not self.board else self.board.length
        self.image = pygame.image.load(os.path.join(GAME_FOLDER, 'assets', Colour.lower()[0] + self.name + '.svg'))
        self.rect = self.image.get_rect()
        self.rect.center = self.coord.convert((0,0), length)
        
                
    
    
    def find_piece(self, coord):
        return self.board.find_piece(coord)
    
    def check_click(self, point):
        if self.rect.collidepoint(point):
            self.click = True
            
    def update(self):
        if self.click:
            self.rect.center = pygame.mouse.get_pos()
            
    

    
    def __repr__(self):
        colourCode = {"White":"W", "Black":"B", "None":" "}
        return colourCode[self.colour] + self.name
    def vertical(self, coord = None):
        """down up"""
        if coord == None:
            coord = self.coord
        up = deque()
        down = deque()
        for i in range(8):
            if i == coord[1]:
                continue
            
            piece = self.find_piece((coord[0],i))

            
            if i - coord[1] > 0:
                up.append(piece)
            else:
                down.appendleft(piece)


    
        return down, up      
    def horizontal(self, coord = None):

        """left right"""
        if coord == None:
            coord = self.coord
        left = deque()
        right = deque()

        for i in range(8):
            if i == coord[0]:
                continue
            
            piece = self.find_piece((i,coord[1]))

            
            if i - coord[0] > 0:
                right.append(piece)
            else:
                left.appendleft(piece)

        return left, right
    def bdiagonal(self, coord = None):
         
        """ne sw"""

        if coord == None:
            coord = self.coord
        ne = deque()
        sw = deque()

        diff = coord[0] - coord[1]
        
        xstart = diff if diff > 0 else 0
        ystart = -diff if diff < 0 else 0
        

        for i in range(8-abs(diff)):
            if xstart + i == coord[0]:
                continue
            piece = self.find_piece((xstart + i, ystart + i))
            
            if xstart + i > coord[0]:
                ne.append(piece)
            else:
                sw.appendleft(piece)

       
        return ne, sw        
    def wdiagonal(self, coord = None):

        """nw se"""
        if coord == None:
            coord = self.coord
        nw = deque()
        se = deque()
        total = coord[0] + coord[1]

        xstart = 0 if total -7 < 0 else total - 7
        ystart = 7 if total -7 > 0 else total

        for i in range(8 - abs(total - 7)):
            if xstart + i == coord[0]:
                continue
            piece = self.find_piece((xstart + i, ystart - i))
            
            if xstart + i > coord[0]:
                se.append(piece)
            else:
                nw.appendleft(piece)

       
        return nw, se
    
    def set_king(self, k):
        self.king = k   
    def set_board(self, b):
        self.board = b
    def valid_moves(self):
        valid = []
        moves = self.movement()
        self.king.check_in_check()
        old_distance = self.coord - self.king.coord

        if len(self.king.attacks) == 3 or len(self.king.attacks) == 2 and self.king.attacks["knight"]:
            self.valid = valid
            return valid

        for move in moves:
            #vector from king to the new coord
            new_distance = move - self.king.coord

            if knight:=self.king.attacks["knight"]:
                if move == knight.coord:
                    valid.append(move)
            elif len(self.king.attacks) == 2:
                if not(new_distance[0] * new_distance[1] !=0 and abs(new_distance[0]) != abs(new_distance[1])) and (d:=new_distance.normalise()) in self.king.attacks:
                    if new_distance <= (self.king.attacks[d].coord -self.king.coord):
                        valid.append(move)
                
            elif self.pinned:
                
                if not(new_distance[0] * new_distance[1] !=0 and abs(new_distance[0]) != abs(new_distance[1])) and new_distance.normalise() == old_distance.normalise():
                    valid.append(move)
            
            else:
                valid.append(move)
        self.valid = valid
        
        return valid
    
    

    
    def movement(self, *possible_directions) -> list:
        moves = []
        
        directions = dict(zip(self.move_direction, (possible_directions))) 
        
        for d in directions:
            
            skip = False
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


class Queen(Piece):
    name = "Q"
    move_direction = [(1,1),(-1,-1),(-1,1),(1,-1),(-1,0),(1,0),(0,-1),(0,1)]
    
    def movement(self):
        return super().movement(*self.bdiagonal(), *self.wdiagonal(), *self.horizontal(), *self.vertical() )

class Pawn(Piece):
    
    moved_twice = False
    name = "P"
    
        
    def movement(self):
        moves = []
        direction = 1 if self.colour == "White" else -1
        for i in range(-1,2):
            newCoord = self.coord + (i,direction)
            if not newCoord.out_of_bounds():
                if i != 0 and self.find_piece(newCoord).colour == self.Opposite:
                    moves.append(newCoord)
                elif i == 0 and not self.find_piece(newCoord):
                    moves.append(newCoord)
                    if not self.moved and not self.find_piece(newCoord := newCoord + (0,direction)):
                        moves.append(newCoord)
                        
        
        for i in range(-1,2,2):
            newCoord = self.coord + (i,0)
            
            if -1 < newCoord[0] < 8:
                piece = self.find_piece(newCoord)
                if (piece := self.find_piece(newCoord)).name == "P" and piece.colour == self.Opposite and piece.moved_twice:
                    moves.append(newCoord + (0,direction))
        return moves

    def promote(self, surface, board_length, new_coord):
        p = promote_window(new_coord, board_length, self.colour)
        sprites = pygame.sprite.Group(p)
        running = True
        s = surface.copy()
        darken = pygame.surface.Surface((400,400),pygame.SRCALPHA)
        darken.fill((0,0,0,128))
        
        while running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not p.rect.collidepoint(pygame.mouse.get_pos()):
                        running = False
                        return None_piece((0,0), self.board)
                    else:
                        for piece in p.promote_pieces:
                            if p.promote_pieces[piece][1].collidepoint(pygame.mouse.get_pos()):
                                return p.promote_pieces[piece][2](self.colour, self.coord, self.board)
                                

            
                    
            surface.fill("black")
            surface.blit(s, (0,0))
            
            surface.blit(darken, (0,0))
            
            
            sprites.update()
            sprites.draw(surface)
            
            pygame.display.flip()
        
            
                    


class promote_window(pygame.sprite.Sprite):
    def __init__(self, coord:Coordinate, length, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,200), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        self.start = Coordinate((0,0)) if colour == "White" else Coordinate((0,-150))
        self.rect.topleft = (self.start + coord.convert((-25,-25), length)).coord
        
        
        self.promote_pieces = {"Queen":[None, None, Queen], "Rook":[None, None, Rook], "Night":[None, None, Knight], "Bishop":[None, None, Bishop]}
        
        self.colour = colour
        self.length = length


        
        current = Coordinate(self.rect.topleft) + self.start *-1
        self.direction = 1 if colour == "White" else -1
        for piece in self.promote_pieces:
            self.promote_pieces[piece][1] = pygame.rect.Rect(0,0,50,50)
            self.promote_pieces[piece][1].topleft = current.coord
            current = current + (0,50*self.direction)
            
    def update(self):
        self.image = pygame.Surface((50,200), pygame.SRCALPHA)
        
        circle_center = Coordinate((25,25)) + self.start * -1
        
        for piece in self.promote_pieces:
            
            r = pygame.Rect(*((circle_center-(25,25)).coord), 50, 50)
            if self.promote_pieces[piece][1].collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.image, (0,128,128,128), r)
                scale = 1.2
                
            else:
                scale = 1
                self.image.blit(pygame.image.load(os.path.join(GAME_FOLDER, 'assets', 'circle.svg')),(circle_center-(25,25)).coord)
                
            self.image.blit(load_and_scale_svg(os.path.join(GAME_FOLDER, 'assets', f'{self.colour[0].lower()}{piece[0]}.svg'), scale), (circle_center - (22*scale,22*scale)).coord)
            circle_center = circle_center + (0,50*self.direction)
            

class Rook(Piece):
    name = "R"
    
    move_direction = [(-1,0),(1,0),(0,-1),(0,1)]
      
    def movement(self):
        return super().movement(*self.horizontal(), *self.vertical())

               
    
class Bishop(Piece):
    name = "B"
    move_direction = [(1,1),(-1,-1),(-1,1),(1,-1)]
    
    def movement(self):
        return super().movement(*self.bdiagonal(), *self.wdiagonal())
class Knight(Piece):
    name = "N"
    
    def movement(self):
        moves = [self.coord + (i,j) for i in range(-2,3) for j in range(-2,3) if abs(i*j) == 2]
        return moves

    def valid_moves(self):
        self.king.check_in_check()
        valid = []
        if len(self.king.attacks) == 3 or len(self.king.attacks) == 2 and self.king.attacks["knight"]:
            self.valid = []
            return []
        
        moves = self.movement()
        for move in moves:
            if knight := self.king.attacks["knight"]:
                if move == knight.coord:
                    valid.append(move)
            elif len(self.king.attacks) == 2:   
                
                new_distance = move - self.king.coord
                if not(new_distance[0] * new_distance[1] !=0 and abs(new_distance[0]) != abs(new_distance[1])) and (d := new_distance.normalise()) in self.king.attacks:
                    attack_distance = self.king.attacks[d].coord - self.king.coord
                    if new_distance <= attack_distance:
                        valid.append(move)

            elif not self.pinned:
                if not move.out_of_bounds():
                    if self.find_piece(move).colour != self.colour:
                        valid.append(move)
        self.valid = valid
        return valid

class King(Piece):
    name = "K"

    attacks = {"knight":None}
    

    
    
    def check_in_check(self):
        #this needs to check what directions the king is being checked from if any
        
        self.direction = dict(zip([(0,-1), (0,1), (-1,0), (1,0), (1,1), (-1,-1), (-1,1), (1,-1)], (*self.vertical(), *self.horizontal(), *self.bdiagonal(), *self.wdiagonal())))
        self.attacks = {"knight":None}
        for d in self.direction:
            first = None
            second = None
            for check_piece in self.direction[d]:
                check_piece : Piece
                
                if not first:
                    if check_piece:
                        first = check_piece
                    if check_piece.colour == self.Opposite:
                        if d in check_piece.move_direction:
                            check_piece.attacking = True
                            self.attacks[d] = check_piece
                            
                            
                elif second == None:
                    if check_piece:
                        second = check_piece
                    if first.colour == self.colour and check_piece.colour == self.Opposite:
                        if d in check_piece.move_direction:
                            first.pinned = d
        for i in range(-1,2,2):
            direction = 1 if self.colour == "White" else -1

            new_coord = self.coord + (i,direction)
            if not new_coord.out_of_bounds() and (piece:=self.find_piece(new_coord)).name == "P" and piece.colour == self.Opposite:
                self.attacks[(i,direction)] = piece
                piece.attacking = True
        for knight in self.board.knights[self.Opposite]:
            if self.coord in knight.movement():
                self.attacks["knight"] = knight
                knight.attacking = True
                


    def predict_check(self, coord):
        directions = dict(zip([(0,-1), (0,1), (-1,0), (1,0), (1,1), (-1,-1), (-1,1), (1,-1)], (*self.vertical(coord), *self.horizontal(coord), *self.bdiagonal(coord), *self.wdiagonal(coord))))
        for d in directions:
            
            count = 0
            for checkpiece in directions[d]:
                if checkpiece and checkpiece != self:
                    count +=1
                if checkpiece.colour == self.Opposite and d in checkpiece.move_direction:
                    if count == 1:
                        return True
        
        for i in range(-1,2,2):
            direction = 1 if self.colour == "White" else -1
            new_coord = coord + (i,direction)
            if not new_coord.out_of_bounds() and (piece:=self.find_piece(new_coord)).name == "P" and piece.colour == self.Opposite:
                return True
        
        for knight in self.board.knights[self.Opposite]:
            if coord in knight.movement():
                return True
        
        opposite_king = self.board.kings[self.Opposite]
        if coord in opposite_king.movement():
            return True


        return False
    
    def movement(self):
        moves = [self.coord + (i,j) for i in range(-1,2) for j in range(-1,2) if (i,j) != (0,0)]
        return moves
    
    def valid_moves(self):
        valid = []
        moves = self.movement()
        for move in moves:
            if not move.out_of_bounds() and not self.predict_check(move) and self.find_piece(move).colour != self.colour:
                valid.append(move)
        if self.moved == False:
            for i in range(-1,2,2):
                r = 7 if i == 1 else 0
                piece = self.find_piece((r, self.coord[1]))
                if piece.name == "R" and piece.moved == False and not (self.attacks["knight"] or len(self.attacks) > 1) and not any(map(self.find_piece, [self.coord + (k*i,0) for k in range(1, int(3+(1-i)/2))])):
                    new_coord = self.coord + (i*2,0)
                    if not self.predict_check(new_coord) and not self.predict_check(new_coord + (-i,0)):
                        valid.append(new_coord)
                        valid.append(Coordinate((r, self.coord[1])))

                       
                
        
        self.valid = valid
        return valid


