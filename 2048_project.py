from tkinter import *
import random

class Play_2048(Tk):
    game_board = []
    new_random_tiles = [2, 2, 2, 2, 2, 2, 4]
    score = 0
    high_score = 0
    game_score = 0
    highest_score = 0
    paused = False  # New attribute for pause state

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.game_score = StringVar(self)
        self.game_score.set("0")
        self.highest_score = StringVar(self)
        self.highest_score.set("0")
        
        self.button_frame = Frame(self)
        self.button_frame.grid(row=2, column=0, columnspan=4)
        Button(self.button_frame, text="New Game", font=("times new roman", 15), command=self.new_game).grid(row=0, column=0)
        Button(self.button_frame, text="Undo", font=("times new roman", 15), command=self.undo_move).grid(row=0, column=1)
        Button(self.button_frame, text="Pause/Resume", font=("times new roman", 15), command=self.toggle_pause).grid(row=0, column=2)  # New pause/resume button
        self.button_frame.pack(side="top")

        Label(self.button_frame, text="Score:", font=("times new roman", 15)).grid(row=0, column=3)
        Label(self.button_frame, textvariable=self.game_score, font=("times new roman", 15)).grid(row=0, column=4)
        Label(self.button_frame, text="Record:", font=("times new roman", 15)).grid(row=0, column=5)
        Label(self.button_frame, textvariable=self.highest_score, font=("times new roman", 15)).grid(row=0, column=6)

        self.canvas = Canvas(self, width=410, height=410, borderwidth=5, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand=False)

        self.new_game()

    def save_state(self):
        self.previous_board = [row[:] for row in self.game_board]
        self.previous_score = self.score

    def undo_move(self):
        if hasattr(self, 'previous_board'):
            self.game_board = [row[:] for row in self.previous_board]
            self.score = self.previous_score
            self.show_board()
            self.game_score.set(str(self.score))
    
    def new_tiles(self):
        index = random.randint(0, 6)
        while not self.full():
            x = random.randint(0, 3)
            y = random.randint(0, 3)
            if self.game_board[x][y] == 0:
                self.game_board[x][y] = self.new_random_tiles[index]
                x1 = y * 105
                y1 = x * 105
                x2 = x1 + 105 - 5
                y2 = y1 + 105 - 5
                num = self.game_board[x][y]
                if num == 2:
                    self.square[x, y] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#e0f2f8", tags="rect", outline="", width=0)
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, font=("Arial", 36), fill="#f78a8a", text="2")
                elif num == 4:
                    self.square[x, y] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#b8dbe5", tags="rect", outline="", width=0)
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, font=("Arial", 36), fill="#f78a8a", text="4")
                break

    def show_board(self):
        cellwidth = 105
        cellheight = 105
        self.square = {}

        for column in range(4):
            for row in range(4):
                x1 = column * cellwidth
                y1 = row * cellheight
                x2 = x1 + cellwidth - 5
                y2 = y1 + cellheight - 5
                num = self.game_board[row][column]
                if num == 0:
                    self.show_number0(row, column, x1, y1, x2, y2)
                else:
                    self.show_number(row, column, x1, y1, x2, y2, num)

    def show_number0(self, row, column, a, b, c, d):
        self.square[row, column] = self.canvas.create_rectangle(a, b, c, d, fill="#f5f5f5", tags="rect", outline="")

    def show_number(self, row, column, a, b, c, d, num):
        bg_color = {
            '2': '#eee4da', '4': '#ede0c8', '8': '#edc850', '16': '#edc53f',
            '32': '#f67c5f', '64': '#f65e3b', '128': '#edcf72', '256': '#edcc61',
            '512': '#f2b179', '1024': '#f59563', '2048': '#edc22e',
        }
        color = {
            '2': '#776e65', '4': '#f9f6f2', '8': '#f9f6f2', '16': '#f9f6f2',
            '32': '#f9f6f2', '64': '#f9f6f2', '128': '#f9f6f2', '256': '#f9f6f2',
            '512': '#776e65', '1024': '#f9f6f2', '2048': '#f9f6f2',
        }
        self.square[row, column] = self.canvas.create_rectangle(a, b, c, d, fill=bg_color[str(num)], tags="rect", outline="")
        self.canvas.create_text((a + c) / 2, (b + d) / 2, font=("Arial", 36), fill=color[str(num)], text=str(num))

    def moves(self, event):
        if self.paused:  # Check if the game is paused
            return

        self.save_state()
        
        if event.keysym == 'Down':
            for j in range(4):
                shift = 0
                for i in range(3, -1, -1):
                    if self.game_board[i][j] == 0:
                        shift += 1
                    else:
                        if i - 1 >= 0 and self.game_board[i - 1][j] == self.game_board[i][j]:
                            self.game_board[i][j] *= 2
                            self.score += self.game_board[i][j]
                            self.game_board[i - 1][j] = 0
                        elif i - 2 >= 0 and self.game_board[i - 1][j] == 0 and self.game_board[i - 2][j] == self.game_board[i][j]:
                            self.game_board[i][j] *= 2
                            self.score += self.game_board[i][j]
                            self.game_board[i - 2][j] = 0
                        elif i == 3 and self.game_board[2][j] + self.game_board[1][j] == 0 and self.game_board[0][j] == self.game_board[3][j]:
                            self.game_board[3][j] *= 2
                            self.score += self.game_board[3][j]
                            self.game_board[0][j] = 0
                        if shift > 0:
                            self.game_board[i + shift][j] = self.game_board[i][j]
                            self.game_board[i][j] = 0
            self.show_board()
            self.new_tiles()
            self.game_over()
        elif event.keysym == 'Right':
            for i in range(4):
                shift = 0
                for j in range(3, -1, -1):
                    if self.game_board[i][j] == 0:
                        shift += 1
                    else:
                        if j - 1 >= 0 and self.game_board[i][j - 1] == self.game_board[i][j]:
                            self.game_board[i][j] *= 2
                            self.score += self.game_board[i][j]
                            self.game_board[i][j - 1] = 0
                        elif j - 2 >= 0 and self.game_board[i][j - 1] == 0 and self.game_board[i][j - 2] == self.game_board[i][j]:
                            self.game_board[i][j] *= 2
                            self.score += self.game_board[i][j]
                            self.game_board[i][j - 2] = 0
                        elif j == 3 and self.game_board[i][2] + self.game_board[i][1] == 0 and self.game_board[i][0] == self.game_board[i][3]:
                            self.game_board[i][3] *= 2
                            self.score += self.game_board[i][3]
                            self.game_board[i][0] = 0
                        if shift > 0:
                            self.game_board[i][j + shift] = self.game_board[i][j]
                            self.game_board[i][j] = 0
            self.show_board()
            self.new_tiles()
            self.game_over()
        elif event.keysym == 'Left':
            for i in range(4):
                shift = 0
                for j in range(4):
                    if self.game_board[i][j] == 0:
                        shift += 1
                    else:
                        if j + 1 < 4 and self.game_board[i][j + 1] == self.game_board[i][j]:
                            self.game_board[i][j] *= 2
                            self.score += self.game_board[i][j]
                            self.game_board[i][j + 1] = 0
                        elif j + 2 < 4 and self.game_board[i][j + 1] == 0 and self.game_board[i][j + 2] == self.game_board[i][j]:
                            self.game_board[i][j] *= 2
                            self.score += self.game_board[i][j]
                            self.game_board[i][j + 2] = 0
                        elif j == 0 and self.game_board[i][1] + self.game_board[i][2] == 0 and self.game_board[i][3] == self.game_board[i][0]:
                            self.game_board[i][0] *= 2
                            self.score += self.game_board[i][0]
                            self.game_board[i][3] = 0
                        if shift > 0:
                            self.game_board[i][j - shift] = self.game_board[i][j]
                            self.game_board[i][j] = 0
            self.show_board()
            self.new_tiles()
            self.game_over()
        elif event.keysym == 'Up':
            for j in range(4):
                shift = 0
                for i in range(4):
                    if self.game_board[i][j] == 0:
                        shift += 1
                    else:
                        if i + 1 < 4 and self.game_board[i + 1][j] == self.game_board[i][j]:
                            self.game_board[i][j] *= 2
                            self.score += self.game_board[i][j]
                            self.game_board[i + 1][j] = 0
                        elif i + 2 < 4 and self.game_board[i + 1][j] == 0 and self.game_board[i + 2][j] == self.game_board[i][j]:
                            self.game_board[i][j] *= 2
                            self.score += self.game_board[i][j]
                            self.game_board[i + 2][j] = 0
                        elif i == 0 and self.game_board[1][j] + self.game_board[2][j] == 0 and self.game_board[3][j] == self.game_board[0][j]:
                            self.game_board[0][j] *= 2
                            self.score += self.game_board[0][j]
                            self.game_board[3][j] = 0
                        if shift > 0:
                            self.game_board[i - shift][j] = self.game_board[i][j]
                            self.game_board[i][j] = 0
            self.show_board()
            self.new_tiles()
            self.game_over()

        self.game_score.set(str(self.score))
        if self.score > self.high_score:
            self.high_score = self.score
            self.highest_score.set(str(self.high_score))

    def new_game(self):
        self.score = 0
        self.game_score.set("0")
        self.game_board = [[0, 0, 0, 0] for _ in range(4)]
        self.add_initial_tiles()
        self.show_board()

    def add_initial_tiles(self):
        for _ in range(2):
            while True:
                x = random.randint(0, 3)
                y = random.randint(0, 3)
                if self.game_board[x][y] == 0:
                    self.game_board[x][y] = random.choice([2, 4])
                    break

    def full(self):
        for row in self.game_board:
            if 0 in row:
                return False
        return True

    def game_over(self):
        if self.full() and not self.can_merge():
            self.canvas.create_text(200, 200, text="Game Over", font=("Arial", 36), fill="red")

    def can_merge(self):
        for i in range(4):
            for j in range(4):
                if i + 1 < 4 and self.game_board[i][j] == self.game_board[i + 1][j]:
                    return True
                if j + 1 < 4 and self.game_board[i][j] == self.game_board[i][j + 1]:
                    return True
        return False

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.canvas.create_text(200, 200, text="Paused", font=("Arial", 36), fill="blue", tags="pause_text")
        else:
            self.canvas.delete("pause_text")

if __name__ == "__main__":
    game = Play_2048()
    game.bind("<Key>", game.moves)
    game.mainloop()
