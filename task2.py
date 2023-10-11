import tkinter as tk
from tkinter import messagebox

AI = 'O'
HUMAN = 'X'
EMPTY_CELL = ' '

class TicTacToeGame:
    def __init__(self):
        self.board = [[EMPTY_CELL] * 3 for _ in range(3)]
        self.current_player = HUMAN
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe")
        self.buttons = [[None] * 3 for _ in range(3)]
        self.create_buttons()

    def create_buttons(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.root, text=EMPTY_CELL, width=10, height=5,
                                   command=lambda row=i, col=j: self.make_move(row, col))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

        restart_button = tk.Button(self.root, text="Restart", command=self.restart_game)
        restart_button.grid(row=3, columnspan=3)

    def make_move(self, row, col):
        if self.board[row][col] == EMPTY_CELL:
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            if self.check_winner(self.current_player):
                self.game_over(self.current_player)
            elif self.is_board_full():
                self.game_over(None)
            else:
                self.current_player = AI
                self.ai_move()

    def ai_move(self):
        best_score = -float('inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == EMPTY_CELL:
                    self.board[i][j] = AI
                    score = self.minimax(self.board, 0, False)
                    self.board[i][j] = EMPTY_CELL
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        row, col = best_move
        self.board[row][col] = AI
        self.buttons[row][col].config(text=AI)
        if self.check_winner(AI):
            self.game_over(AI)
        elif self.is_board_full():
            self.game_over(None)
        else:
            self.current_player = HUMAN

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner(HUMAN):
            return -1
        elif self.check_winner(AI):
            return 1
        elif self.is_board_full():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == EMPTY_CELL:
                        board[i][j] = AI
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = EMPTY_CELL
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == EMPTY_CELL:
                        board[i][j] = HUMAN
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = EMPTY_CELL
                        best_score = min(score, best_score)
            return best_score

    def check_winner(self, player):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] == player:
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] == player:
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
            return True
        return False

    def is_board_full(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == EMPTY_CELL:
                    return False
        return True

    def game_over(self, winner):
        if winner:
            messagebox.showinfo("Game Over", f"{winner} wins!")
        else:
            messagebox.showinfo("Game Over", "It's a draw!")
        self.restart_game()

    def restart_game(self):
        self.board = [[EMPTY_CELL] * 3 for _ in range(3)]
        self.current_player = HUMAN
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=EMPTY_CELL)

    def start(self):
        self.root.mainloop()

# Start the game
game = TicTacToeGame()
game.start()