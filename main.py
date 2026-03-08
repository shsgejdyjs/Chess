import pygame
import pygame.freetype
import board
import pieces

pygame.init()
screen = pygame.display.set_mode((400,400))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()
font = pygame.freetype.SysFont(None, 24)
running = True


# PIECES = {(i,j):pieces.None_piece((i,j), None) for i in range(8) for j in range(8)}
# PIECES[0,0] = pieces.Queen("White", (0,0))
# PIECES[1,0] = pieces.King("White", (1,0))
# PIECES[7,7] = pieces.King("Black", (7,7))

b = board.Board()



clicked_piece = None

current = "White"
swap = {"White":"Black", "Black":"White"}

while running:

    

    for event in pygame.event.get():



        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:

            #unhighlight a piece if clicking it again
            if clicked_piece:
                for square in b.squares:
                    if square.rect.collidepoint(pygame.mouse.get_pos()) and square.coord in clicked_piece.valid:
                        break
                else:
                    clicked_piece = None
                    b.unhighlight_squares()

            #clicking a piece
            if clicked_piece and not clicked_piece.rect.collidepoint(pygame.mouse.get_pos()) or not clicked_piece:
                for piece in b.piece_sprites:
                    if piece.colour == current and piece.rect.collidepoint(pygame.mouse.get_pos()) and ((piece != clicked_piece and (clicked_piece and piece.coord not in clicked_piece.valid_moves())) or clicked_piece == None):
                        old_pos = piece.rect.center
                        piece.click = True
                        clicked_piece = piece
                        b.unhighlight_squares()
                        b.highlight_squares(piece.valid_moves(), piece.coord)
        
        if event.type == pygame.MOUSEBUTTONUP:
            if clicked_piece:
                for piece in b.Pieces.values():
                    piece.pinned = False
                b.kings[current].check_in_check()
                for square in b.squares:
                    if square.rect.collidepoint(pygame.mouse.get_pos()):
                        promoted = True

                        if clicked_piece.name == "P" and square.coord[1] in [0,7] and square.coord in clicked_piece.valid:
                            clicked_piece.rect.center = square.coord.convert()
                            b.piece_sprites.draw(screen)
                            pygame.display.flip()
                            promoted = clicked_piece.promote(screen, b.length, square.coord)
                            if promoted:
                                b.piece_sprites.remove(clicked_piece)
                                b.Pieces[clicked_piece.coord] = promoted
                                clicked_piece = promoted
                                
                            
                        if square.coord in clicked_piece.valid and not isinstance(promoted, pieces.None_piece) or (promoted and isinstance(promoted, pieces.Piece)):
                            b.move_piece(clicked_piece, square.coord)       
                            b.unhighlight_squares()
                            clicked_piece.click = False
                            clicked_piece = None  
                            current = swap[current]   
                        else:
                            clicked_piece.rect.center = old_pos
                            clicked_piece.click = False
                            

    if clicked_piece:
        for square in b.squares:
            if square.rect.collidepoint(pygame.mouse.get_pos()) and square.coord in (*clicked_piece.valid, clicked_piece.coord):
                square.hover = (0,0,128,128)
            elif square.coord != clicked_piece.coord:
                square.hover = False         
    
    
            
    screen.fill("black")
    
    
    b.piece_sprites.update()
    b.squares.update(screen)
    b.piece_sprites.draw(screen)
    
    if len((king := b.kings[current]).attacks) > 1 and len(king.valid) == 0:
        checkmate = True
        for piece in b.piece_sprites:
            if piece.colour == current and len(piece.valid_moves()) > 0:
                checkmate = False
        if checkmate:
            font.render_to(screen, (200,200), "CHECKMATE", (128,0,0), size=100)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()