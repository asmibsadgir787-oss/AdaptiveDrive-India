from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4

from scenarios.runner import create_simulator
from scenarios.scenarios import SCENARIOS


app = FastAPI(
    title="AdaptiveDrive India",
    description="Backend for SIH26037 - Adaptive Path Planning and Collision Avoidance for Autonomous Vehicles on Unstructured Indian Roads.",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


active_simulations = {}


@app.get("/")
def home():
    return {
        "project": "AdaptiveDrive India",
        "problem_statement": "SIH26037",
        "status": "Backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/scenarios")
def get_scenarios():
    return {
        "scenarios": [
            {
                "id": scenario_id,
                "name": scenario_data["name"],
                "description": scenario_data["description"]
            }
            for scenario_id, scenario_data in SCENARIOS.items()
        ]
    }


@app.get("/scenario/{scenario_id}")
def run_scenario(scenario_id: str):

    simulator = create_simulator(scenario_id)

    result = simulator.run_step()

    return result


@app.post("/simulation/start/{scenario_id}")
def start_simulation(scenario_id: str):

    simulator = create_simulator(scenario_id)

    session_id = str(uuid4())

    active_simulations[session_id] = simulator

    return {
        "session_id": session_id,
        "scenario": scenario_id,
        "step": 0,
        "vehicle_position":
            simulator.vehicle.get_position(),
        "destination":
            simulator.vehicle.get_destination(),
        "decision": "READY"
    }


@app.post("/simulation/{session_id}/step")
def simulation_step(session_id: str):

    if session_id not in active_simulations:
        return {
            "error": "Simulation session not found"
        }

    simulator = active_simulations[session_id]

    result = simulator.run_step()

    return {
        "session_id":
            session_id,

        "step":
            result["step"],

        "vehicle_position":
            result["vehicle_position"],

        "destination":
            result["destination"],

        "decision":
            result["decision"],

        "risk":
            result["risk"],

        "candidate_count":
            result["candidate_count"],

        "planning_latency_ms":
            result["planning_latency_ms"],

        "path":
            result["path"],

        "predicted_traffic":
            result["predicted_traffic"],

        "traffic":
            result["traffic"],

        "obstacle_count":
            result["obstacle_count"],

        "finished":
            simulator.is_finished(),

        "collision_detected":
            result.get(
                "collision_detected",
                False
            ),

        "metrics":
            result.get(
                "metrics",
                {}
            )
    }


@app.post("/simulation/{session_id}/reset")
def reset_simulation(session_id: str):

    if session_id not in active_simulations:
        return {
            "error": "Simulation session not found"
        }

    old_simulator = active_simulations[session_id]

    scenario_id = None

    for key, value in SCENARIOS.items():

        if value["name"]:

            try:

                test_simulator = create_simulator(key)

                if (
                    test_simulator.vehicle.get_destination()
                    ==
                    old_simulator.vehicle.get_destination()
                ):
                    scenario_id = key
                    break

            except Exception:
                continue

    if scenario_id:

        active_simulations[session_id] = (
            create_simulator(scenario_id)
        )

    return {
        "session_id":
            session_id,

        "status":
            "reset"
    }