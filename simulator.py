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

        # -----------------------------------------------------
        # SIMULATION STATE
        # -----------------------------------------------------

        self.step_count = 0

        self.current_path = []
        self.previous_path = []

        self.decision = "READY"
        self.last_risk = "SAFE"

        self.candidate_count = 0

        # -----------------------------------------------------
        # PERFORMANCE
        # -----------------------------------------------------

        self.planning_latency_ms = 0
        self.total_planning_latency_ms = 0

        # -----------------------------------------------------
        # DECISION COUNTERS
        # -----------------------------------------------------

        self.replan_count = 0
        self.wait_count = 0
        self.stop_count = 0
        self.continue_count = 0

        # -----------------------------------------------------
        # SAFETY
        # -----------------------------------------------------

        self.collision_count = 0

    # =========================================================
    # UPDATE TRAFFIC
    # =========================================================

    def update_traffic(self):

        for traffic in self.traffic_objects:

            traffic.move()

    # =========================================================
    # CHECK CURRENT PATH RISK
    # =========================================================

    def check_current_path_risk(self):

        if not self.current_path:

            return "DANGER"

        return self.replanner.calculate_path_risk(
            self.current_path,
            self.traffic_objects
        )

    # =========================================================
    # CALCULATE PATH
    # =========================================================

    def calculate_path(self):

        start_time = time.perf_counter()

        # -----------------------------------------------------
        # FIRST STEP
        #
        # There is no existing path, so calculate one.
        # -----------------------------------------------------

        if not self.current_path:

            result = self.replanner.find_safe_path(
                self.vehicle.get_position(),
                self.vehicle.get_destination(),
                self.traffic_objects
            )

            new_path = result.get(
                "path",
                []
            )

            self.previous_path = []

            self.current_path = new_path

            self.last_risk = result.get(
                "risk",
                "SAFE"
            )

            self.candidate_count = result.get(
                "candidate_count",
                0
            )

            self.decision = result.get(
                "decision",
                "STOP"
            )

        # -----------------------------------------------------
        # EXISTING PATH
        #
        # Check whether the vehicle can safely continue on
        # its current route.
        # -----------------------------------------------------

        else:

            current_path_risk = (
                self.check_current_path_risk()
            )

            # -------------------------------------------------
            # CURRENT PATH IS SAFE
            #
            # Do NOT unnecessarily replan.
            # -------------------------------------------------

            if current_path_risk == "SAFE":

                self.last_risk = "SAFE"

                self.decision = "CONTINUE"

                self.candidate_count = 1

            # -------------------------------------------------
            # CURRENT PATH HAS WARNING / DANGER
            #
            # Now ask the replanner to find a better option.
            # -------------------------------------------------

            else:

                result = self.replanner.find_safe_path(
                    self.vehicle.get_position(),
                    self.vehicle.get_destination(),
                    self.traffic_objects
                )

                new_path = result.get(
                    "path",
                    []
                )

                self.previous_path = (
                    self.current_path
                )

                self.current_path = new_path

                self.last_risk = result.get(
                    "risk",
                    "DANGER"
                )

                self.candidate_count = result.get(
                    "candidate_count",
                    0
                )

                self.decision = result.get(
                    "decision",
                    "STOP"
                )

        # -----------------------------------------------------
        # PLANNING LATENCY
        # -----------------------------------------------------

        end_time = time.perf_counter()

        self.planning_latency_ms = round(
            (
                end_time
                - start_time
            ) * 1000,
            3
        )

        self.total_planning_latency_ms += (
            self.planning_latency_ms
        )

        # -----------------------------------------------------
        # COUNT DECISIONS
        # -----------------------------------------------------

        if self.decision == "WAIT":

            self.wait_count += 1

        elif self.decision == "STOP":

            self.stop_count += 1

        elif self.decision == "CONTINUE":

            self.continue_count += 1

        elif self.decision == "REPLAN":

            self.replan_count += 1

    # =========================================================
    # MOVE VEHICLE
    # =========================================================

    def move_vehicle(self):

        if not self.current_path:

            return

        current_position = (
            self.vehicle.get_position()
        )

        next_position = None

        # Find the next point after current position
        for position in self.current_path:

            if position == current_position:

                continue

            next_position = position

            break

        if next_position is None:

            return

        x, y = next_position

        self.vehicle.move_to(
            x,
            y
        )

    # =========================================================
    # COLLISION CHECK
    # =========================================================

    def check_collision(self):

        vehicle_position = (
            self.vehicle.get_position()
        )

        # -----------------------------------------------------
        # Dynamic traffic collision
        # -----------------------------------------------------

        for traffic in self.traffic_objects:

            if (
                traffic.get_position()
                == vehicle_position
            ):

                self.collision_count += 1

                return True

        # -----------------------------------------------------
        # Static obstacle collision
        # -----------------------------------------------------

        if (
            vehicle_position
            in self.environment.get_obstacles()
        ):

            self.collision_count += 1

            return True

        return False

    # =========================================================
    # PREDICT TRAFFIC
    # =========================================================

    def get_predicted_traffic(self):

        predicted = []

        for traffic in self.traffic_objects:

            predictions = []

            for step in range(1, 6):

                predictions.append(
                    {
                        "time_step": step,

                        "position":
                            traffic.predict_position(
                                step
                            )
                    }
                )

            predicted.append(
                {
                    "id":
                        traffic.object_id,

                    "predictions":
                        predictions
                }
            )

        return predicted

    # =========================================================
    # METRICS
    # =========================================================

    def get_metrics(self):

        if self.step_count > 0:

            average_latency = (
                self.total_planning_latency_ms
                /
                self.step_count
            )

        else:

            average_latency = 0

        return {

            "steps":
                self.step_count,

            "replan_count":
                self.replan_count,

            "wait_count":
                self.wait_count,

            "stop_count":
                self.stop_count,

            "continue_count":
                self.continue_count,

            "collision_count":
                self.collision_count,

            "average_planning_latency_ms":
                round(
                    average_latency,
                    3
                )
        }

    # =========================================================
    # DESTINATION CHECK
    # =========================================================

    def is_finished(self):

        return (
            self.vehicle.get_position()
            ==
            self.vehicle.get_destination()
        )

    # =========================================================
    # RUN ONE SIMULATION STEP
    # =========================================================

    def run_step(self):

        # -----------------------------------------------------
        # STEP
        # -----------------------------------------------------

        self.step_count += 1

        # -----------------------------------------------------
        # UPDATE TRAFFIC
        # -----------------------------------------------------

        self.update_traffic()

        # -----------------------------------------------------
        # PLAN / CHECK CURRENT PATH
        # -----------------------------------------------------

        self.calculate_path()

        # -----------------------------------------------------
        # VEHICLE MOVEMENT
        # -----------------------------------------------------

        if self.decision in [
            "CONTINUE",
            "REPLAN"
        ]:

            self.move_vehicle()

        # -----------------------------------------------------
        # COLLISION CHECK
        # -----------------------------------------------------

        collision_detected = (
            self.check_collision()
        )

        # -----------------------------------------------------
        # RETURN SIMULATION DATA
        # -----------------------------------------------------

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

                    for traffic
                    in self.traffic_objects
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