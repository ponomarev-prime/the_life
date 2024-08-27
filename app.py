from flask import Flask, render_template, jsonify, request
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

    def reset_counter(self):
        self.counter = 0

# Initialize a single instance of GameOfLife
game_instance = GameOfLife(25, 25)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/live')
def live():
    game_instance.form_new_generation()
    return render_template('live.html', world=game_instance.get_display_world(), counter=game_instance.counter)

@app.route('/update')
def update():
    game_instance.form_new_generation()
    return jsonify(world=game_instance.get_display_world(), counter=game_instance.counter)

@app.route('/reset_counter')
def reset_counter():
    game_instance.reset_counter()
    return jsonify(counter=game_instance.counter)

if __name__ == '__main__':
    app.run(debug=True)
