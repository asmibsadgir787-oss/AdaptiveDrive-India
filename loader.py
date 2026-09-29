from scenarios.scenarios import SCENARIOS


def load_scenario(scenario_id):
    if scenario_id not in SCENARIOS:
        raise ValueError(
            f"Unknown scenario: {scenario_id}"
        )

    return SCENARIOS[scenario_id]