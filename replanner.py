class Replanner:
    """
    Traffic-aware adaptive replanner.

    Generates candidate paths, evaluates traffic risk,
    predicts future traffic movement and selects:

    CONTINUE
    REPLAN
    WAIT
    STOP
    """

    def __init__(self, planner, risk_engine):

        self.planner = planner
        self.risk_engine = risk_engine

    # ---------------------------------------------------------
    # PATH LENGTH
    # ---------------------------------------------------------

    def path_length(self, path):

        if not path:
            return float("inf")

        return len(path)

    # ---------------------------------------------------------
    # PATH RISK
    # ---------------------------------------------------------

    def calculate_path_risk(
        self,
        path,
        traffic_objects
    ):

        if not path:
            return "DANGER"

        highest_risk = "SAFE"

        for traffic in traffic_objects:

            risk = self.risk_engine.assess_path_risk(
                path,
                traffic
            )

            if risk == "DANGER":
                return "DANGER"

            if risk == "WARNING":
                highest_risk = "WARNING"

        return highest_risk

    # ---------------------------------------------------------
    # CURRENT TRAFFIC COST
    # ---------------------------------------------------------

    def traffic_cost(
        self,
        path,
        traffic_objects
    ):

        total_cost = 0

        for position in path:

            for traffic in traffic_objects:

                traffic_position = (
                    traffic.get_position()
                )

                distance = (
                    (
                        position[0]
                        - traffic_position[0]
                    ) ** 2
                    +
                    (
                        position[1]
                        - traffic_position[1]
                    ) ** 2
                ) ** 0.5

                if distance <= 1.5:

                    total_cost += 100

                elif distance <= 3:

                    total_cost += 20

                elif distance <= 5:

                    total_cost += 5

        return total_cost

    # ---------------------------------------------------------
    # PREDICTED TRAFFIC COST
    # ---------------------------------------------------------

    def predicted_traffic_cost(
        self,
        path,
        traffic_objects
    ):

        total_cost = 0

        for traffic in traffic_objects:

            for future_step in range(1, 6):

                predicted_position = (
                    traffic.predict_position(
                        future_step
                    )
                )

                for path_index, position in enumerate(path):

                    distance = (
                        (
                            position[0]
                            - predicted_position[0]
                        ) ** 2
                        +
                        (
                            position[1]
                            - predicted_position[1]
                        ) ** 2
                    ) ** 0.5

                    if distance <= 1.5:

                        time_penalty = max(
                            1,
                            20 - path_index
                        )

                        total_cost += (
                            50
                            +
                            time_penalty
                        )

                    elif distance <= 3:

                        total_cost += 8

        return total_cost

    # ---------------------------------------------------------
    # SCORE PATH
    # ---------------------------------------------------------

    def score_path(
        self,
        path,
        traffic_objects
    ):

        if not path:

            return float("inf")

        length_cost = (
            self.path_length(path)
        )

        traffic_cost = (
            self.traffic_cost(
                path,
                traffic_objects
            )
        )

        prediction_cost = (
            self.predicted_traffic_cost(
                path,
                traffic_objects
            )
        )

        risk = (
            self.calculate_path_risk(
                path,
                traffic_objects
            )
        )

        if risk == "DANGER":

            risk_cost = 1000

        elif risk == "WARNING":

            risk_cost = 100

        else:

            risk_cost = 0

        return (
            length_cost
            +
            traffic_cost
            +
            prediction_cost
            +
            risk_cost
        )

    # ---------------------------------------------------------
    # GENERATE CANDIDATE PATHS
    # ---------------------------------------------------------

    def generate_candidate_paths(
        self,
        start,
        goal,
        traffic_objects
    ):

        candidates = []

        # Normal path
        normal_path = self.planner.find_path(
            start,
            goal,
            traffic_objects
        )

        if normal_path:

            candidates.append(
                normal_path
            )

        # Save original obstacles
        original_obstacles = list(
            self.planner.environment.obstacles
        )

        predicted_positions = []

        for traffic in traffic_objects:

            predicted_positions.append(
                traffic.get_position()
            )

            predicted_positions.append(
                traffic.predict_position(2)
            )

            predicted_positions.append(
                traffic.predict_position(4)
            )

        # Generate alternatives
        for blocked_position in predicted_positions:

            self.planner.environment.obstacles = (
                list(original_obstacles)
            )

            if (
                blocked_position
                not in self.planner.environment.obstacles
            ):

                self.planner.environment.obstacles.append(
                    blocked_position
                )

            alternative_path = (
                self.planner.find_path(
                    start,
                    goal,
                    traffic_objects
                )
            )

            if alternative_path:

                candidates.append(
                    alternative_path
                )

        # Restore environment
        self.planner.environment.obstacles = (
            original_obstacles
        )

        # Remove duplicates
        unique_paths = []

        for path in candidates:

            if path not in unique_paths:

                unique_paths.append(
                    path
                )

        return unique_paths

    # ---------------------------------------------------------
    # MAIN DECISION ENGINE
    # ---------------------------------------------------------

    def find_safe_path(
        self,
        start,
        goal,
        traffic_objects
    ):

        candidates = (
            self.generate_candidate_paths(
                start,
                goal,
                traffic_objects
            )
        )

        # -----------------------------------------------------
        # NO PATH
        # -----------------------------------------------------

        if not candidates:

            return {
                "decision": "STOP",
                "path": [],
                "risk": "DANGER",
                "candidate_count": 0
            }

        # -----------------------------------------------------
        # SCORE ALL CANDIDATES
        # -----------------------------------------------------

        scored_paths = []

        for path in candidates:

            risk = (
                self.calculate_path_risk(
                    path,
                    traffic_objects
                )
            )

            score = (
                self.score_path(
                    path,
                    traffic_objects
                )
            )

            scored_paths.append(
                {
                    "path": path,
                    "score": score,
                    "risk": risk
                }
            )

        # Lowest score = preferred path
        scored_paths.sort(
            key=lambda item: item["score"]
        )

        best = scored_paths[0]

        best_path = best["path"]
        best_risk = best["risk"]

        # -----------------------------------------------------
        # DANGER
        # -----------------------------------------------------

        if best_risk == "DANGER":

            return {
                "decision": "STOP",
                "path": best_path,
                "risk": "DANGER",
                "candidate_count":
                    len(scored_paths)
            }

        # -----------------------------------------------------
        # WARNING
        # -----------------------------------------------------

        if best_risk == "WARNING":

            safe_alternatives = [

                item

                for item in scored_paths

                if item["risk"] == "SAFE"

            ]

            if safe_alternatives:

                safest = safe_alternatives[0]

                # IMPORTANT:
                # Only REPLAN when a genuinely
                # safer alternative exists.

                return {
                    "decision": "REPLAN",
                    "path": safest["path"],
                    "risk": "SAFE",
                    "candidate_count":
                        len(scored_paths)
                }

            # No safe alternative.
            # Wait for traffic to clear.

            return {
                "decision": "WAIT",
                "path": best_path,
                "risk": "WARNING",
                "candidate_count":
                    len(scored_paths)
            }

        # -----------------------------------------------------
        # SAFE
        # -----------------------------------------------------

        # If the selected path is SAFE,
        # simply continue.

        return {
            "decision": "CONTINUE",
            "path": best_path,
            "risk": "SAFE",
            "candidate_count":
                len(scored_paths)
        }

    # ---------------------------------------------------------
    # ALTERNATIVE PATH
    # ---------------------------------------------------------

    def find_alternative_path(
        self,
        start,
        goal,
        traffic_objects
    ):

        return self.find_safe_path(
            start,
            goal,
            traffic_objects
        )

    # ---------------------------------------------------------
    # EVALUATE EXISTING PATH
    # ---------------------------------------------------------

    def evaluate_path(
        self,
        path,
        traffic_objects
    ):

        risk = (
            self.calculate_path_risk(
                path,
                traffic_objects
            )
        )

        if risk == "DANGER":

            return "REPLAN"

        if risk == "WARNING":

            return "WAIT"

        return "CONTINUE"