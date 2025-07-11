import pygame as p
import ChessEngine

Width = Height = 512
Dimension = 8
Sq_Size = Height // Dimension
Max_FPS = 15
images = {}

def load_Images():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR", "bP", "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR", "wP"]
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (Sq_Size, Sq_Size))

def main():
    p.init()
    screen = p.display.set_mode((Width, Height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False
    animate = False
    load_Images()
    running = True
    sq_selected = ()
    player_clicks = []
    game_over = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over:
                    location = p.mouse.get_pos()
                    col = location[0] // Sq_Size
                    row = location[1] // Sq_Size
                    if sq_selected == (row, col):
                        sq_selected = ()
                        player_clicks = []
                    else:
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected)
                    if len(player_clicks) == 2:
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                gs.make_move(valid_moves[i], t = True)
                                move_made = True
                                animate = True
                                sq_selected = ()
                                player_clicks = []
                        if not move_made:
                            player_clicks = [sq_selected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo_move(t = True)
                    move_made = True
                    animate = False
                if e.key == p.K_q:
                    gs.promotion_type = "Q"
                elif e.key == p.K_k:
                    gs.promotion_type = "N"
                elif e.key == p.K_b:
                    gs.promotion_type = "B"
                elif e.key == p.K_r:
                    gs.promotion_type = "R"
                if e.key == p.K_p:
                    gs = ChessEngine.GameState()
                    valid_moves = gs.get_valid_moves()
                    sq_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
        if move_made:
            if animate:
                animate_move(gs.move_log[-1], screen, gs.board, clock)
            valid_moves = gs.get_valid_moves()
            move_made = False
        draw_game_state(screen, gs, valid_moves, sq_selected)
        if gs.checkmate:
            game_over = True
            if gs.white_to_move:
                draw_text(screen, "Black wins by checkmate")
            else:
                draw_text(screen, "White wins by checkmate")
        elif gs.stalemate:
            draw_text(screen, "Stalemate")
        clock.tick(Max_FPS)
        p.display.flip()

def highlight_squares(screen, gs, valid_moves, sq_selected):
    if sq_selected != ():
        r,c  = sq_selected
        if gs.board[r][c][0] == ("w" if gs.white_to_move else "b"):
            s = p.Surface((Sq_Size, Sq_Size))
            s.set_alpha(100)
            s.fill(p.Color("purple"))
            screen.blit(s, (c * Sq_Size, r * Sq_Size))
            s.fill(p.Color("blue"))
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    screen.blit(s, (move.end_col * Sq_Size, move.end_row * Sq_Size))


def draw_game_state(screen, gs, valid_moves, sq_selected):
    draw_board(screen)
    highlight_squares(screen, gs, valid_moves, sq_selected)
    draw_pieces(screen, gs.board)

def draw_board(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(Dimension):
        for c in range(Dimension):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color,p.Rect(c*Sq_Size, r*Sq_Size, Sq_Size, Sq_Size))


def draw_pieces(screen, board):
    for r in range(Dimension):
        for c in range(Dimension):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], p.Rect(c * Sq_Size, r * Sq_Size, Sq_Size, Sq_Size))

def animate_move(move, screen, board, clock):
    global colors
    dr = move.end_row - move.start_row
    dc = move.end_col - move.start_col
    frames_per_square = 10
    frame_count = (abs(dr) + abs(dc)) * frames_per_square
    for frame in range(frame_count + 1):
        r, c = (move.start_row + dr * frame/frame_count, move.start_col + dc * frame/frame_count)
        draw_board(screen)
        draw_pieces(screen, board)
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect(move.end_col * Sq_Size, move.end_row * Sq_Size, Sq_Size, Sq_Size)
        p.draw.rect(screen, color, end_square)
        if move.piece_captured != "--":
            screen.blit(images[move.piece_captured], end_square)
        screen.blit(images[move.piece_moved], p.Rect(c * Sq_Size, r * Sq_Size, Sq_Size, Sq_Size))
        p.display.flip()
        clock.tick(60)

def draw_text(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    text_object = font.render(text, 0, p.Color("Dark Gray"))
    text_location = p.Rect(0,0, Width, Height).move(Width/2 - text_object.get_width()/2, Height/2 - text_object.get_height()/2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, 0, p.Color("Black"))
    screen.blit(text_object, text_location.move(2, 2))
if __name__ == "__main__":
    main()