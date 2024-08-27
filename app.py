# app.py
from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

class GameOfLife:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.world = [[random.randint(0, 1) for _ in range(width)] for _ in range(height)]
        self.prev_world = [[0] * width for _ in range(height)]  # Track previous generation
        self.counter = 0  # Initialize generation counter

    def _get_near(self, x, y):
        neighbors = [(i, j) for i in range(x-1, x+2) for j in range(y-1, y+2) if (i, j) != (x, y)]
        count = 0
        for i, j in neighbors:
            if 0 <= i < self.width and 0 <= j < self.height and self.world[i][j] == 1:
                count += 1
        return count

    def form_new_generation(self):
        new_world = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for x in range(self.width):
            for y in range(self.height):
                neighbors = self._get_near(x, y)
                if self.world[x][y] == 1 and neighbors in [2, 3]:
                    new_world[x][y] = 1
                elif self.world[x][y] == 0 and neighbors == 3:
                    new_world[x][y] = 1

        self.prev_world = [[cell for cell in row] for row in self.world]
        self.world = new_world
        self.counter += 1  # Increment generation counter

    def get_display_world(self):
        display_world = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for x in range(self.width):
            for y in range(self.height):
                if self.world[x][y] == 1:
                    display_world[x][y] = 1
                elif self.prev_world[x][y] == 1:
                    display_world[x][y] = 2
                else:
                    display_world[x][y] = 0
        return display_world

# Initialize a global instance
game = GameOfLife(25, 25)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/live')
def live():
    return render_template('live.html', world=game.get_display_world(), counter=game.counter)

@app.route('/update')
def update():
    game.form_new_generation()
    return jsonify(world=game.get_display_world(), counter=game.counter)

@app.route('/reset_counter')
def reset_counter():
    global game
    game = GameOfLife(25, 25)  # Reinitialize the game
    return jsonify(counter=game.counter)

if __name__ == '__main__':
    app.run(debug=True)
