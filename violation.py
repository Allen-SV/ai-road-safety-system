from email_alert import send_email_alert

SPEED_LIMIT = 60
reported_overspeed = set()

def reset_violation_data():
    global reported_overspeed
    reported_overspeed.clear()

def check_overspeed(vehicle_data, frame=None):

    violations = []

    for vehicle_id, data in vehicle_data.items():

        speed = data["speed"]

        if speed > SPEED_LIMIT and vehicle_id not in reported_overspeed:

            print(f"⚠ Overspeed detected | Vehicle ID: {vehicle_id} | Speed: {int(speed)} km/h")

            send_email_alert(
                "⚠️ Overspeed Violation",
                f"Vehicle {vehicle_id} exceeded speed limit",
                frame
            )

            reported_overspeed.add(vehicle_id)

            violations.append({
                "vehicle_id": vehicle_id,
                "speed": speed,
                "type": "Overspeed"
            })

    return violations


