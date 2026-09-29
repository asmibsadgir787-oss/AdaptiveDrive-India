import time


class Simulator:

    def __init__(
        self,
        vehicle,
        environment,
        planner,
        replanner,
        traffic_objects
    ):
        self.vehicle = vehicle
        self.environment = environment
        self.planner = planner
        self.replanner = replanner
        self.traffic_objects = traffic_objects

        self.current_path = []
        self.previous_path = []

        self.step_count = 0
        self.decision = "START"

        self.last_risk = "SAFE"
        self.candidate_count = 0
        self.planning_latency_ms = 0.0

        # Metrics
        self.replan_count = 0
        self.wait_count = 0
        self.stop_count = 0
        self.continue_count = 0
        self.collision_count = 0
        self.total_planning_latency_ms = 0.0

    def update_traffic(self):
        for traffic in self.traffic_objects:
            traffic.move()

    def calculate_path(self):

        old_path = self.current_path

        start_time = time.perf_counter()

        result = self.replanner.find_safe_path(
            self.vehicle.get_position(),
            self.vehicle.get_destination(),
            self.traffic_objects
        )

        end_time = time.perf_counter()

        self.planning_latency_ms = round(
            (end_time - start_time) * 1000,
            3
        )

        self.total_planning_latency_ms += (
            self.planning_latency_ms
        )

        new_path = result.get(
            "path",
            []
        )

        self.last_risk = result.get(
            "risk",
            "SAFE"
        )

        self.candidate_count = result.get(
            "candidate_count",
            0
        )

        self.previous_path = old_path

        self.current_path = new_path

        # Use the actual decision returned by the replanner.
        self.decision = result.get(
            "decision",
            "STOP"
        )

        # Count decisions.

        if self.decision == "WAIT":

            self.wait_count += 1

        elif self.decision == "STOP":

            self.stop_count += 1

        elif self.decision == "CONTINUE":

            self.continue_count += 1

        elif self.decision == "REPLAN":

            self.replan_count += 1


    def check_collision(self):

        vehicle_position = self.vehicle.get_position()

        for traffic in self.traffic_objects:

            if vehicle_position == traffic.get_position():
                self.collision_count += 1
                return True

        return False

    def move_vehicle(self):

        if not self.current_path:
            return

        current_position = self.vehicle.get_position()

        if current_position == self.vehicle.get_destination():
            return

        try:

            current_index = self.current_path.index(
                current_position
            )

            next_position = self.current_path[
                current_index + 1
            ]

            self.vehicle.move_to(
                next_position[0],
                next_position[1]
            )

        except (ValueError, IndexError):
            return

    def get_predicted_traffic(self):

        predicted = []

        for traffic in self.traffic_objects:

            predictions = []

            for step in range(1, 6):

                predictions.append(
                    {
                        "time_step": step,
                        "position":
                            traffic.predict_position(step)
                    }
                )

            predicted.append(
                {
                    "id": traffic.object_id,
                    "predictions": predictions
                }
            )

        return predicted

    def get_metrics(self):

        if self.step_count > 0:

            average_latency = round(
                self.total_planning_latency_ms
                / self.step_count,
                3
            )

        else:

            average_latency = 0.0

        return {
            "steps": self.step_count,
            "replan_count": self.replan_count,
            "wait_count": self.wait_count,
            "stop_count": self.stop_count,
            "continue_count": self.continue_count,
            "collision_count": self.collision_count,
            "average_planning_latency_ms":
                average_latency
        }

    def run_step(self):

        self.step_count += 1

        self.update_traffic()

        self.calculate_path()

        if self.decision in [
            "CONTINUE",
            "REPLAN"
        ]:
            self.move_vehicle()

        collision_detected = self.check_collision()

        return {
            "step":
                self.step_count,

            "vehicle_position":
                self.vehicle.get_position(),

            "destination":
                self.vehicle.get_destination(),

            "decision":
                self.decision,

            "risk":
                self.last_risk,

            "candidate_count":
                self.candidate_count,

            "planning_latency_ms":
                self.planning_latency_ms,

            "path":
                self.current_path,

            "predicted_traffic":
                self.get_predicted_traffic(),

            "traffic":
                [
                    {
                        "id":
                            traffic.object_id,

                        "position":
                            traffic.get_position(),

                        "direction":
                            traffic.direction
                    }
                    for traffic in self.traffic_objects
                ],

            "obstacle_count":
                len(
                    self.environment.get_obstacles()
                ),

            "collision_detected":
                collision_detected,

            "metrics":
                self.get_metrics()
        }

    def is_finished(self):

        return (
            self.vehicle.get_position()
            ==
            self.vehicle.get_destination()
        )