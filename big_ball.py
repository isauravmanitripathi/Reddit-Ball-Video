import pygame
from random import choice
from collections import deque

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
CELL_SIZE = 16  # Size of each cell in the maze
BALL_RADIUS = 8  # Radius of the ball

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Cell(pygame.sprite.Sprite):
    w, h = CELL_SIZE, CELL_SIZE

    def __init__(self, x, y, maze):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([self.w, self.h])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x * self.w
        self.rect.y = y * self.h
        self.x = x
        self.y = y
        self.maze = maze
        self.nbs = [(x + nx, y + ny) for nx, ny in ((-2, 0), (0, -2), (2, 0), (0, 2))
                    if 0 <= x + nx < maze.w and 0 <= y + ny < maze.h]

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Wall(Cell):
    def __init__(self, x, y, maze):
        super(Wall, self).__init__(x, y, maze)
        self.image.fill(BLACK)
        self.type = 0

class Maze:
    def __init__(self, size):
        self.w, self.h = size[0] // Cell.w, size[1] // Cell.h
        self.grid = [[Wall(x, y, self) for y in range(self.h)] for x in range(self.w)]

    def get(self, x, y):
        return self.grid[x][y]

    def place_wall(self, x, y):
        self.grid[x][y] = Wall(x, y, self)

    def draw(self, screen):
        for row in self.grid:
            for cell in row:
                cell.draw(screen)

    def generate(self, screen=None, animate=False):
        unvisited = [c for r in self.grid for c in r if c.x % 2 and c.y % 2]
        cur = unvisited.pop()
        stack = []

        while unvisited:
            try:
                n = choice([c for c in map(lambda x: self.get(*x), cur.nbs) if c in unvisited])
                stack.append(cur)
                nx, ny = cur.x - (cur.x - n.x) // 2, cur.y - (cur.y - n.y) // 2
                self.grid[nx][ny] = Cell(nx, ny, self)
                self.grid[cur.x][cur.y] = Cell(cur.x, cur.y, self)
                cur = n
                unvisited.remove(n)

                if animate:
                    self.draw(screen)
                    pygame.display.update()
                    pygame.time.wait(10)
            except IndexError:
                if stack:
                    cur = stack.pop()

    def solve(self, start, end):
        queue = deque([start])
        visited = {start}
        parent = {start: None}

        while queue:
            x, y = queue.popleft()
            if (x, y) == end:
                path = []
                while (x, y) is not None:
                    path.append((x, y))
                    x, y = parent[(x, y)]
                return path[::-1]

            for nx, ny in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                if 0 <= nx < self.w and 0 <= ny < self.h and (nx, ny) not in visited and isinstance(self.grid[nx][ny], Cell):
                    queue.append((nx, ny))
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)

        return []

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Generator and Solver")

    maze = Maze((SCREEN_WIDTH, SCREEN_HEIGHT))
    maze.generate(screen=screen, animate=True)

    start = (0, 0)
    end = (maze.w - 1, maze.h - 1)
    path = maze.solve(start, end)

    running = True
    ball_pos = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        maze.draw(screen)

        if ball_pos < len(path):
            x, y = path[ball_pos]
            pygame.draw.circle(screen, RED, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), BALL_RADIUS)
            ball_pos += 1

        pygame.display.flip()
        pygame.time.wait(100)  # Adjust the speed of the ball

    pygame.quit()

if __name__ == "__main__":
    main()
