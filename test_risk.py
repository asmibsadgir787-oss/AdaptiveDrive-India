from planning.risk_engine import RiskEngine
from planning.traffic import TrafficObject


risk_engine = RiskEngine()

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

print("Traffic position:", traffic.get_position())

print(
    "Safe position risk:",
    risk_engine.assess_position_risk(
        safe_position,
        traffic.get_position()
    )
)

print(
    "Warning position risk:",
    risk_engine.assess_position_risk(
        warning_position,
        traffic.get_position()
    )
)

print(
    "Danger position risk:",
    risk_engine.assess_position_risk(
        danger_position,
        traffic.get_position()
    )
)

test_path = [
    (2, 2),
    (4, 4),
    (6, 6),
    (8, 8),
    (10, 8)
]

print(
    "Path risk:",
    risk_engine.assess_path_risk(
        test_path,
        traffic
    )
)