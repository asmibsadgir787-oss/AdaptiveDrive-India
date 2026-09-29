import heapq


class AStarPlanner:
    def __init__(self, environment, cost_function=None):
        self.environment = environment
        self.cost_function = cost_function

    def heuristic(self, current, goal):
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    def get_neighbors(self, position):
        x, y = position

        possible_moves = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1)
        ]

        valid_neighbors = []

        for nx, ny in possible_moves:

            if 0 <= nx < self.environment.width:
                if 0 <= ny < self.environment.height:

                    if not self.environment.is_obstacle(nx, ny):
                        valid_neighbors.append((nx, ny))

        return valid_neighbors

    def find_path(self, start, goal, traffic_objects=None):

        if traffic_objects is None:
            traffic_objects = []

        open_list = []

        heapq.heappush(
            open_list,
            (0, start)
        )

        came_from = {}
        cost_so_far = {
            start: 0
        }

        while open_list:

            _, current = heapq.heappop(open_list)

            if current == goal:
                return self.reconstruct_path(
                    came_from,
                    current
                )

            for neighbor in self.get_neighbors(current):

                movement_cost = 1

                if self.cost_function:

                    traffic_cost = self.cost_function.get_position_cost(
                        neighbor,
                        traffic_objects
                    )

                    movement_cost = traffic_cost

                new_cost = (
                    cost_so_far[current]
                    + movement_cost
                )

                if (
                    neighbor not in cost_so_far
                    or new_cost < cost_so_far[neighbor]
                ):

                    cost_so_far[neighbor] = new_cost

                    priority = (
                        new_cost
                        + self.heuristic(
                            neighbor,
                            goal
                        )
                    )

                    heapq.heappush(
                        open_list,
                        (priority, neighbor)
                    )

                    came_from[neighbor] = current

        return []

    def reconstruct_path(
        self,
        came_from,
        current
    ):
        path = [current]

        while current in came_from:

            current = came_from[current]

            path.append(current)

        path.reverse()

        return path