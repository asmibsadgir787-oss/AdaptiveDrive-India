from models.environment import Environment
from planning.astar import AStarPlanner
from planning.risk_engine import RiskEngine
from planning.replanner import Replanner
from planning.traffic import TrafficObject


# Create environment
environment = Environment()

# Create path planner
planner = AStarPlanner(environment)

# Create risk engine
risk_engine = RiskEngine()

# Create replanner
replanner = Replanner(
    planner,
    risk_engine
)

# Create a traffic vehicle
traffic = TrafficObject(
    object_id="vehicle_1",
    x=2,
    y=8,
    speed=20,
    direction="north"
)

# Start and destination
start = (2, 13)
goal = (21, 2)

# Find and evaluate path
result = replanner.find_safe_path(
    start,
    goal,
    [traffic]
)

print("Decision:", result["decision"])
print("Path:", result["path"])
print("Number of steps:", len(result["path"]))