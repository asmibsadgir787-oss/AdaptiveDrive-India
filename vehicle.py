from dataclasses import dataclass


@dataclass
class Vehicle:
    x: int
    y: int
    speed: float
    direction: str
    destination_x: int
    destination_y: int
    safety_radius: float = 1.0

    def get_position(self):
        return (self.x, self.y)

    def get_destination(self):
        return (self.destination_x, self.destination_y)

    def move_to(self, x: int, y: int):
        self.x = x
        self.y = y