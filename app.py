# app.py
from flask import Flask, render_template
import random

app = Flask(__name__)

class GameOfLife:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.world = [[random.randint(0, 1) for _ in range(width)] for _ in range(height)]

    def _get_near(self, x, y):
        # Calculate the number of living neighbors
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
        self.world = new_world

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/live')
def live():
    game = GameOfLife(25, 25)
    game.form_new_generation()
    return render_template('live.html', world=game.world)

if __name__ == '__main__':
    app.run(debug=True)
