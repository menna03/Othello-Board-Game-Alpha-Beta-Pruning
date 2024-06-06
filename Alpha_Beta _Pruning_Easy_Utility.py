import copy
import tkinter as tk
from tkinter import messagebox

class OthelloBoard:
    def __init__(self):
        self.board = [[' '] * 8 for _ in range(8)]
        self.board[3][3] = 'W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'
        self.board[4][4] = 'W'
        self.current_player = 'B'
        self.black_moves = 30  # Counter for black player's moves
        self.white_moves = 30

    def is_valid_move(self, row, col):
        if row < 0 or row >= 8 or col < 0 or col >= 8 or self.board[row][col] != ' ':
            return False
        directions = [(-1, 0), (1, 0), (0, 1),(0,-1)]
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
        if self.current_player == 'B':
            self.black_moves -= 1
        else:
            self.white_moves -= 1

        # lw kanet valid move then hay3melha b2a
        self.board[row][col] = self.current_player
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
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
                        # hena b2a bey3mel flip l elly fel nos
                        while r != row or c != col:
                            self.board[r][c] = self.current_player
                            r -= dr
                            c -= dc
                        break
                    # hena lw mal2ash fel row,col da valid move hayd5ol fel row,col elly b3do w y3eed tany
                    r += dr
                    c += dc
        # hena bey-switch el players 3ady
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
        if self.black_moves == 0 or self.white_moves == 0:
            return True
        # Check if there are no valid moves for current player and also switch to see if the other player has moves
        if len(self.get_valid_moves()) == 0:
            self.switch_player()
            if len(self.get_valid_moves()) == 0:
                return True
            self.switch_player()
        return False

    def switch_player(self):
        self.current_player = 'W' if self.current_player == 'B' else 'B'

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
    def __init__(self, ro, difficulty):
        self.root = ro
        self.board = OthelloBoard() #title of the root window or frame to "Othello".
        self.difficulty = difficulty #stores the difficulty level of the game.
        self.create_widgets() #creates and configures the widgets (GUI elements) for the Othello game interface.
        self.update_board() #updates the GUI to reflect the current state of the game board.


    def restart_game(self):
        self.board = OthelloBoard()  # Reinitialize the game board
        self.black_moves = 0  # Reset black player's move counter
        self.white_moves = 0  # Reset white player's move counter
        self.update_board()  # Update the GUI to reflect the new board
        if self.board.current_player == 'W':
            self.make_computer_move()  # Make the computer move if it's its turn

    # Existing GUI methods like create_widgets, update_board, etc., remain unchanged.
    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="green")
        self.canvas.grid(row=0, column=0, columnspan=8, padx=5, pady=5) #It specifies that the Canvas should be placed in row 0 and column 0,
        # spanning 8 columns (columnspan=8),
        # with 5 pixels of padding both horizontally and vertically (padx=5, pady=5).
        self.canvas.bind("<Button-1>", self.on_click) #This means that when the left mouse button is clicked on the Canvas,
        # the on_click method will be called.
        self.lbl_status = tk.Label(self.root, text="Current Player: Black", fg="black") #initialize el board b en door el black
        self.lbl_status.grid(row=1, column=0, columnspan=8, pady=5) #Label should be placed in row 1 and column 0, spanning 8 columns
        self.lbl_score = tk.Label(self.root, text="Score - Black: 2, White: 2", fg="black") #displaying the initial score of the game
        self.lbl_score.grid(row=2, column=0, columnspan=8, pady=5) #place the score Label within the root window or frame
        self.lbl_moves = tk.Label(self.root, text="Remaining moves - Black: 30, White: 30", fg="black")
        #initial number of remaining moves for each player
        self.lbl_moves.grid(row=3, column=0, columnspan=8, pady=5) #place the moves Label within the root window
        self.btn_restart = tk.Button(self.root, text="Restart", command=self.restart_game) #creates a Button widget labeled "Restart",
        # When this button is clicked, it will call the restart_game method.
        self.btn_restart.grid(row=4, column=0, columnspan=8, pady=5) #place the Restart button within the root window
    def update_board(self):
        self.canvas.delete("all")
        valid_moves = self.board.get_valid_moves()
        ai_thinking = self.lbl_status.cget("text") == "AI Thinking..."  # Check if AI is thinking
        for i in range(8):
            for j in range(8):
                x1, y1 = j * 50, i * 50
                x2, y2 = x1 + 50, y1 + 50
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="black")
                if (i, j) in valid_moves and not ai_thinking:  # Draw clear circle only if AI is not thinking
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, outline="black",
                                            fill="green")  # Draw clear circle with same size as black and white ones
                if self.board.board[i][j] == 'B':
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="black", outline="black")
                elif self.board.board[i][j] == 'W':
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="white", outline="black")
        self.lbl_status.config(text=f"Current Player: {self.board.current_player}")
        black_score = sum(row.count('B') for row in self.board.board)
        white_score = sum(row.count('W') for row in self.board.board)
        self.lbl_score.config(text=f"Score - Black: {black_score}, White: {white_score}")
        self.lbl_moves.config(
            text=f"Remaining moves - Black: {self.board.black_moves}, White: {self.board.white_moves}")

    # el function de 3shan tesama3  lma ne5tar makan mn el gui eandena fel functions
    def on_click(self, event):
        col = event.x // 50
        row = event.y // 50
        if self.board.current_player == 'B' and self.board.is_valid_move(row, col):
            self.board.make_move(row, col)
            self.update_board()
            if self.board.is_game_over():
                self.end_game()
            else:
                # Check for AI moves after human plays
                self.root.after(500, self.make_computer_move)
        # Check if no moves are available after an attempt
        elif self.board.current_player == 'B' and not self.board.get_valid_moves():
            self.board.switch_player()  # If human has no move, switch to AI
            self.root.after(500, self.make_computer_move)  # Delay for AI to make a move

    # Make a move for the computer player
    def make_computer_move(self):
        if self.board.current_player == 'W':
            valid_moves = self.board.get_valid_moves()
            if valid_moves:
                best_move = self.get_best_move(self.board, max_depth=self.difficulty)
                if best_move:  # Ensure best_move is not None before using it
                    self.board.make_move(best_move[0], best_move[1])
                    self.update_board()
                    if self.board.is_game_over():
                        self.end_game()
                else:
                    # Handle situation when no best move is returned
                    messagebox.showinfo("No Moves", "AI has no valid moves, passing back to player.")
                    self.board.switch_player()
                    self.update_board()
            else:
                # If AI has no valid moves, switch back to the human player
                self.board.switch_player()
                self.update_board()

    # Get the best move for the current game state
    # bey-call el alpha beta pruning w y5tar el move based on it
    def get_best_move(self, game, max_depth, alpha=float('-inf'), beta=float('inf')):
        # Use alpha-beta pruning to find the best move
        max_eval, best_move = self.alphabeta(game, max_depth, alpha, beta, maximizing_player=True)
        if max_eval != float('-inf'):  # This checks if any evaluation was made
            return best_move
        return None  # Explicitly return None if no evaluation changed the initial max_eval

    # Use the Alpha-Beta pruning algorithm to find the best move
    def alphabeta(self, game, depth, alpha=float('-inf'), beta=float('inf'), maximizing_player=True):
        if depth == 0 or game.is_game_over():
            return self.evaluate_game_state(game), None

        valid_moves = game.get_valid_moves()
        if not valid_moves:  # Early exit if no valid moves are available
            return self.evaluate_game_state(game), None

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
            return min_eval, best_move

    # hena de el utility fun elly haneshta8al beha fel alpha-beta
    def evaluate_game_state(self, game):
        corner_positions = [(0, 0), (0, 7), (7, 0), (7, 7)]  # corners
        edge_positions = [(0, i) for i in range(1, 7)] + [(7, i) for i in range(1, 7)] + \
                         [(i, 0) for i in range(1, 7)] + [(i, 7) for i in range(1, 7)] # edges

        #  weights for different evaluation factors
        weights = {
            'corner_weight': 15,
            'edge_weight': 10,
            'mobility_weight': 8, # number of legal moves available to a player
            'disc_weight': 2, # number of discs  owned by the current player compared to the opponent.
            'flip_weight': 20, # if B W W B we flip 2 W only if B W W W B we flip 3 so it is better so we make for it more wight
        }

        # Initialize counters for flip counts and potential flip counts
        flip_count = 0

        # Count the number of player pieces in corner and edge positions
        corner_count = sum(game.board[x][y] == game.current_player for x, y in corner_positions)
        edge_count = sum(game.board[x][y] == game.current_player for x, y in edge_positions)

        # Calculate the difference between player and opponent valid moves
        player_moves = len(game.get_valid_moves())
        opponent_moves = len(OthelloBoard().get_valid_moves())

        # Count the number of player and opponent discs on the board
        player_disc_count = sum(row.count(game.current_player) for row in game.board)
        opponent_disc_count = sum(row.count('W' if game.current_player == 'B' else 'B') for row in game.board)

        # Calculate the flip count and potential flip count for each valid move
        for move in game.get_valid_moves():
            temp_game = copy.deepcopy(game)
            temp_game.make_move(*move)
            flip_count += abs(len(game.board) - temp_game.board.count(game.current_player))

        # Calculate the difference in disc count
        disc_score = player_disc_count - opponent_disc_count

        # Calculate scores based on evaluation factors and their weights
        corner_score = corner_count * weights['corner_weight']
        edge_score = edge_count * weights['edge_weight']
        mobility_score = (player_moves - opponent_moves) * weights['mobility_weight']
        disc_score = disc_score * weights['disc_weight']
        flip_score = flip_count * weights['flip_weight']

        # Sum up the scores to get the final evaluation score
        evaluation = corner_score + edge_score + mobility_score + disc_score + flip_score
        # Return the evaluation score
        return evaluation

    def end_game(self):
        winner = self.board.get_winner()
        if winner == 'Tie':
            messagebox.showinfo("Game Over", "It's a tie!")
        else:
            messagebox.showinfo("Game Over", f"The winner is {winner}!")
        self.restart_game()

def easy_difficulty():
    return 1

def medium_difficulty():
    return 5

def hard_difficulty():
    return 7

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