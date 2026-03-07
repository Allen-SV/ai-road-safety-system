from risk_assessment import process_violation

SPEED_LIMIT = 60

def reset_violation_data():
    pass

def check_overspeed(vehicle_data, frame=None):

    violations = []

    for vehicle_id, data in vehicle_data.items():

        speed = data["speed"]

        if speed > SPEED_LIMIT:
            print(f"⚠ Overspeed detected | Vehicle ID: {vehicle_id} | Speed: {int(speed)} km/h")
            
            process_violation("overspeed", vehicle_id, frame)

            violations.append({
                "vehicle_id": vehicle_id,
                "speed": speed,
                "type": "Overspeed"
            })

    return violations


