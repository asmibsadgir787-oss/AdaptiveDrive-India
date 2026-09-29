from planning.traffic import TrafficObject


vehicle = TrafficObject(
    object_id="vehicle_1",
    x=10,
    y=8,
    speed=20,
    direction="east"
)

print("Object ID:", vehicle.object_id)
print("Current position:", vehicle.get_position())
print("Speed:", vehicle.speed)
print("Direction:", vehicle.direction)

print("Predicted position after 1 step:", vehicle.predict_position(1))
print("Predicted position after 3 steps:", vehicle.predict_position(3))

vehicle.move()

print("Position after moving:", vehicle.get_position())