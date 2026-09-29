class RiskEngine:
    """
    Time-aware risk engine for dynamic traffic.

    Evaluates:
    - Current distance
    - Predicted traffic movement
    - Time-synchronized trajectory conflict
    - Warning and danger zones
    """

    def __init__(
        self,
        warning_distance=3.0,
        danger_distance=1.5
    ):
        self.warning_distance = warning_distance
        self.danger_distance = danger_distance

    # -------------------------------------------------
    # DISTANCE
    # -------------------------------------------------

    def calculate_distance(self, point1, point2):

        return (
            (point1[0] - point2[0]) ** 2
            +
            (point1[1] - point2[1]) ** 2
        ) ** 0.5

    # -------------------------------------------------
    # POSITION RISK
    # -------------------------------------------------

    def assess_position_risk(
        self,
        vehicle_position,
        traffic_position
    ):

        distance = self.calculate_distance(
            vehicle_position,
            traffic_position
        )

        if distance <= self.danger_distance:
            return "DANGER"

        elif distance <= self.warning_distance:
            return "WARNING"

        return "SAFE"

    # -------------------------------------------------
    # PREDICT TRAFFIC
    # -------------------------------------------------

    def predict_traffic_positions(
        self,
        traffic_object,
        prediction_horizon=5
    ):

        predictions = []

        for step in range(
            1,
            prediction_horizon + 1
        ):

            position = traffic_object.predict_position(
                step
            )

            predictions.append(
                {
                    "time_step": step,
                    "position": position
                }
            )

        return predictions

    # -------------------------------------------------
    # TIME SYNCHRONIZED CONFLICT
    # -------------------------------------------------

    def check_trajectory_conflict(
        self,
        path,
        traffic_object,
        prediction_horizon=5
    ):

        if not path:
            return "DANGER"

        predictions = self.predict_traffic_positions(
            traffic_object,
            prediction_horizon
        )

        highest_risk = "SAFE"

        # Vehicle reaches each path point
        # approximately one simulation step apart.
        for vehicle_time, vehicle_position in enumerate(
            path[:prediction_horizon],
            start=1
        ):

            for prediction in predictions:

                traffic_time = prediction["time_step"]

                # Only compare positions occurring
                # at approximately the same time.
                if traffic_time != vehicle_time:
                    continue

                traffic_position = prediction["position"]

                risk = self.assess_position_risk(
                    vehicle_position,
                    traffic_position
                )

                if risk == "DANGER":
                    return "DANGER"

                if risk == "WARNING":
                    highest_risk = "WARNING"

        return highest_risk

    # -------------------------------------------------
    # PATH RISK
    # -------------------------------------------------

    def assess_path_risk(
        self,
        path,
        traffic_object
    ):

        if not path:
            return "DANGER"

        # ---------------------------------------------
        # 1. Current position check
        # ---------------------------------------------

        current_vehicle_position = path[0]

        current_traffic_position = (
            traffic_object.get_position()
        )

        current_risk = self.assess_position_risk(
            current_vehicle_position,
            current_traffic_position
        )

        if current_risk == "DANGER":
            return "DANGER"

        # ---------------------------------------------
        # 2. Time-synchronized prediction
        # ---------------------------------------------

        trajectory_risk = self.check_trajectory_conflict(
            path,
            traffic_object,
            prediction_horizon=min(
                5,
                len(path)
            )
        )

        if trajectory_risk == "DANGER":
            return "DANGER"

        if (
            current_risk == "WARNING"
            or trajectory_risk == "WARNING"
        ):
            return "WARNING"

        # ---------------------------------------------
        # 3. Longer-horizon proximity warning
        # ---------------------------------------------

        for step in range(1, 6):

            predicted_position = (
                traffic_object.predict_position(step)
            )

            for vehicle_position in path:

                distance = self.calculate_distance(
                    vehicle_position,
                    predicted_position
                )

                if distance <= self.danger_distance:

                    return "DANGER"

                if distance <= self.warning_distance:

                    return "WARNING"

        return "SAFE"

    # -------------------------------------------------
    # COMPLETE TRAFFIC ASSESSMENT
    # -------------------------------------------------

    def assess_traffic(
        self,
        path,
        traffic_objects
    ):

        overall_risk = "SAFE"

        traffic_results = []

        for traffic in traffic_objects:

            risk = self.assess_path_risk(
                path,
                traffic
            )

            traffic_results.append(
                {
                    "id": traffic.object_id,
                    "risk": risk,
                    "current_position":
                        traffic.get_position(),
                    "predicted_positions":
                        [
                            item["position"]
                            for item in
                            self.predict_traffic_positions(
                                traffic
                            )
                        ]
                }
            )

            if risk == "DANGER":
                overall_risk = "DANGER"

            elif (
                risk == "WARNING"
                and overall_risk != "DANGER"
            ):
                overall_risk = "WARNING"

        return {
            "overall_risk": overall_risk,
            "traffic": traffic_results
        }