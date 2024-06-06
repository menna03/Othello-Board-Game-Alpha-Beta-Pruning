import copy
import math
import tkinter as tk
from tkinter import messagebox
import time

class OthelloBoard:
    def __init__(self):
        self.board = [[' '] * 8 for _ in range(8)]
        self.board[3][3] = 'W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'
        self.board[4][4] = 'W'
        self.current_player = 'B'

    def is_valid_move(self, row, col):
        if row < 0 or row >= 8 or col < 0 or col >= 8 or self.board[row][col] != ' ':
            return False
        # Add diagonal directions to the existing row and column directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            # hena bey-check lw el cell within el boundaries , enaha beta3et el opponent 3shan y-indicate en de cell momken ye7salaha flip
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] != self.current_player and self.board[r][c] != ' ':
                while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] != ' ':
                    # hena b2a beyshoof lw el cell elly 3aleha el dor beta3et el current keda hay2dar y3mel flip ll circle beta3et el ai
                    # b ma3na haybtedy mn awel 5ales maslan b black b3den hay5osh el if el ola hayla2eha white, hayfdal mashy fe nafs el row/ col
                    # l8ayet ma yla2y makan momken y-flip elly fel nos mn 5elalo
                    if self.board[r][c] == self.current_player:
                        return True
                    r += dr
                    c += dc
        return False

    def make_move(self, row, col):
        if not self.is_valid_move(row, col):
            return False
        # lw kanet valid move then hay3melha b2a

        self.board[row][col] = self.current_player
        # Add diagonal directions to the existing row and column directions

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] != self.current_player and self.board[r][c] != ' ':
                # beyfdal mashy fe nafs el direction elly e7na feh l8ayet ma y7sal violation 3ady
                while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] != ' ':
                    # hena beyshof el cell elly ana feha delwa2ty nafs el color beta3 el current lw ah hay-flip elly 2ablaha
                    # b ma3na eno el cell de flagged en da true (valid) fa 3shan keda elly 2ablo momken yet3melo flip
                    if self.board[r][c] == self.current_player:
                        # bey-minus 3shan ygeeb el points beta3et el ai/ player2 elly hayt3melaha flip l8ayet ma yewsal ll point el asleya beta3to
                        r -= dr
                        c -= dc
                        while r != row or c != col:
                            self.board[r][c] = self.current_player
                            r -= dr
                            c -= dc
                        break
                    r += dr
                    c += dc
        self.current_player = 'W' if self.current_player == 'B' else 'B'
        return True

    def get_valid_moves(self):
        # hena beygebly kol el possible moves b2a 3shan el user y5tar menhom
        valid_moves = []
        for i in range(8):
            for j in range(8):
                if self.is_valid_move(i, j):
                    valid_moves.append((i, j))
        return valid_moves

    # llw 5alas el list beta3et el valid 5elset keda indicator en el game 5alas
    def is_game_over(self):
        return len(self.get_valid_moves()) == 0

    def get_winner(self):
        black_count = sum(row.count('B') for row in self.board)
        white_count = sum(row.count('W') for row in self.board)
        if black_count > white_count:
            return 'Black'
        elif white_count > black_count:
            return 'White'
        else:
            return 'Tie'
class OthelloGUI:
    def __init__(self, root, difficulty):
        self.root = root
        self.root.title("Othello")
        self.board = OthelloBoard() #title of the root window or frame to "Othello".
        self.difficulty = difficulty#stores the difficulty level of the game.
        self.create_widgets() #creates and configures the widgets (GUI elements) for the Othello game interface.
        self.update_board() #updates the GUI to reflect the current state of the game board.

    def restart_game(self):
            self.board = OthelloBoard()  # Reinitialize the game board
            self.update_board()  # Update the GUI to reflect the new board
            if self.board.current_player == 'W':
                self.make_computer_move()  # Make the computer move if it's its turn

    # Existing GUI methods like create_widgets, update_board, etc., remain unchanged.
    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="green")
        self.canvas.grid(row=0, column=0, columnspan=8, padx=5, pady=5)#Label should be placed in row 1 and column 0, spanning 8 columns
        # spanning 8 columns (columnspan=8),
        # with 5 pixels of padding both horizontally and vertically (padx=5, pady=5).
        self.canvas.bind("<Button-1>", self.on_click)
        self.lbl_status = tk.Label(self.root, text="Current Player: Black", fg="black") #displaying the initial score of the game
        self.lbl_status.grid(row=1, column=0, columnspan=8, pady=5)
        self.lbl_score = tk.Label(self.root, text="Score - Black: 2, White: 2", fg="black")
        #initial number of remaining moves for each player
        self.lbl_score.grid(row=2, column=0, columnspan=8, pady=5)#place the moves Label within the root window
        self.btn_restart = tk.Button(self.root, text="Restart", command=self.restart_game) #creates a Button widget labeled "Restart",
        # When this button is clicked, it will call the restart_game method.
        self.btn_restart.grid(row=3, column=0, columnspan=8, pady=5)

    def update_board(self):
        self.canvas.delete("all")
        valid_moves = self.board.get_valid_moves()
        ai_thinking = self.lbl_status.cget("text") == "AI Thinking..."  # Check if AI is thinking
        for i in range(8):
            for j in range(8):
                x1, y1 = j * 50, i * 50
                x2, y2 = x1 + 50, y1 + 50
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="black")
                if (i, j) in valid_moves and not ai_thinking:  # Draw red dot only if AI is not thinking
                    dot_size = 5  # Adjust dot size as needed
                    self.canvas.create_oval(x1 + (50 - dot_size) // 2, y1 + (50 - dot_size) // 2,
                                            x1 + (50 + dot_size) // 2, y1 + (50 + dot_size) // 2,
                                            outline="red", width=1)  # Draw small red dot with thin border
                if self.board.board[i][j] == 'B':
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="black", outline="black")
                elif self.board.board[i][j] == 'W':
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="white", outline="black")
        self.lbl_status.config(text=f"Current Player: {self.board.current_player}")
        black_score = sum(row.count('B') for row in self.board.board)
        white_score = sum(row.count('W') for row in self.board.board)
        self.lbl_score.config(text=f"Score - Black: {black_score}, White: {white_score}")

    def evaluate_board(self, board):
        # Updated evaluation function to prioritize corner and edge positions and consider piece stability
        corner_positions = [(0, 0), (0, 7), (7, 0), (7, 7)]
        edge_positions = [(0, i) for i in range(8)] + [(i, 0) for i in range(8)] + [(7, i) for i in range(8)] + [(i, 7)
                                                                                                                 for i
                                                                                                                 in
                                                                                                                 range(
                                                                                                                     8)]
        corner_weight = 20
        edge_weight = 5
        stability_weight = 1

        black_count = sum(row.count('B') for row in board.board)
        white_count = sum(row.count('W') for row in board.board)

        # Calculate stability for each piece
        stability_black = self.calculate_stability(board, 'B')
        stability_white = self.calculate_stability(board, 'W')

        # Calculate score based on counts, corner/edge positions, and stability
        score = (black_count - white_count) + \
                corner_weight * (sum(board.board[i][j] == 'B' for i, j in corner_positions) -
                                 sum(board.board[i][j] == 'W' for i, j in corner_positions)) + \
                edge_weight * (sum(board.board[i][j] == 'B' for i, j in edge_positions) -
                               sum(board.board[i][j] == 'W' for i, j in edge_positions)) + \
                stability_weight * (stability_black - stability_white)
        return score

    def calculate_stability(self, board, player):
        # Helper function to calculate stability of pieces for a player
        stable_count = 0
        for i in range(8):
            for j in range(8):
                if board.board[i][j] == player:
                    # Check if the piece is stable
                    if self.is_stable(board, i, j):
                        stable_count += 1
        return stable_count

    def is_stable(self, board, row, col):
        # Helper function to check if a piece is stable
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board.board[r][c] != board.board[row][col] and board.board[r][c] != ' ':
                    return False  # Found an opponent piece in this direction
                r += dr
                c += dc
        return True  # No opponent pieces found in any direction

    def on_click(self, event):
        col = event.x // 50
        row = event.y // 50
        if self.board.current_player == 'B' and self.board.is_valid_move(row, col):
            if self.board.make_move(row, col):
                self.update_board()
                if not self.board.is_game_over() and self.board.current_player == 'W':
                    self.root.after(500, self.make_computer_move)  # Add a slight delay before computer move
                elif self.board.is_game_over():
                    self.end_game()

    def make_computer_move(self):
        if self.board.current_player == 'W':
            best_move = self.get_best_move(self.board, max_depth=self.difficulty)
            if best_move:
                self.board.make_move(best_move[0], best_move[1])
                self.update_board()
                if self.board.is_game_over():
                    self.end_game()

    def get_best_move(self, game, max_depth=4, alpha=float('-inf'), beta=float('inf')):
        return self.alphabeta(game, max_depth, alpha, beta, maximizing_player=True)[1]

    # Use the Alpha-Beta pruning algorithm to find the best move
    def alphabeta(self, game, depth, alpha=float('-inf'), beta=float('inf'), maximizing_player=True):
        if depth == 0 or game.is_game_over():
            return self.evaluate_game_state(game), None

        valid_moves = game.get_valid_moves()

        if maximizing_player:
            max_eval = float("-inf")
            best_move = None
            for move in valid_moves:
                new_game = copy.deepcopy(game)
                new_game.make_move(*move)
                eval, _ = self.alphabeta(new_game, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if alpha >= beta:
                    break
            return max_eval, best_move
        else:
            min_eval = float("inf")
            best_move = None
            for move in valid_moves:
                new_game = copy.deepcopy(game)
                new_game.make_move(*move)
                eval, _ = self.alphabeta(new_game, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval,best_move

    # hena de el utility fun elly haneshta8al beha fel alpha-beta
    def evaluate_game_state(self, game):
        corner_positions = [(0, 0), (0, 7), (7, 0), (7, 7)]
        edge_positions = [(0, i) for i in range(1, 7)] + [(7, i) for i in range(1, 7)] + \
                     [(i, 0) for i in range(1, 7)] + [(i, 7) for i in range(1, 7)]

    # Weights for various factors
        weights = {
        'corner_weight': 25,
        'edge_weight': 10,
        'mobility_weight': 5,
        'disc_weight': 1,
        'late_game_weight': 2
        }

    # Calculate corner and edge control
        corner_count = sum(game.board[x][y] == game.current_player for x, y in corner_positions)
        edge_count = sum(game.board[x][y] == game.current_player for x, y in edge_positions)

    # Mobility (number of valid moves)
        player_moves = len(game.get_valid_moves())
        opponent_moves = len(OthelloBoard().get_valid_moves())  # Opponent's moves assuming opponent is opposite color

    # Disc count
        player_disc_count = sum(row.count(game.current_player) for row in game.board)
        opponent_disc_count = sum(row.count('W' if game.current_player == 'B' else 'B') for row in game.board)

    # Combine evaluation factors
        if len(game.board) * len(game.board[0]) - player_disc_count - opponent_disc_count < 10:
        # Late game scenario, focus more on disc count
            disc_score = (player_disc_count - opponent_disc_count) * weights['late_game_weight']
        else:
            disc_score = player_disc_count - opponent_disc_count

        evaluation = (corner_count * weights['corner_weight'] +
                    edge_count * weights['edge_weight'] +
                    (player_moves - opponent_moves) * weights['mobility_weight'] +
                    disc_score * weights['disc_weight'])

        return evaluation

    def end_game(self):
        winner = self.board.get_winner()
        if winner == 'Tie':
            messagebox.showinfo("Game Over", "It's a tie!")
        else:
            messagebox.showinfo("Game Over", f"The winner is {winner}!")
        self.restart_game()

def easy_difficulty():
    return 2

def medium_difficulty():
    return 4

def hard_difficulty():
    return 6

def select_difficulty(difficulty):
    if difficulty == 1:
        return easy_difficulty()
    elif difficulty == 2:
        return medium_difficulty()
    elif difficulty == 3:
        return hard_difficulty()
    else:
        print("Invalid difficulty level. Defaulting to medium.")
        return medium_difficulty()

if __name__ == "__main__":
    root = tk.Tk() # main application window
    difficulty = int(input("Enter the difficulty level (1 for Easy, 2 for Medium, 3 for Hard): "))
    depth = select_difficulty(difficulty)
    gui = OthelloGUI(root, depth)
    root.mainloop() # Tkinter event loop
