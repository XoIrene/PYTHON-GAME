import tkinter as tk
from tkinter import messagebox
import random

class RiverCrossingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("River Crossing Puzzle - Farmer, Lion, Goat & maize")
        self.root.geometry("900x600")
        self.root.configure(bg="#87CEEB")
        
        # Game state
        self.left_side = {"man", "lion", "goat", "maize"}
        self.right_side = set()
        self.boat_on_left = True
        self.selected_item = None
        self.game_over = False
        
        # Create UI
        self.setup_ui()
        self.draw_game()
        
    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="River Crossing Puzzle",
            font=("Aerial", 40, "bold"),
            fg="#1A09AE",
            bg="#87CEEB"
        )
        title_label.pack(pady=10)
        
        # Instructions
        instructions = tk.Label(
            self.root,
            text="Move items to the boat with the man. Constraints:\n" 
                 "Lion cannot be alone with Goat\n" 
                 "Goat cannot be alone with maize",
            font=("Arial", 10),
            bg="#87CEEB",
            justify=tk.LEFT
        )
        instructions.pack(pady=5)
        
        # Canvas for game display
        self.canvas = tk.Canvas(
            self.root,
            width=850,
            height=350,
            bg="#E0F6FF",
            highlightthickness=2,
            highlightbackground="#000080"
        )
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        # Control panel
        control_frame = tk.Frame(self.root, bg="#87CEEB")
        control_frame.pack(pady=10)
        
        self.status_label = tk.Label(
            control_frame,
            text="Status: Ready to start",
            font=("Arial", 12),
            bg="#87CEEB",
            fg="#000080"
        )
        self.status_label.pack()
        
        button_frame = tk.Frame(control_frame, bg="#87CEEB")
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame,
            text="Reset Game",
            command=self.reset_game,
            font=("Arial", 10),
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Undo Move",
            command=self.undo_move,
            font=("Arial", 10),
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        # Move history for undo
        self.move_history = []
      
    def draw_game(self):
        self.canvas.delete("all")
        
        # Draw river
        self.canvas.create_rectangle(350, 50, 450, 300, fill="#4DA6FF", outline="#000080", width=3)
        self.canvas.create_text(400, 25, text="RIVER", font=("Arial", 12, "bold"), fill="#000080")
        
        # Draw left bank label
        self.canvas.create_text(100, 25, text="LEFT BANK", font=("Arial", 12, "bold"), fill="#000080")
        
        # Draw right bank label
        self.canvas.create_text(750, 25, text="RIGHT BANK", font=("Arial", 12, "bold"), fill="#000080")
        
        # Draw boat
        boat_y = 280 if self.boat_on_left else 280
        boat_x = 370 if self.boat_on_left else 430
        self.draw_boat(boat_x, boat_y)
        
        # Draw items on left side
        left_x_positions = [50, 120, 190, 260]
        for i, item in enumerate(sorted(self.left_side)):
            if item != "man":
                x = left_x_positions[min(i, len(left_x_positions) - 1)]
                self.draw_item(item, x, 200, self.left_side)
        
        # Draw man on left if on left
        if "man" in self.left_side:
            self.draw_item("man", 310, 150, self.left_side)
        
        # Draw items on right side
        right_x_positions = [650, 720, 790, 860]
        for i, item in enumerate(sorted(self.right_side)):
            if item != "man":
                x = right_x_positions[min(i, len(right_x_positions) - 1)]
                self.draw_item(item, x, 200, self.right_side)
        
        # Draw man on right if on right
        if "man" in self.right_side:
            self.draw_item("man", 590, 150, self.right_side)
        
        # Check win condition
        if len(self.right_side) == 4 and not self.game_over:
            self.game_over = True
            messagebox.showinfo("Congratulations!", "You successfully moved everyone across the river!")
            self.status_label.config(text="Status: YOU WIN! 🎉")
    
    def draw_boat(self, x, y):
        # Draw boat
        self.canvas.create_polygon(
            x-20, y, x+20, y, x+25, y+30, x-25, y+30,
            fill="#8B4513", outline="#000000", width=2
        )
        self.canvas.create_text(x, y+15, text="⛵",font=("Arial", 20))
    
    def draw_item(self, item, x, y, container):
        # Draw clickable item
        colors = {
            "man": "#FFD700",
            "lion": "#FF6347",
            "goat": "#98FB98",
            "maize": "#FFD700"
        }
        emojis = {
            "man": "👨",
            "lion": "🦁",
            "goat": "🐐",
            "maize": "🌽"
        }
        
        color = colors.get(item, "#CCCCCC")
        tag = f"item_{item}"
        
        # Draw rectangle
        self.canvas.create_rectangle(
            x-25, y-25, x+25, y+25,
            fill=color,
            outline="#000000",
            width=2,
            tags=tag
        )
        
        # Draw emoji and label
        self.canvas.create_text(x, y-5, text=emojis.get(item, "?"), font=("Arial", 20), tags=tag)
        self.canvas.create_text(x, y+15, text=item.capitalize(), font=("Arial", 9), tags=tag)
    
    def on_canvas_click(self, event):
        if self.game_over:
            return
        
        # Check which item was clicked
        clicked_items = self.canvas.find_overlapping(
            event.x - 5, event.y - 5, event.x + 5, event.y + 5
        )
        
        if not clicked_items:
            return
        
        for item_id in clicked_items:
            tags = self.canvas.gettags(item_id)
            for tag in tags:
                if tag.startswith("item_"):
                    item_name = tag.replace("item_", "")
                    self.try_move_item(item_name)
                    return
    
    def try_move_item(self, item):
        # Check if item is on the same side as the man
        if self.boat_on_left:
            if item not in self.left_side:
                self.status_label.config(text="Status: The man must be on the same side as the item!")
                return
        else:
            if item not in self.right_side:
                self.status_label.config(text="Status: The man must be on the same side as the item!")
                return
        
        # Save state for undo
        self.move_history.append({
            "left": self.left_side.copy(),
            "right": self.right_side.copy(),
            "boat_on_left": self.boat_on_left
        })
        
        # Move item (only if it's not the man) and move the man
        if self.boat_on_left:
            if item != "man":
                self.left_side.remove(item)
                self.right_side.add(item)
            self.left_side.remove("man")
            self.right_side.add("man")
        else:
            if item != "man":
                self.right_side.remove(item)
                self.left_side.add(item)
            self.right_side.remove("man")
            self.left_side.add("man")
        
        self.boat_on_left = not self.boat_on_left
        
        # Check for invalid states
        if not self.is_valid_state():
            messagebox.showerror("Invalid Move!", "You left the goat alone with the lion or maize!\nGame Over!")
            self.game_over = True
            self.status_label.config(text="Status: GAME OVER - Invalid state reached!")
            self.draw_game()
            return
        
        move_description = "himself" if item == "man" else item
        self.status_label.config(text=f"Status: Moved {move_description} across the river")
        self.draw_game()
    
    def is_valid_state(self):
        # Check left side
        if not ("man" in self.left_side):
            # Man not on left, check constraints
            if "goat" in self.left_side and "lion" in self.left_side:
                return False
            if "goat" in self.left_side and "maize" in self.left_side:
                return False
        
        # Check right side
        if not ("man" in self.right_side):
            # Man not on right, check constraints
            if "goat" in self.right_side and "lion" in self.right_side:
                return False
            if "goat" in self.right_side and "maize" in self.right_side:
                return False
        
        return True
    
    def reset_game(self):
        self.left_side = {"man", "lion", "goat", "maize"}
        self.right_side = set()
        self.boat_on_left = True
        self.selected_item = None
        self.game_over = False
        self.move_history = []
        self.status_label.config(text="Status: Game Reset!")
        self.draw_game()
    
    def undo_move(self):
        if not self.move_history:
            messagebox.showinfo("Undo", "No moves to undo!")
            return
        
        previous_state = self.move_history.pop()
        self.left_side = previous_state["left"]
        self.right_side = previous_state["right"]
        self.boat_on_left = previous_state["boat_on_left"]
        self.game_over = False
        self.status_label.config(text="Status: Move undone!")
        self.draw_game()


if __name__ == "__main__":
    root = tk.Tk()
    game = RiverCrossingGame(root)
    root.mainloop()