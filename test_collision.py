from planning.safety.collision_checker import CollisionChecker


checker = CollisionChecker(safety_distance=1.0)

vehicle_position = (5, 5)

obstacle_near = (5, 5)
obstacle_far = (10, 10)

print(
    "Collision with near obstacle:",
    checker.is_collision(vehicle_position, obstacle_near)
)

print(
    "Collision with far obstacle:",
    checker.is_collision(vehicle_position, obstacle_far)
)


path = [
    (5, 5),
    (6, 5),
    (7, 5),
    (8, 5)
]

obstacles = [
    (10, 10)
]

print(
    "Is path safe:",
    checker.is_path_safe(path, obstacles)
)