from planning.cost_function import TrafficCostFunction
from planning.traffic import TrafficObject


cost_function = TrafficCostFunction()

traffic = TrafficObject(
    object_id="vehicle_1",
    x=10,
    y=8,
    speed=20,
    direction="east"
)

safe_position = (2, 2)
warning_position = (8, 8)
danger_position = (10, 8)

print(
    "Safe position cost:",
    cost_function.get_position_cost(
        safe_position,
        [traffic]
    )
)

print(
    "Warning position cost:",
    cost_function.get_position_cost(
        warning_position,
        [traffic]
    )
)

print(
    "Danger position cost:",
    cost_function.get_position_cost(
        danger_position,
        [traffic]
    )
)