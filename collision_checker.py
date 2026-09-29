class CollisionChecker:
    def __init__(self, safety_distance=1.0):
        self.safety_distance = safety_distance

    def distance(self, point1, point2):
        return (
            (point1[0] - point2[0]) ** 2
            + (point1[1] - point2[1]) ** 2
        ) ** 0.5

    def is_collision(self, vehicle_position, obstacle_position):
        distance = self.distance(
            vehicle_position,
            obstacle_position
        )

        return distance <= self.safety_distance

    def is_path_safe(self, path, obstacles):
        for position in path:
            for obstacle in obstacles:
                if self.is_collision(position, obstacle):
                    return False

        return True