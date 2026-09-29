class TrafficCostFunction:
    def __init__(
        self,
        safe_cost=1,
        warning_cost=5,
        danger_cost=100
    ):
        self.safe_cost = safe_cost
        self.warning_cost = warning_cost
        self.danger_cost = danger_cost

    def calculate_distance(self, point1, point2):
        return (
            (point1[0] - point2[0]) ** 2
            + (point1[1] - point2[1]) ** 2
        ) ** 0.5

    def get_position_cost(
        self,
        position,
        traffic_objects
    ):
        total_cost = self.safe_cost

        for traffic in traffic_objects:

            distance = self.calculate_distance(
                position,
                traffic.get_position()
            )

            if distance <= 1.5:
                total_cost += self.danger_cost

            elif distance <= 3.0:
                total_cost += self.warning_cost

        return total_cost