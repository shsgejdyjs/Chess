import pygame
import board
import pieces

pygame.init()
screen = pygame.display.set_mode((400,400))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()
running = True
b = board.Board()

clicked_piece = None



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if clicked_piece and clicked_piece.rect.collidepoint(pygame.mouse.get_pos()):
                clicked_piece = None
                b.unhighlight_squares()

            
            elif clicked_piece and not clicked_piece.rect.collidepoint(pygame.mouse.get_pos()) or not clicked_piece:
                for piece in b.piece_sprites:
                    if piece.rect.collidepoint(pygame.mouse.get_pos()) and (piece != clicked_piece or clicked_piece == None):
                        old_pos = piece.rect.center
                        piece.click = True
                        clicked_piece = piece
                        b.highlight_squares(piece.valid_moves(), piece.coord)
        
        
        
        if clicked_piece:
            for square in b.squares:
                if square.rect.collidepoint(pygame.mouse.get_pos()) and square.coord in (*clicked_piece.valid, clicked_piece.coord):
                    square.hover = (0,0,128,128)
                elif square.coord != clicked_piece.coord:
                    square.hover = False
                        

        if event.type == pygame.MOUSEBUTTONUP:
            if clicked_piece:
                moves = clicked_piece.valid
                for square in b.squares:
                    if square.rect.collidepoint(pygame.mouse.get_pos()):
                        
                        if square.coord in moves:
                            b.move_piece(clicked_piece, square.coord)
                            if clicked_piece.name == "P":
                                clicked_piece.moved = True
                            b.unhighlight_squares()
                            clicked_piece.click = False
                            clicked_piece = None
                            
                                
                        else:
                            clicked_piece.rect.center = old_pos
                            clicked_piece.click = False
                    
                    
                
            
    screen.fill("black")
    b.piece_sprites.update()
    b.squares.update(screen)
    b.piece_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()