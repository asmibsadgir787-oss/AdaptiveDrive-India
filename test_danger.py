from models.vehicle import Vehicle
from models.environment import Environment
from planning.astar import AStarPlanner
from planning.cost_function import TrafficCostFunction
from planning.risk_engine import RiskEngine
from planning.replanner import Replanner
from planning.traffic import TrafficObject
from simulation.simulator import Simulator

environment = Environment(width=24, height=16)

vehicle = Vehicle(
    x=2,
    y=13,
    speed=20,
    direction="north",
    destination_x=2,
    destination_y=2
)

crossing_vehicle = TrafficObject(
    object_id="crossing_vehicle",
    x=0,
    y=11,
    speed=10,
    direction="east"
)

traffic_objects = [crossing_vehicle]

cost_function = TrafficCostFunction()
planner = AStarPlanner(environment, cost_function)

risk_engine = RiskEngine(
    warning_distance=3.0,
    danger_distance=1.5
)

replanner = Replanner(planner, risk_engine)

simulator = Simulator(
    vehicle,
    environment,
    planner,
    replanner,
    traffic_objects
)

for i in range(10):
    result = simulator.run_step()

    print("Step:", result["step"])
    print("Vehicle:", result["vehicle_position"])
    print("Decision:", result["decision"])
    print("Traffic:", result["traffic"])
    print("-" * 40)
