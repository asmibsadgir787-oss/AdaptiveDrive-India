class Environment:
    def __init__(self, width=24, height=16):
        self.width = width
        self.height = height
        self.obstacles = []

    def add_obstacle(self, x, y):
        self.obstacles.append((x, y))

    def is_obstacle(self, x, y):
        return (x, y) in self.obstacles

    def get_obstacles(self):
        return self.obstacles