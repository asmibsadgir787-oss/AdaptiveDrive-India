from models.vehicle import Vehicle
from models.environment import Environment
from planning.astar import AStarPlanner
from planning.cost_function import TrafficCostFunction
from planning.risk_engine import RiskEngine
from planning.replanner import Replanner
from planning.traffic import TrafficObject
from simulation.simulator import Simulator


# --------------------------------------------------
# 1. CREATE ENVIRONMENT
# --------------------------------------------------

environment = Environment(
    width=24,
    height=16
)


# --------------------------------------------------
# 2. CREATE OUR VEHICLE
# --------------------------------------------------

vehicle = Vehicle(
    x=2,
    y=13,
    speed=20,
    direction="north",
    destination_x=2,
    destination_y=2
)


# --------------------------------------------------
# 3. START WITH TRAFFIC AWAY FROM OUR ROUTE
# --------------------------------------------------

traffic = TrafficObject(
    object_id="dynamic_vehicle",
    x=15,
    y=10,
    speed=1,
    direction="west"
)

traffic_objects = [traffic]


# --------------------------------------------------
# 4. CREATE PLANNER + RISK ENGINE
# --------------------------------------------------

cost_function = TrafficCostFunction()

planner = AStarPlanner(
    environment,
    cost_function
)

risk_engine = RiskEngine(
    warning_distance=3.0,
    danger_distance=1.5
)

replanner = Replanner(
    planner,
    risk_engine
)


# --------------------------------------------------
# 5. CREATE SIMULATOR
# --------------------------------------------------

simulator = Simulator(
    vehicle,
    environment,
    planner,
    replanner,
    traffic_objects
)


# --------------------------------------------------
# 6. RUN SIMULATION
# --------------------------------------------------

for i in range(12):

    # After a few steps, introduce a dynamic obstacle
    # near the vehicle's route.
    if i == 3:

        traffic.x = 2
        traffic.y = 10
        traffic.direction = "east"

        print()
        print(">>> DYNAMIC TRAFFIC APPEARED <<<")
        print()

    result = simulator.run_step()

    print("Step:", result["step"])
    print("Vehicle:", result["vehicle_position"])
    print("Decision:", result["decision"])
    print("Path:", result["path"])
    print("Traffic:", result["traffic"])
    print("-" * 50)