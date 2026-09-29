from models.vehicle import Vehicle
from models.environment import Environment

from planning.astar import AStarPlanner
from planning.cost_function import TrafficCostFunction
from planning.risk_engine import RiskEngine
from planning.replanner import Replanner
from planning.traffic import TrafficObject

from simulation.simulator import Simulator

from scenarios.loader import load_scenario


def create_simulator(scenario_id):

    scenario = load_scenario(scenario_id)

    environment = Environment()

    # Add fixed obstacles
    for obstacle in scenario["obstacles"]:
        environment.add_obstacle(
            obstacle[0],
            obstacle[1]
        )

    # Create our autonomous vehicle
    vehicle = Vehicle(
        x=2,
        y=13,
        speed=20,
        direction="north",
        destination_x=21,
        destination_y=2
    )

    # Create traffic objects
    traffic_objects = []

    for traffic_data in scenario["traffic"]:

        traffic = TrafficObject(
            object_id=traffic_data["id"],
            x=traffic_data["x"],
            y=traffic_data["y"],
            speed=traffic_data["speed"],
            direction=traffic_data["direction"]
        )

        traffic_objects.append(traffic)

    # Create planning system
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

    # Create simulator
    simulator = Simulator(
        vehicle,
        environment,
        planner,
        replanner,
        traffic_objects
    )

    return simulator