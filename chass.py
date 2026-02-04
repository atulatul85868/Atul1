import tkinter as tk
from tkinter import messagebox

class ChessGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Chess - Gemini")
        
        # State Management
        self.turn = "white"
        self.selected_sq = None  # (row, col)
        self.valid_moves = []
        
        # Unicode characters for Chess pieces
        self.pieces = {
            'white': {'r': '♖', 'n': '♘', 'b': '♗', 'q': '♕', 'k': '♔', 'p': '♙'},
            'black': {'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟'}
        }
        
        # Initial Board Layout
        self.board = self.create_initial_board()
        
        # GUI Components
        self.buttons = [[None for _ in range(8)] for _ in range(8)]
        self.create_widgets()

    def create_initial_board(self):
        """Creates the starting 8x8 board configuration."""
        layout = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p'] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            ['P'] * 8,
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        
        board = [[None for _ in range(8)] for _ in range(8)]
        for r in range(8):
            for c in range(8):
                char = layout[r][c]
                if char:
                    color = "white" if char.isupper() else "black"
                    piece_type = char.lower()
                    board[r][c] = {"type": piece_type, "color": color}
        return board

    def create_widgets(self):
        """Builds the 8x8 grid of buttons for the UI."""
        self.container = tk.Frame(self.root, bg="#333", padx=10, pady=10)
        self.container.pack()
        
        self.status_label = tk.Label(self.root, text="White's Turn", font=("Arial", 14, "bold"), pady=10)
        self.status_label.pack()

        for r in range(8):
            for c in range(8):
                color = "#f0d9b5" if (r + c) % 2 == 0 else "#b58863"
                btn = tk.Button(
                    self.container, 
                    text="", 
                    font=("Arial", 32), 
                    width=2, 
                    height=1,
                    bg=color,
                    activebackground="#7b9e4a",
                    command=lambda row=r, col=c: self.on_click(row, col)
                )
                btn.grid(row=r, column=c)
                self.buttons[r][c] = btn
        
        self.update_board_display()

    def update_board_display(self):
        """Refreshes button text and colors based on board state."""
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                btn = self.buttons[r][c]
                
                # Set piece text
                if piece:
                    btn.config(text=self.pieces[piece['color']][piece['type']], fg="black" if piece['color'] == 'black' else "#fff")
                else:
                    btn.config(text="")
                
                # Reset background colors
                base_color = "#f0d9b5" if (r + c) % 2 == 0 else "#b58863"
                
                if self.selected_sq == (r, c):
                    btn.config(bg="#7b9e4a") # Highlight selected
                elif (r, c) in self.valid_moves:
                    btn.config(bg="#a9bd5c") # Highlight valid move
                else:
                    btn.config(bg=base_color)

    def on_click(self, r, c):
        """Handles logic for selecting pieces and executing moves."""
        piece = self.board[r][c]

        # Case 1: Clicked a valid destination for a move
        if (r, c) in self.valid_moves:
            self.move_piece(self.selected_sq[0], self.selected_sq[1], r, c)
            self.selected_sq = None
            self.valid_moves = []
            self.update_board_display()
            return

        # Case 2: Selected a piece of the current turn's color
        if piece and piece['color'] == self.turn:
            self.selected_sq = (r, c)
            self.valid_moves = self.get_valid_moves(r, c)
        else:
            self.selected_sq = None
            self.valid_moves = []
        
        self.update_board_display()

    def get_valid_moves(self, r, c):
        """Calculates valid squares for the piece at (r, c)."""
        piece = self.board[r][c]
        if not piece: return []
        
        moves = []
        p_type = piece['type']
        color = piece['color']
        
        directions = {
            'r': [(0,1), (0,-1), (1,0), (-1,0)],
            'b': [(1,1), (1,-1), (-1,1), (-1,-1)],
            'q': [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)],
            'k': [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)],
            'n': [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]
        }

        if p_type == 'p':
            direction = -1 if color == 'white' else 1
            # Forward
            if self.is_on_board(r + direction, c) and not self.board[r + direction][c]:
                moves.append((r + direction, c))
                # Initial double move
                start_row = 6 if color == 'white' else 1
                if r == start_row and not self.board[r + (2 * direction)][c]:
                    moves.append((r + (2 * direction), c))
            # Captures
            for dc in [-1, 1]:
                nr, nc = r + direction, c + dc
                if self.is_on_board(nr, nc):
                    target = self.board[nr][nc]
                    if target and target['color'] != color:
                        moves.append((nr, nc))

        elif p_type in ['r', 'b', 'q']:
            for dr, dc in directions[p_type]:
                nr, nc = r + dr, c + dc
                while self.is_on_board(nr, nc):
                    target = self.board[nr][nc]
                    if not target:
                        moves.append((nr, nc))
                    else:
                        if target['color'] != color:
                            moves.append((nr, nc))
                        break
                    nr += dr
                    nc += dc
                    
        elif p_type in ['n', 'k']:
            for dr, dc in directions[p_type]:
                nr, nc = r + dr, c + dc
                if self.is_on_board(nr, nc):
                    target = self.board[nr][nc]
                    if not target or target['color'] != color:
                        moves.append((nr, nc))
                        
        return moves

    def is_on_board(self, r, c):
        return 0 <= r < 8 and 0 <= c < 8

    def move_piece(self, from_r, from_c, to_r, to_c):
        """Moves a piece on the board and handles turn switching."""
        piece = self.board[from_r][from_c]
        target = self.board[to_r][to_c]
        
        # Handle Win Condition (King Capture)
        if target and target['type'] == 'k':
            messagebox.showinfo("Game Over", f"{self.turn.capitalize()} Wins by capturing the King!")
            self.root.destroy()
            return

        # Execute move
        self.board[to_r][to_c] = piece
        self.board[from_r][from_c] = None
        
        # Promotion (Simple auto-queen)
        if piece['type'] == 'p' and (to_r == 0 or to_r == 7):
            piece['type'] = 'q'

        # Switch Turn
        self.turn = "black" if self.turn == "white" else "white"
        self.status_label.config(text=f"{self.turn.capitalize()}'s Turn")

if __name__ == "__main__":
    root = tk.Tk()
    game = ChessGame(root)
    root.mainloop()