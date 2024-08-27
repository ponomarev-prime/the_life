from flask import Flask, render_template, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Нужно для использования сессий

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
        print(f"Before generation: Counter = {self.counter}")  # Debugging line
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
        print(f"After generation: Counter = {self.counter}")  # Debugging line

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

# Глобальная переменная для хранения состояния игры
game_of_life = GameOfLife(25, 25)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/live')
def live():
    global game_of_life
    game_of_life.form_new_generation()
    return render_template('live.html', world=game_of_life.get_display_world(), counter=game_of_life.counter)

@app.route('/reset_counter')
def reset_counter():
    global game_of_life
    game_of_life.counter = 0
    return redirect(url_for('live'))

if __name__ == '__main__':
    app.run(debug=True)
