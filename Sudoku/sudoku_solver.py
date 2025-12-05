import tkinter as tk
from tkinter import ttk, messagebox
import copy
from collections import deque
import time
import random

class SudokuSolverGUI:
    """
    Sudoku Solver with GUI showing AC-3 + Backtracking with MRV, LCV, Forward Checking
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku CSP Solver")
        
        # Store board state
        self.board = [[0]*9 for _ in range(9)]
        self.cells = [[None]*9 for _ in range(9)]
        
        # AC-3 tracking for visualization
        self.ac3_steps = []
        self.solution_time = 0
        
        self.setup_gui()
        
    def setup_gui(self):
        """Create GUI layout"""
        # Top frame for mode selection
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)
        
        tk.Label(top_frame, text="Mode:", font=("Arial", 12)).pack(side=tk.LEFT)
        
        self.mode_var = tk.StringVar(value="mode1")
        tk.Radiobutton(top_frame, text="Mode 1: Watch AI Solve", 
                      variable=self.mode_var, value="mode1").pack(side=tk.LEFT)
        tk.Radiobutton(top_frame, text="Mode 2: Input Your Puzzle", 
                      variable=self.mode_var, value="mode2").pack(side=tk.LEFT)
        
        # Sudoku grid
        grid_frame = tk.Frame(self.root, bg="black")
        grid_frame.pack(pady=10)
        
        for r in range(9):
            for c in range(9):
                # Thicker borders for 3x3 boxes
                padx = (2 if c % 3 == 0 else 1, 2 if c % 3 == 2 else 1)
                pady = (2 if r % 3 == 0 else 1, 2 if r % 3 == 2 else 1)
                
                cell = tk.Entry(grid_frame, width=3, font=("Arial", 16), 
                              justify="center", bg="white")
                cell.grid(row=r, column=c, padx=padx, pady=pady)
                self.cells[r][c] = cell
                
                # Validation for user input
                cell.bind("<KeyRelease>", lambda e, r=r, c=c: self.validate_input(r, c))
        
        # Control buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Generate Random Puzzle", 
                 command=self.generate_puzzle).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Solve with AC-3 + FC", 
                 command=self.solve_with_visualization).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Clear Board", 
                 command=self.clear_board).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Show AC-3 Steps", 
                 command=self.show_ac3_steps).pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = tk.Label(self.root, text="Ready", 
                                    font=("Arial", 10), fg="blue")
        self.status_label.pack(pady=5)
    
    def validate_input(self, row, col):
        """Validate user input in real-time"""
        if self.mode_var.get() != "mode2":
            return
            
        cell = self.cells[row][col]
        value = cell.get().strip()
        
        if value == "":
            cell.config(bg="white")
            self.board[row][col] = 0
            return
        
        try:
            num = int(value)
            if num < 1 or num > 9:
                cell.config(bg="pink")
                messagebox.showwarning("Invalid", "Enter 1-9 only")
                return
            
            # Check constraints
            temp_board = [row[:] for row in self.board]
            temp_board[row][col] = num
            
            if self.is_valid(temp_board, row, col, num):
                cell.config(bg="lightgreen")
                self.board[row][col] = num
            else:
                cell.config(bg="pink")
                self.status_label.config(text=f"Constraint violated at ({row+1},{col+1})", fg="red")
        except ValueError:
            cell.config(bg="pink")
    
    def is_valid(self, board, row, col, value):
        """Check Sudoku constraints"""
        # Row check
        for c in range(9):
            if c != col and board[row][c] == value:
                return False
        # Column check
        for r in range(9):
            if r != row and board[r][col] == value:
                return False
        # Box check
        start_r, start_c = (row // 3) * 3, (col // 3) * 3
        for r in range(start_r, start_r + 3):
            for c in range(start_c, start_c + 3):
                if (r, c) != (row, col) and board[r][c] == value:
                    return False
        return True
    
    def generate_puzzle(self):
        """Generate random solvable puzzle"""
        self.clear_board()
        # Fill diagonal boxes first
        for box in range(3):
            nums = list(range(1, 10))
            random.shuffle(nums)
            idx = 0
            for r in range(box*3, box*3+3):
                for c in range(box*3, box*3+3):
                    self.board[r][c] = nums[idx]
                    idx += 1
        # Use backtracking to fill rest
        domains, neighbors = self.build_csp(self.board)
        self.backtracking_solver_fc(self.board, domains, neighbors)
        # Remove cells randomly
        difficulty = 40
        cells_to_remove = random.sample([(r,c) for r in range(9) for c in range(9)], difficulty)
        for r, c in cells_to_remove:
            self.board[r][c] = 0
        self.update_display()
        self.status_label.config(text="Random puzzle generated!", fg="green")
    
    def solve_with_visualization(self):
        """Solve puzzle with AC-3 + Backtracking + Forward Checking"""
        self.read_board_from_gui()
        self.ac3_steps = []
        start_time = time.time()
        
        # Build CSP
        domains, neighbors = self.build_csp(self.board)
        
        # Apply AC-3
        self.status_label.config(text="Running AC-3...", fg="blue")
        self.root.update()
        if not self.ac3_with_tracking(domains, neighbors):
            messagebox.showerror("Error", "Puzzle is unsolvable!")
            return
        
        # Update board from AC-3
        self.update_board_with_domains(self.board, domains)
        self.update_display()
        self.root.update()
        time.sleep(0.5)
        
        # Backtracking with Forward Checking if incomplete
        if not self.is_complete(self.board):
            self.status_label.config(text="AC-3 done. Running Backtracking + FC...", fg="blue")
            self.root.update()
            self.backtracking_solver_fc(self.board, domains, neighbors)
        
        self.solution_time = time.time() - start_time
        self.update_display()
        self.status_label.config(
            text=f"Solved in {self.solution_time:.3f}s! AC-3 steps: {len(self.ac3_steps)}", 
            fg="green"
        )
    
    # ================= CSP & AC-3 =================
    
    def build_csp(self, board):
        """Build domains and neighbors"""
        domains = {}
        neighbors = {}
        for r in range(9):
            for c in range(9):
                cell = (r, c)
                if board[r][c] != 0:
                    domains[cell] = {board[r][c]}
                else:
                    valid = set(range(1, 10))
                    for val in range(1, 10):
                        if not self.is_valid(board, r, c, val):
                            valid.discard(val)
                    domains[cell] = valid
                
                # neighbors: same row, col, box
                neigh = set()
                for cc in range(9):
                    if cc != c:
                        neigh.add((r, cc))
                for rr in range(9):
                    if rr != r:
                        neigh.add((rr, c))
                start_r, start_c = (r//3)*3, (c//3)*3
                for rr in range(start_r, start_r+3):
                    for cc in range(start_c, start_c+3):
                        if (rr, cc) != (r, c):
                            neigh.add((rr, cc))
                neighbors[cell] = list(neigh)
        return domains, neighbors
    
    def ac3_with_tracking(self, domains, neighbors):
        """AC-3 algorithm with step tracking"""
        queue = deque()
        for Xi in domains.keys():
            for Xj in neighbors[Xi]:
                queue.append((Xi, Xj))
        
        while queue:
            Xi, Xj = queue.popleft()
            if self.revise(Xi, Xj, domains):
                self.ac3_steps.append({'arc': (Xi, Xj), 'domain_Xi': domains[Xi].copy(), 'action': 'revised'})
                if len(domains[Xi]) == 0:
                    return False
                for Xk in neighbors[Xi]:
                    if Xk != Xj:
                        queue.append((Xk, Xi))
        return True
    
    def revise(self, Xi, Xj, domains):
        revised = False
        to_remove = []
        for v in domains[Xi]:
            if not any(v != w for w in domains[Xj]):
                to_remove.append(v)
        for v in to_remove:
            domains[Xi].remove(v)
            revised = True
        return revised
    
    def update_board_with_domains(self, board, domains):
        """Fill cells with singleton domains"""
        for (r, c), domain in domains.items():
            if len(domain) == 1 and board[r][c] == 0:
                board[r][c] = next(iter(domain))
    
    # ================= Backtracking + Forward Checking =================
    
    def backtracking_solver_fc(self, board, domains, neighbors):
        """Backtracking with MRV + LCV + Forward Checking"""
        empty = self.find_empty_mrv_fc(domains, board)
        if empty is None:
            return True
        row, col = empty
        cell = (row, col)
        
        for value in self.lcv_order(cell, domains, neighbors):
            if value in domains[cell]:
                board[row][col] = value
                saved_domains = copy.deepcopy(domains)
                domains[cell] = {value}
                
                if self.forward_check(cell, value, domains, neighbors):
                    # visualize
                    self.update_display()
                    self.root.update()
                    time.sleep(0.01)
                    if self.backtracking_solver_fc(board, domains, neighbors):
                        return True
                
                # backtrack
                board[row][col] = 0
                domains = saved_domains
        return False
    
    def find_empty_mrv_fc(self, domains, board):
        min_len = 10
        best_cell = None
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    n = len(domains[(r, c)])
                    if n < min_len:
                        min_len = n
                        best_cell = (r, c)
        return best_cell
    
    def lcv_order(self, cell, domains, neighbors):
        counts = []
        for val in domains[cell]:
            count = sum(1 for neigh in neighbors[cell] if val in domains[neigh])
            counts.append((count, val))
        counts.sort()
        return [v for _, v in counts]
    
    def forward_check(self, cell, value, domains, neighbors):
        for neigh in neighbors[cell]:
            if value in domains[neigh]:
                domains[neigh].remove(value)
                if len(domains[neigh]) == 0:
                    return False
        return True
    
    # ================= GUI Helpers =================
    
    def is_complete(self, board):
        return all(board[r][c] != 0 for r in range(9) for c in range(9))
    
    def read_board_from_gui(self):
        for r in range(9):
            for c in range(9):
                val = self.cells[r][c].get().strip()
                self.board[r][c] = int(val) if val.isdigit() else 0
    
    def update_display(self):
        for r in range(9):
            for c in range(9):
                val = self.board[r][c]
                self.cells[r][c].delete(0, tk.END)
                if val != 0:
                    self.cells[r][c].insert(0, str(val))
                    if self.mode_var.get() == "mode1":
                        self.cells[r][c].config(bg="lightyellow")
    
    def clear_board(self):
        self.board = [[0]*9 for _ in range(9)]
        for r in range(9):
            for c in range(9):
                self.cells[r][c].delete(0, tk.END)
                self.cells[r][c].config(bg="white")
        self.status_label.config(text="Board cleared", fg="blue")
    
    def show_ac3_steps(self):
        if not self.ac3_steps:
            messagebox.showinfo("Info", "No AC-3 steps recorded. Solve a puzzle first!")
            return
        
        steps_window = tk.Toplevel(self.root)
        steps_window.title("AC-3 Constraint Propagation Steps")
        steps_window.geometry("500x400")
        
        text = tk.Text(steps_window, wrap=tk.WORD, font=("Courier", 10))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(steps_window, command=text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text.config(yscrollcommand=scrollbar.set)
        
        text.insert(tk.END, f"Total AC-3 revisions: {len(self.ac3_steps)}\n")
        text.insert(tk.END, "="*50 + "\n\n")
        
        for i, step in enumerate(self.ac3_steps[:100]):
            xi, xj = step['arc']
            domain = step['domain_Xi']
            text.insert(tk.END, f"Step {i+1}:\n")
            text.insert(tk.END, f"  Arc: {xi} -> {xj}\n")
            text.insert(tk.END, f"  Domain reduced to: {sorted(domain)}\n\n")
        
        if len(self.ac3_steps) > 100:
            text.insert(tk.END, f"... and {len(self.ac3_steps)-100} more steps\n")
        
        text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolverGUI(root)
    root.mainloop()
