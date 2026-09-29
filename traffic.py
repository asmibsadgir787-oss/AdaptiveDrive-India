class TrafficObject:
    def __init__(self, object_id, x, y, speed, direction):
        self.object_id = object_id
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction

    def get_position(self):
        return (self.x, self.y)

    def move(self):
        if self.direction == "north":
            self.y -= 1
        elif self.direction == "south":
            self.y += 1
        elif self.direction == "east":
            self.x += 1
        elif self.direction == "west":
            self.x -= 1

    def predict_position(self, steps=1):
        predicted_x = self.x
        predicted_y = self.y

        if self.direction == "north":
            predicted_y -= steps
        elif self.direction == "south":
            predicted_y += steps
        elif self.direction == "east":
            predicted_x += steps
        elif self.direction == "west":
            predicted_x -= steps

        return (predicted_x, predicted_y)