import tkinter as tk
from tkinter import messagebox
from copy import deepcopy

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colours
HIGHLIGHT = "#002D04"  # Color to show possible move
GREEN = "#228B22"  # Color of board
WHITE = "#FFFFFF"  # Color of board and White pieces
BLACK = "#000000"  # Color of black pieces
KING = "#FFFF00"


class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color  # Colour of the piece
        self.isKing = False
        self.pos_x = 0
        self.pos_y = 0
        self.get_position()

    def draw_piece(self, screen):
        x, y = self.pos_x, self.pos_y
        radius = SQUARE_SIZE // 2 - 10
        screen.create_oval(x - radius, y - radius, x + radius, y + radius, fill=self.color, outline=BLACK)
        if self.isKing:
            screen.create_oval(x - 8, y - 8, x + 8, y + 8, fill=KING, outline=BLACK)

    def get_position(self):
        self.pos_x = self.col * SQUARE_SIZE + SQUARE_SIZE // 2
        self.pos_y = self.row * SQUARE_SIZE + SQUARE_SIZE // 2

    def move_piece(self, row, col):
        self.row = row
        self.col = col
        self.get_position()


class Board:
    def __init__(self):
        self.board = [
            [0, Piece(0, 1, BLACK), 0, Piece(0, 3, BLACK), 0, Piece(0, 5, BLACK), 0, Piece(0, 7, BLACK)],
            [Piece(1, 0, BLACK), 0, Piece(1, 2, BLACK), 0, Piece(1, 4, BLACK), 0, Piece(1, 6, BLACK), 0],
            [0, Piece(2, 1, BLACK), 0, Piece(2, 3, BLACK), 0, Piece(2, 5, BLACK), 0, Piece(2, 7, BLACK)],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [Piece(5, 0, WHITE), 0, Piece(5, 2, WHITE), 0, Piece(5, 4, WHITE), 0, Piece(5, 6, WHITE), 0],
            [0, Piece(6, 1, WHITE), 0, Piece(6, 3, WHITE), 0, Piece(6, 5, WHITE), 0, Piece(6, 7, WHITE)],
            [Piece(7, 0, WHITE), 0, Piece(7, 2, WHITE), 0, Piece(7, 4, WHITE), 0, Piece(7, 6, WHITE), 0]
        ]
        self.black_piece_remaining = 12
        self.white_piece_remaining = 12
        self.jump_point = 0

    def draw_board(self, screen):
        screen.create_rectangle(0, 0, WIDTH, HEIGHT, fill=GREEN)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                x0, y0 = col * SQUARE_SIZE, row * SQUARE_SIZE
                x1, y1 = x0 + SQUARE_SIZE, y0 + SQUARE_SIZE
                screen.create_rectangle(x0, y0, x1, y1, fill=WHITE)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw_piece(screen)

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move_piece(row, col)
        if row == ROWS - 1 or row == 0:
            piece.isKing = True

    def get_legal_moves(self, piece):
        moves = {}
        left_sqr = piece.col - 1
        right_sqr = piece.col + 1
        row = piece.row

        if piece.color == WHITE or piece.isKing:
            moves.update(self.look_left(row - 1, max(row - 3, -1), -1, piece.color, left_sqr))
            moves.update(self.look_right(row - 1, max(row - 3, -1), -1, piece.color, right_sqr))

        if piece.color == BLACK or piece.isKing:
            moves.update(self.look_left(row + 1, min(row + 3, ROWS), 1, piece.color, left_sqr,))
            moves.update(self.look_right(row + 1, min(row + 3, ROWS), 1, piece.color, right_sqr))

        return moves

    def look_left(self, current_row, last_row, direction, color, left_sqr, jumped=[]):
        moves = {}
        last_sqr = []
        for step in range(current_row, last_row, direction):
            if left_sqr < 0:
                #col out of bound
                break
            square = self.board[step][left_sqr]
            # If there's no piece in the square
            if square == 0:
                if jumped and not last_sqr:
                    break
                elif jumped:
                    moves[(step, left_sqr)] = last_sqr + jumped
                else:
                    moves[(step, left_sqr)] = last_sqr

                if last_sqr:
                    if direction == -1:
                        row = max(step - 3, 0)
                    else:
                        row = min(step + 3, ROWS)
                    moves.update(self.look_left(step + direction, row, direction, color, left_sqr - 1, jumped=last_sqr))
                    moves.update(self.look_right(step + direction, row, direction, color, left_sqr + 1, jumped=last_sqr))
                break
            # If square piece in square is of same team's colour
            elif square.color == color:
                break
            else:
                last_sqr = [square]

            left_sqr -= 1
        return moves


    def look_right(self, current_row, last_row, direction, color, right_sqr, jumped=[]):
        moves = {}
        last_sqr = []
        for step in range(current_row, last_row, direction):
            if right_sqr >= COLS:
                #col of out bound
                break
            square = self.board[step][right_sqr]
            # If there's no piece in the square
            if square == 0:
                if jumped and not last_sqr:
                    break
                elif jumped:
                    moves[(step, right_sqr)] = last_sqr + jumped
                else:
                    moves[(step, right_sqr)] = last_sqr

                if last_sqr:
                    if direction == -1:
                        row = max(step - 3, 0)
                    else:
                        row = min(step + 3, ROWS - 1)
                    moves.update(self.look_left(step + direction, row, direction, color, right_sqr - 1, jumped=last_sqr))
                    moves.update(self.look_right(step + direction, row, direction, color, right_sqr + 1, jumped=last_sqr))
                break
            # If current piece in square is of same team's colour
            elif square.color == color:
                break
            else:
                last_sqr = [square]

            right_sqr += 1
        return moves

    def remove(self, pieces):
        for piece in pieces:
            if piece.color == BLACK:
                self.jump_point += 1
            self.board[piece.row][piece.col] = 0

    def get_piece(self, row, col):
        return self.board[row][col]


    def calc_score(self, game):
        # self.no_move_left(game)
        return (-self.white_piece_remaining - self.jump_point)

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces


class Game:

    def __init__(self, screen):
        self.screen = screen
        self.board = Board()
        self.selected_piece = None
        self.player = WHITE
        self.legal_moves = {}
        self.highlights = []

    def select_square(self, row, col):
        if self.selected_piece:
            result = self.move_to(row, col)
            if not result:
                self.selected_piece = None
                self.select_square(row, col)

        piece = self.board.board[row][col]
        if piece != 0 and piece.color == self.player:
            self.selected_piece = piece
            self.legal_moves = self.board.get_legal_moves(piece)
            return True

        return False

    def move_to(self, row, col):
        piece = self.board.board[row][col]
        if self.selected_piece and piece == 0 and (row, col) in self.legal_moves:
            self.board.move(self.selected_piece, row, col)
            jumped = self.legal_moves[(row, col)]
            if jumped:
                self.board.remove(jumped)
                if self.player == WHITE:
                    self.board.white_piece_remaining -= 1
                else:
                    self.board.black_piece_remaining -= 1

            self.change_player()
        else:
            return False
        return True

    def highlight_possible_moves(self, moves):
        #self.unhighlight_previous_moves()
        for m in moves:
            r, c = m
            x, y = c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2
            h = self.screen.create_oval(x - 28, y - 28, x + 28, y + 28, outline=HIGHLIGHT, width=2)
            self.highlights.append(h)

    def unhighlight_previous_moves(self):
        for m in self.highlights:
            self.screen.delete(m)
        self.highlights = []

    def change_player(self):
        #self.unhighlight_previous_moves()
        if self.player == WHITE:
            self.player = BLACK
        else:
            self.player = WHITE

    def wins(self):
        winner = None
        if self.board.black_piece_remaining <= 0:
            winner = "BLACK"
        elif self.board.white_piece_remaining <= 0:
            winner = "WHITE"
        else:
            current_player_color = self.player
            opponent_color = "BLACK" if current_player_color == WHITE else "WHITE"
            valid_moves_exist = False
            for row in range(ROWS):
                for col in range(COLS):
                    piece = self.board.get_piece(row, col)
                    if piece != 0 and piece.color == current_player_color:
                        if self.board.get_legal_moves(piece):
                            valid_moves_exist = True
                            break
            if not valid_moves_exist:
                winner = opponent_color

        return winner

    def update(self):
        # if self.board.black_piece_remaining == 0 or self.board.white_piece_remaining == 0:
        self.board.draw_board(self.screen)
        self.highlight_possible_moves(self.legal_moves)

    def algo_move(self, board):
        self.board = board
        self.change_player()


def minimax(board_pos, depth, alpha, beta, max_player, game):
    if depth == 0 or game.wins() is not None:
        return board_pos.calc_score(game), board_pos

    if max_player:
        max_score = float('-inf')
        next_move = None
        for move in possible_moves(board_pos, BLACK):
            score, _ = minimax(move, depth - 1, alpha, beta, False, game)
            max_score = max(max_score, score)
            if max_score >= beta:
                return max_score, next_move  # Beta cutoff
            alpha = max(alpha, max_score)
            if max_score == score:
                next_move = move

        return max_score, next_move
    else:
        min_score = float('inf')
        next_move = None
        for move in possible_moves(board_pos, WHITE):
            score, _ = minimax(move, depth - 1, alpha, beta, True, game)
            min_score = min(min_score, score)
            if min_score <= alpha:
                return min_score, next_move  # Alpha cutoff
            beta = min(beta, min_score)
            if min_score == score:
                next_move = move

        return min_score, next_move


def possible_moves(board, color):
    moves = []
    for piece in board.get_all_pieces(color):
        legal_moves = board.get_legal_moves(piece)
        for move, jumped in legal_moves.items():
            # Getting a copy of the board to
            # check possibles moves to avoid messing up the actual board
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            temp_board.move(temp_piece, move[0], move[1])
            if jumped:
                temp_board.remove(jumped)
            moves.append(temp_board)

    return moves


def main(depth):
    root = tk.Tk()
    root.title("Checkers")

    SCREEN = tk.Canvas(root, width=WIDTH, height=HEIGHT)
    SCREEN.pack()
    game = Game(SCREEN)

    while True:
        if game.wins() is not None:
            winner = game.wins()
            messagebox.showinfo("Game Over", f"WINNER IS {winner}")
            root.quit()
            return

        if game.player == BLACK:
            alpha = float('-inf')
            beta = float('inf')
            value, new_board = minimax(game.board, depth, alpha, beta, WHITE, game)
            game.algo_move(new_board)
            #game.update()

        def mouse_click(event):
            row = event.y // SQUARE_SIZE
            col = event.x // SQUARE_SIZE
            click = game.select_square(row, col)
            game.update()

        SCREEN.bind("<Button-1>", mouse_click)
        game.update()

        root.update()
    root.mainloop()


def show_instructions():
    instructions = """        
    Checkers Rules:

    1. Each player starts with 12 pieces.
       Your piece is WHITE and your turn is first.
    2. To move a piece, click on it and 
       then click on the highlighted square where you want to move it. 
    3. Wait for the AI to make a move and then follow up with your move.
    4. You and AI will take turns moving the pieces diagonally forward.
       If a player's piece reaches the opposite end of the board, 
       it becomes a king and gains the ability to move backwards.
    5. If a player's piece is adjacent to an opponent's piece 
       and there is an empty square behind the opponent's piece,
       the player can jump over the opponent's piece and capture it.
    6. The game ends when either one player captures all of the opponent's pieces 
       or blocks them from making any legal moves.
    7. Any player with remaining pieces 
       or the ability to make legal moves wins the game.

                          Enjoy the game!
    """
    messagebox.showinfo("Instructions", instructions)

def start_game():
    depth = depth_var.get()
    if depth > 4:
        result = messagebox.askquestion("START GAME", f"AI smartness is set high as {depth}. Proceed?")
        if result == "no":
            return

    show_instructions()
    start_frame.destroy()
    game_frame.pack()
    main(depth)



if __name__ == '__main__':
    root = tk.Tk()
    root.title("Checkers")

    start = tk.Canvas(root, width=WIDTH, height=HEIGHT)
    start.pack()

    start_frame = tk.Frame(start)
    start_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    game_info = """ 
    WELCOME TO CHECKERS!!!
    
    Click on "-" or "+" to adjust the AI player's smartness.
    
    Remember! Higher smartness can make the AI responses a little slower.
    
    Click the "Start Game" button when you're ready to begin!
    """

    def decrement_depth():
        current_value = depth_var.get()
        if current_value > 2:
            depth_var.set(current_value - 1)

    def increment_depth():
        current_value = depth_var.get()
        if current_value < 6:
            depth_var.set(current_value + 1)

    info_label = tk.Label(start_frame, text="CHECKERS", font=("Curlz MT", 36, "bold"), fg="red")
    info_label.grid(row=0, column=0, columnspan=4, padx=10, pady=(10, 20))

    game_info_label = tk.Label(start_frame, text=game_info, font=("Chalkboard", 12), fg="black", bg="yellow")
    game_info_label.grid(row=1, column=0, columnspan=4, padx=10, pady=(0, 20))

    depth_label = tk.Label(start_frame, text="AI Smartness?", font=("Comic Sans MS", 14), fg="dark green")
    depth_label.grid(row=2, column=0, padx=(20, 5), pady=5)

    depth_var = tk.IntVar(value=2)

    minus_button = tk.Button(start_frame, text="-", command=decrement_depth, font=("Comic Sans MS", 12), width=2, bg="yellow", fg="black")
    minus_button.grid(row=2, column=1, pady=5)

    depth_display = tk.Label(start_frame, textvariable=depth_var, font=("Comic Sans MS", 14), fg="black")
    depth_display.grid(row=2, column=2, pady=5)

    plus_button = tk.Button(start_frame, text="+", command=increment_depth, font=("Comic Sans MS", 12), width=2, bg="yellow", fg="black")
    plus_button.grid(row=2, column=3, pady=5)

    start_button = tk.Button(start_frame, text="Start Game", command=start_game, font=("Comic Sans MS", 18), fg="white",
                             bg="red")
    start_button.grid(row=3, column=0, columnspan=4, pady=(20, 10))

    game_frame = tk.Frame(start)

    root.mainloop()
