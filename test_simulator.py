from models.vehicle import Vehicle
from models.environment import Environment

from planning.astar import AStarPlanner
from planning.cost_function import TrafficCostFunction
from planning.risk_engine import RiskEngine
from planning.replanner import Replanner
from planning.traffic import TrafficObject

from simulation.simulator import Simulator


environment = Environment()

vehicle = Vehicle(
    x=2,
    y=13,
    speed=20,
    direction="north",
    destination_x=21,
    destination_y=2
)

cost_function = TrafficCostFunction()

planner = AStarPlanner(
    environment,
    cost_function
)

risk_engine = RiskEngine()

replanner = Replanner(
    planner,
    risk_engine
)

traffic = TrafficObject(
    object_id="vehicle_1",
    x=10,
    y=8,
    speed=20,
    direction="east"
)

simulator = Simulator(
    vehicle,
    environment,
    planner,
    replanner,
    [traffic]
)


for i in range(10):

    result = simulator.run_step()

    print("Step:", result["step"])
    print("Vehicle:", result["vehicle_position"])
    print("Decision:", result["decision"])
    print("Traffic:", result["traffic"])
    print("-" * 40)

    if simulator.is_finished():
        print("Destination reached!")
        break