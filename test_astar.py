from models.environment import Environment
from planning.astar import AStarPlanner
from planning.cost_function import TrafficCostFunction
from planning.traffic import TrafficObject


# Create environment
environment = Environment()

# Create traffic cost function
cost_function = TrafficCostFunction()

# Create traffic object
traffic = TrafficObject(
    object_id="vehicle_1",
    x=2,
    y=8,
    speed=20,
    direction="east"
)

# Create planner with traffic awareness
planner = AStarPlanner(
    environment,
    cost_function
)

# Start and destination
start = (2, 13)
goal = (21, 2)

# Find traffic-aware path
path = planner.find_path(
    start,
    goal,
    [traffic]
)

print("Start:", start)
print("Destination:", goal)
print("Traffic position:", traffic.get_position())
print("Path found:", path)
print("Number of steps:", len(path))