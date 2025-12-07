
import tkinter as tk
from tkinter import ttk, messagebox
import copy
import time
import random

from constraints import is_valid, get_valid_values
from csp import build_csp
from arc_consistency import ac3_with_tracking, update_board_with_domains
from backtracking import backtracking_solver_fc, is_complete


class SudokuSolverGUI:

    def __init__(self, root):
        """Initialize GUI"""
        self.root = root
        self.root.title("Sudoku CSP Solver")
        
        # Store board state
        self.board = [[0] * 9 for _ in range(9)]
        self.cells = [[None] * 9 for _ in range(9)]
        
        # AC-3 tracking for visualization: store a list of runs (each run is a list of steps)
        self.ac3_runs = []
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
                      variable=self.mode_var, value="mode1", command=self.on_mode_change).pack(side=tk.LEFT)
        tk.Radiobutton(top_frame, text="Mode 2: Input Your Puzzle",
                      variable=self.mode_var, value="mode2", command=self.on_mode_change).pack(side=tk.LEFT)
        
        # Sudoku grid
        grid_frame = tk.Frame(self.root, bg="black")
        grid_frame.pack(pady=10)
        
        for r in range(9):
            for c in range(9):
                # Thicker borders for 3x3 boxes
                padx = (2 if c % 3 == 0 else 1, 2 if c % 3 == 2 else 1)
                pady = (2 if r % 3 == 0 else 1, 2 if r % 3 == 2 else 1)
                
                cell = tk.Entry(grid_frame, width=3, font=("Arial", 16),
                              justify="center", bg="white", state="readonly")
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
            
            if is_valid(temp_board, row, col, num):
                cell.config(bg="lightgreen")
                self.board[row][col] = num
            else:
                cell.config(bg="pink")
                self.status_label.config(text=f"Constraint violated at ({row+1},{col+1})", fg="red")
        except ValueError:
            cell.config(bg="pink")
    
    def on_mode_change(self):
        """Handle mode change - enable/disable cells for editing"""
        mode = self.mode_var.get()
        
        for r in range(9):
            for c in range(9):
                cell = self.cells[r][c]
                if mode == "mode2":
                    # User input mode - enable editing
                    cell.config(state="normal")
                else:
                    # AI solve mode - disable editing
                    cell.config(state="readonly")
    
    def generate_puzzle(self):
        """Generate random solvable puzzle"""
        self.clear_board()
        
        # Fill diagonal boxes first (independent - no conflicts)
        for box in range(3):
            nums = list(range(1, 10))
            random.shuffle(nums)
            idx = 0
            for r in range(box * 3, box * 3 + 3):
                for c in range(box * 3, box * 3 + 3):
                    self.board[r][c] = nums[idx]
                    idx += 1
        
        # Use backtracking to fill rest
        domains, neighbors = build_csp(self.board)
        backtracking_solver_fc(self.board, domains, neighbors)
        
        # Remove cells randomly (create puzzle)
        difficulty = 60
        cells_to_remove = random.sample([(r, c) for r in range(9) for c in range(9)], difficulty)
        for r, c in cells_to_remove:
            self.board[r][c] = 0
        
        self.update_display()
        self.status_label.config(text="Random puzzle generated!", fg="green")
    
    def solve_with_visualization(self):
        """Solve puzzle with AC-3 + Backtracking + Forward Checking"""
        self.read_board_from_gui()
        start_time = time.time()
        
        # Build CSP
        domains, neighbors = build_csp(self.board)
        
        # Apply AC-3
        self.status_label.config(text="Running AC-3...", fg="blue")
        self.root.update()
        
        while not is_complete(self.board):
            
            self.status_label.config(text="Entered Arc", fg="blue")
            self.root.update()
            time.sleep(0.5)
            # Run AC-3 and append the new tracking steps as a separate run
            success, new_steps = ac3_with_tracking(domains, neighbors)
            if new_steps:
                # keep each AC-3 invocation as a separate entry (so runs are separated)
                self.ac3_runs.append(list(new_steps))
        
            # if not success:
            #     result = backtracking_solver_fc(self.board, domains, neighbors, callback=self._update_callback)
            #     # messagebox.showerror("Error", "Puzzle is unsolvable!")
            #     # return
        
            # Update board from AC-3
            flag = update_board_with_domains(self.board, domains)
            
            if(flag == False):
                print("Entered backtracking")
                self.status_label.config(text="AC-3 done. Running Backtracking + FC...", fg="red")
                self.root.update()
                time.sleep(0.5)
                result = backtracking_solver_fc(self.board, domains, neighbors, callback=self._update_callback)
                if not result:
                    messagebox.showerror("Error", "Puzzle is unsolvable!")
                    return
                
            self.update_display()
            self.root.update()

        
        self.solution_time = time.time() - start_time
        self.update_display()
        total_ac3_steps = sum(len(run) for run in self.ac3_runs)
        self.status_label.config(
            text=f"Solved in {self.solution_time:.3f}s! AC-3 steps: {total_ac3_steps}",
            fg="green"
        )
    
    def _update_callback(self, board):
        """Callback for backtracking visualization"""
        self.update_display()
        self.root.update()
        time.sleep(0.01)
    
    def read_board_from_gui(self):
        """Read board state from GUI cells"""
        for r in range(9):
            for c in range(9):
                val = self.cells[r][c].get().strip()
                self.board[r][c] = int(val) if val.isdigit() else 0
    
    def update_display(self):
        """Update GUI display with current board state"""
        for r in range(9):
            for c in range(9):
                cell = self.cells[r][c]
                # Temporarily enable cell to update content
                cell.config(state="normal")
                cell.delete(0, tk.END)
                val = self.board[r][c]
                if val != 0:
                    cell.insert(0, str(val))
                    if self.mode_var.get() == "mode1":
                        cell.config(bg="lightyellow")
                # Return to appropriate state based on current mode
                if self.mode_var.get() == "mode1":
                    cell.config(state="readonly")
                else:
                    cell.config(state="normal")
    
    def clear_board(self):
        """Clear the board"""
        self.board = [[0] * 9 for _ in range(9)]
        # Reset AC-3 history when board is cleared / new board created
        self.ac3_runs = []
        for r in range(9):
            for c in range(9):
                self.cells[r][c].delete(0, tk.END)
                self.cells[r][c].config(bg="white")
        self.status_label.config(text="Board cleared", fg="blue")
    
    def show_ac3_steps(self):
        """Display AC-3 constraint propagation steps"""
        if not self.ac3_runs:
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
        
        total_steps = sum(len(run) for run in self.ac3_runs)
        text.insert(tk.END, f"Total AC-3 revisions: {total_steps}\n")
        text.insert(tk.END, "=" * 50 + "\n\n")
        # Display runs separately so each AC-3 invocation is distinct
        shown = 0
        for run_idx, run in enumerate(self.ac3_runs, start=1):
            text.insert(tk.END, f"--- AC-3 Run {run_idx}: {len(run)} revisions ---\n")
            for step in run:
                if shown >= 100:
                    break
                xi, xj = step['arc']
                intial_domain = step['initial_domain_Xi']
                domain = step['domain_Xi']
                shown += 1
                text.insert(tk.END, f"Run {run_idx} - Revision {shown}:\n")
                text.insert(tk.END, f"  Arc: {xi} -> {xj}\n")
                text.insert(tk.END, f"  Intial Domain : {sorted(intial_domain)}\n")
                text.insert(tk.END, f"  Domain reduced to: {sorted(domain)}\n\n")
            if shown >= 100:
                break

        if total_steps > 100:
            text.insert(tk.END, f"... and {total_steps - 100} more steps\n")
        
        text.config(state=tk.DISABLED)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = SudokuSolverGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
