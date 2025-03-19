import tkinter as tk
import random


class Agent:
    def __init__(self, canvas, x, y, number, color="blue", font_color="white"):
        self.canvas = canvas
        self.x, self.y = x, y
        self.number = number
        self.color = color
        self.font_color = font_color
        self.radius = 10  # Radius of the agent circle
        self.create_agent()

    def create_agent(self):
        self.oval = self.canvas.create_oval(
            self.x - self.radius, self.y - self.radius,
            self.x + self.radius, self.y + self.radius,
            fill=self.color, outline="black"
        )
        self.text = self.canvas.create_text(
            self.x, self.y, text=str(self.number),
            fill=self.font_color, font=("Arial", 10, "bold")
        )

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.canvas.move(self.oval, dx, dy)
        self.canvas.move(self.text, dx, dy)


class Simulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulation GUI")
        self.root.geometry("1600x1000")  # Set initial window size

        self.frame = tk.Frame(root)
        self.frame.pack(side=tk.LEFT, fill=tk.Y)

        self.labels = {}
        label_texts = ["clean dish", "dirty dish", "free seat", "current time", "served guest"]
        for text in label_texts:
            self.labels[text] = tk.Label(self.frame, text=f"{text}: 0", font=("Arial", 12))
            self.labels[text].pack()

        self.start_button = tk.Button(self.frame, text="Start", command=self.toggle_simulation)
        self.start_button.pack()

        self.canvas = tk.Canvas(root, bg="white", width=1500, height=1000)
        self.canvas.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self.grid_width = 3000
        self.grid_height = 1000
        self.active_simulation = False
        self.draw_grid()

        self.agents = [Agent(self.canvas, random.randint(50, 500), random.randint(50, 500), random.randint(1, 999)) for
                       _ in range(5)]

        self.root.bind("<Up>", lambda e: self.move_agents(0, -10))
        self.root.bind("<Down>", lambda e: self.move_agents(0, 10))
        self.root.bind("<Left>", lambda e: self.move_agents(-10, 0))
        self.root.bind("<Right>", lambda e: self.move_agents(10, 0))
        self.root.bind("<space>", lambda e: self.step_agents() if not self.active_simulation else None)

    def toggle_simulation(self):
        self.active_simulation = not self.active_simulation
        self.start_button.config(text="Stop" if self.active_simulation else "Start")
        if self.active_simulation:
            self.run_simulation()

    def run_simulation(self):
        if self.active_simulation:
            self.step_agents()
            self.root.after(1000, self.run_simulation)

    def step_agents(self):
        occupied_positions = {(agent.x, agent.y) for agent in self.agents}
        for agent in self.agents:
            possible_moves = [(agent.x + dx, agent.y + dy) for dx, dy in [(-10, -10), (0, -10), (10, -10),
                                                                          (-10, 0), (10, 0),
                                                                          (-10, 10), (0, 10), (10, 10)]]
            valid_moves = [(x, y) for x, y in possible_moves if
                           (x, y) not in occupied_positions and 0 <= x <= 1500 and 0 <= y <= 1000]
            if valid_moves:
                new_x, new_y = random.choice(valid_moves)
                agent.move(new_x - agent.x, new_y - agent.y)
                occupied_positions.add((new_x, new_y))

    def draw_grid(self):
        self.canvas.delete("grid_line")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        scale_x = width / self.grid_width
        scale_y = height / self.grid_height
        spacing_x = width // 30  # Approximate scale
        spacing_y = height // 10
        for i in range(0, width, 10):
            self.canvas.create_line(i, 0, i, height, fill="lightgray", tags="grid_line")
        for j in range(0, height, 10):
            self.canvas.create_line(0, j, width, j, fill="lightgray", tags="grid_line")
        self.root.after(500, self.draw_grid)  # Redraw grid periodically to adjust scaling

    def move_agents(self, dx, dy):
        for agent in self.agents:
            agent.move(dx, dy)

    def update_label(self, label, value):
        if label in self.labels:
            self.labels[label].config(text=f"{label}: {value}")


if __name__ == "__main__":
    root = tk.Tk()
    sim = Simulation(root)
    root.mainloop()
