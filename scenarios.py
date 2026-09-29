SCENARIOS = {

    "village_road": {
        "name": "Unmarked Village Road",
        "description": "Unmarked road with unclear road boundaries and unexpected obstacles.",
        "obstacles": [
            (8, 8),
            (12, 7),
            (15, 10)
        ],
        "traffic": [
            {
                "id": "village_vehicle",
                "x": 10,
                "y": 6,
                "speed": 10,
                "direction": "east"
            }
        ]
    },

    "urban_intersection": {
        "name": "Urban Intersection",
        "description": "Busy intersection with multiple moving vehicles.",
        "obstacles": [
            (10, 7),
            (10, 8),
            (14, 8)
        ],
        "traffic": [
            {
                "id": "car_1",
                "x": 8,
                "y": 8,
                "speed": 20,
                "direction": "east"
            },
            {
                "id": "car_2",
                "x": 13,
                "y": 5,
                "speed": 15,
                "direction": "south"
            }
        ]
    },

    "highway_merge": {
        "name": "Highway Merge",
        "description": "Slow-moving traffic merging into the vehicle's route.",
        "obstacles": [
            (12, 6),
            (12, 7)
        ],
        "traffic": [
            {
                "id": "slow_truck",
                "x": 10,
                "y": 7,
                "speed": 8,
                "direction": "east"
            }
        ]
    },

    "dense_market": {
        "name": "Dense Market",
        "description": "Crowded area with vehicles and pedestrians creating uncertain movement.",
        "obstacles": [
            (8, 6),
            (9, 6),
            (10, 6),
            (8, 7),
            (10, 7),
            (9, 9),
            (12, 8)
        ],
        "traffic": [
            {
                "id": "market_auto",
                "x": 7,
                "y": 8,
                "speed": 8,
                "direction": "east"
            },
            {
                "id": "market_vehicle",
                "x": 13,
                "y": 9,
                "speed": 10,
                "direction": "west"
            }
        ]
    },

    "cattle_crossing": {
        "name": "Sudden Cattle Crossing",
        "description": "An animal suddenly enters the vehicle's path.",
        "obstacles": [],
        "traffic": [
            {
                "id": "cattle",
                "x": 0,
                "y": 11,
                "speed": 2,
                "direction": "east"
            }
        ]
    }
}