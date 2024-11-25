import tkinter as tk
from tkinter import messagebox

class SudokuVisualizer:
    def __init__(self, root,puzzle, solution_steps,last_changed_indexes):
        self.root = root
        self.original_puzzle = [row[:] for row in puzzle]  # keep a copy of the original puzzle
        self.solution_steps = solution_steps
        self.current_step = 0
        self.last_changed_indexes = last_changed_indexes
        self.size = 50  # cell size for visualization
        max_steps = len(self.solution_steps) - 1  # maximum step number (0-based)
        # create the UI elements
        self.canvas = tk.Canvas(root, width=9*self.size, height=9*self.size)
        self.canvas.grid(row=0, column=0, columnspan=5)

        self.prev_button = tk.Button(root, text="< Previous", command=self.show_prev_step)
        self.prev_button.grid(row=1, column=0)

        self.next_button = tk.Button(root, text="Next >", command=self.show_next_step)
        self.next_button.grid(row=1, column=1)

        self.jump_label = tk.Label(root, text=f"Go to step:(0,{max_steps})")
        self.jump_label.grid(row=1, column=2)

        self.step_entry = tk.Entry(root, width=5)
        self.step_entry.grid(row=1, column=3)

        self.jump_button = tk.Button(root, text="Go", command=self.jump_to_step)
        self.jump_button.grid(row=1, column=4)

        self.final_button = tk.Button(root, text="Show Final", command=self.show_final)
        self.final_button.grid(row=2, column=0, columnspan=5)

        self.draw_puzzle(self.solution_steps[self.current_step],self.last_changed_indexes[self.current_step])

    
    def draw_puzzle(self, puzzle,l_index):
        """Draw the current state of the puzzle on the canvas."""
        self.canvas.delete("all") 

        for i in range(9):
            for j in range(9):
                x0, y0 = j * self.size, i * self.size
                x1, y1 = x0 + self.size, y0 + self.size

                # for step 0 show the original puzzle
                if self.current_step == 0:
                    if self.original_puzzle[i][j] != 0:
                        color = "gold"  # original cells that are not empty
                        self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)
                        self.canvas.create_text(x0 + self.size / 2, y0 + self.size / 2,
                                                text=str(self.original_puzzle[i][j]), font=("Arial", 20))
                    else:
                        color = "light goldenrod"  # empty cells in the original puzzle
                        self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

                # for other steps show the current puzzle state
                else:
                    color = "gold" if self.original_puzzle[i][j] != 0 else "light goldenrod"
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

                    if puzzle[i][j] != 0:
                        text_color = "red" if l_index == [i,j] else "black"
                        self.canvas.create_text(x0 + self.size / 2, y0 + self.size / 2,
                                                text=str(puzzle[i][j]), font=("Arial", 20), fill=text_color)
        for i in range(1, 3):  # there are 3 grid lines for 9 rows/columns
        # horizontal lines
            self.canvas.create_line(0, i * 3 * self.size, 9 * self.size, i * 3 * self.size, fill="black", width=3)
        # vertical lines
            self.canvas.create_line(i * 3 * self.size, 0, i * 3 * self.size, 9 * self.size, fill="black", width=3)

    def show_prev_step(self):
        """Display the previous step."""
        if self.current_step > 0:
            self.current_step -= 1
            self.draw_puzzle(self.solution_steps[self.current_step],self.last_changed_indexes[self.current_step-1])
        else:
            messagebox.showinfo("Info", "You are at the first step.")

    def show_next_step(self):
        """Display the next step."""
        if self.current_step < len(self.solution_steps) - 1:
            self.current_step += 1
            self.draw_puzzle(self.solution_steps[self.current_step],self.last_changed_indexes[self.current_step-1])
        else:
            messagebox.showinfo("Info", "You are at the final step.")

    def jump_to_step(self):
        """Jump to a specific step entered by the user."""
        try:
            step = int(self.step_entry.get())
            if 0 <= step < len(self.solution_steps):
                self.current_step = step
                self.draw_puzzle(self.solution_steps[self.current_step],self.last_changed_indexes[self.current_step])
            else:
                messagebox.showerror("Error", "Step out of range.")
        except ValueError:
            messagebox.showerror("Error", "Invalid step number.")

    def show_final(self):
        """Display the final solution."""
        self.current_step = len(self.solution_steps) - 1
        self.draw_puzzle(self.solution_steps[self.current_step],self.last_changed_indexes[self.current_step-1])

def get_solution_steps(puzzle, solver_function,last_changed_indexes):
        """Run the solver and collect the steps of the solution."""
        steps = [[row[:] for row in puzzle]]  # start with the original puzzle
        # use a modified version of the solver that yields each step
        solver_function(puzzle, steps,last_changed_indexes)
        return steps

if __name__ == "__main__":
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    def sudoku(puzzle, steps,last_changed_indexes):
        subgrids = []
        #detect subgrids
        for j in range(0, 9, 3):
            for i in range(0, 9, 3):
                subgrids.append([puzzle[j][i:i+3], puzzle[j+1][i:i+3], puzzle[j+2][i:i+3]])

        d = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        may = []
        empty_cells_indx = []

        for i in range(9):
            for j in range(9):
                if puzzle[i][j] == 0:
                    empty_cells_indx.append([i, j])
                    may.append([1, 2, 3, 4, 5, 6, 7, 8, 9])

        columns = []
        for i in range(9):
            p = []
            for j in range(9):
                p.append(puzzle[j][i])
            columns.append(p)

        i, count = 0, 0

        while i != 9:
            j = 0
            while j != 9:
                success_flag = 1
                row_values = puzzle[i].copy()
                #code below finds in which subgrid is the element
                if 0 <= i <= 2:
                    k = j // 3
                elif 3 <= i <= 5:
                    k = 3 + j // 3
                else:
                    k = 6 + j // 3

                if puzzle[i][j] == 0:
                    ind = 0
                    while ((may[count][ind] in row_values) or 
                           (may[count][ind] in columns[j]) or 
                           (may[count][ind] in subgrids[k][0]) or 
                           (may[count][ind] in subgrids[k][1]) or 
                           (may[count][ind] in subgrids[k][2])):
                        ind += 1
                        if ind >= len(may[count]):
                            i, j = empty_cells_indx[count-1][0], empty_cells_indx[count-1][1]
                            may[count-1].remove(puzzle[i][j])
                            count -= 1
                            for o in range(count+1, len(may)):
                                may[o] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                            if 0 <= i <= 2:
                                h = j // 3
                            elif 3 <= i <= 5:
                                h = 3 + j // 3
                            else:
                                h = 6 + j // 3
                            for u in range(3):
                                if puzzle[i][j] in subgrids[h][u]:
                                    subgrids[h][u][subgrids[h][u].index(puzzle[i][j])] = 0
                            puzzle[i][j] = 0
                            columns[j][i] = 0
                            success_flag = 0
                            break
                    if success_flag:
                        for u in range(3):
                            if puzzle[i][j] in subgrids[k][u]:
                                subgrids[k][u][subgrids[k][u].index(puzzle[i][j])] = may[count][ind]
                        puzzle[i][j] = may[count][ind]
                        last_changed_indexes.append([i,j])
                        columns[j][i] = puzzle[i][j]
                        count += 1
                        steps.append([row[:] for row in puzzle])  # Save each step
                if success_flag:
                    j += 1
            if success_flag:
                i += 1

    root = tk.Tk()
    root.title("Sudoku Solver Visualization")
    last_changed_indexes=[]
    solution_steps = get_solution_steps(puzzle, sudoku,last_changed_indexes)
    app = SudokuVisualizer(root, solution_steps[0], solution_steps,last_changed_indexes)

    root.mainloop()
 
