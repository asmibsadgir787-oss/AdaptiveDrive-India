from models.vehicle import Vehicle
from models.environment import Environment
from planning.astar import AStarPlanner
from planning.cost_function import TrafficCostFunction
from planning.risk_engine import RiskEngine
from planning.replanner import Replanner
from planning.traffic import TrafficObject
from simulation.simulator import Simulator

environment = Environment(
    width=24,
    height=16
)

vehicle = Vehicle(
    x=2,
    y=13,
    speed=20,
    direction="north",
    destination_x=2,
    destination_y=2
)

traffic = TrafficObject(
    object_id="dynamic_vehicle",
    x=15,
    y=10,
    speed=1,
    direction="west"
)

traffic_objects = [traffic]

cost_function = TrafficCostFunction()
planner = AStarPlanner(environment, cost_function)

risk_engine = RiskEngine(
    warning_distance=3.0,
    danger_distance=1.5
)

replanner = Replanner(
    planner,
    risk_engine
)

simulator = Simulator(
    vehicle,
    environment,
    planner,
    replanner,
    traffic_objects
)

for i in range(12):

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
