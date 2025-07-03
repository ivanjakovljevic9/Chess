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
    gs = ChessEngine.game_state()
    load_Images()
    running = True
    sq_selected = ()
    player_clicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
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
                    move = ChessEngine.move(player_clicks[0], player_clicks[1], gs.board)
                    gs.make_move(move)
                    sq_selected = ()
        draw_game_state(screen, gs)
        clock.tick(Max_FPS)
        p.display.flip()
def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)

def draw_board(screen):
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



if __name__ == "__main__":
    main()