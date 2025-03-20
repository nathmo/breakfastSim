import tkinter as tk
import time
import random
import math
from threading import Thread


class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Breakfast Simulation")
        self.canvas = tk.Canvas(self.root, width=1000, height=500, bg="white")
        self.canvas.pack()
        self.labels = {}
        self.create_labels()
        self.draw_grid()
        self.root.bind("<space>", self.on_spacebar)

    def create_labels(self):
        label_names = ["simulation time", "clean dish", "dirty dish", "free seat", "served guest"]
        self.label_frame = tk.Frame(self.root)
        self.label_frame.pack(side="bottom", fill="x")

        for name in label_names:
            tk.Label(self.label_frame, text=name).pack(side="left", padx=10)
            self.labels[name] = tk.Label(self.label_frame, text="0")
            self.labels[name].pack(side="left", padx=10)

    def draw_grid(self):
        for x in range(0, 1500, 10):
            self.canvas.create_line(x, 0, x, 1000, fill="lightgray")
        for y in range(0, 1000, 10):
            self.canvas.create_line(0, y, 1500, y, fill="lightgray")

    def draw_circle(self, x, y, diameter, color="white", number=0):
        r = diameter // 2
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="black")
        self.canvas.create_text(x, y, text=str(number), fill="black")

    def draw_square(self, x, y, side, color="white", number=0):
        half = side // 2
        self.canvas.create_rectangle(x - half, y - half, x + half, y + half, fill=color, outline="black")
        self.canvas.create_text(x, y, text=str(number), fill="black")

    def draw_line(self, x1, y1, x2, y2, width=2, color="black"):
        self.canvas.create_line(x1, y1, x2, y2, width=width, fill=color)

    def update_label(self, name, value):
        if name in self.labels:
            self.labels[name].config(text=str(value))

    def on_spacebar(self, event):
        simulation.step()


class Agent:
    def __init__(self, x, y, shape, color, agent_id):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
        self.agent_id = agent_id
        self.state = None

    def step(self):
        pass


class Customer(Agent):
    def __init__(self, x, y, agent_id):
        super().__init__(x, y, "circle", "red", agent_id)

    def step(self):
        pass  # To be implemented


class Worker(Agent):
    def __init__(self, x, y, agent_id):
        super().__init__(x, y, "square", "blue", agent_id)

    def step(self):
        pass  # To be implemented


class Dish:
    def __init__(self, x, y, state="clean"):
        self.x = x
        self.y = y
        self.state = state

    def move(self, x, y):
        self.x = x
        self.y = y


class Simulation:
    def __init__(self):
        self.simulation_running = False
        self.time_counter = 360  # Starts at 6:00 AM
        self.dishes = []
        self.customers = []
        self.last_time = time.time()

    def toggle_simulation(self):
        self.simulation_running = not self.simulation_running
        if self.simulation_running:
            Thread(target=self.run, daemon=True).start()

    def run(self):
        while self.simulation_running:
            current_time = time.time()
            if current_time - self.last_time >= 1:
                self.last_time = current_time
                self.step()

    def step(self):
        self.time_counter += 1
        hh, mm = divmod(self.time_counter, 60)
        if hh >= 11 and mm >= 30:
            self.simulation_running = False
            return
        window.update_label("simulation time", f"{hh:02d}:{mm:02d}")
        if self.time_counter == 360:  # 6:00 AM
            self.dishes = [Dish(20, 20, "clean") for _ in range(40)]
        if 390 <= self.time_counter <= 600:  # 6:30 AM to 10:00 AM
            if random.random() < 0.5:  # Gaussian-like probability
                self.customers.append(Customer(random.randint(50, 1450), random.randint(50, 950), len(self.customers)))
            for customer in self.customers:
                customer.step()
            clean_count = sum(1 for dish in self.dishes if dish.state == "clean")
            dirty_count = len(self.dishes) - clean_count
            window.update_label("clean dish", clean_count)
            window.update_label("dirty dish", dirty_count)


if __name__ == "__main__":
    window = Window()
    simulation = Simulation()
    simulation.toggle_simulation()
    window.root.mainloop()