from email_alert import send_email_alert

class RiskState:
    def __init__(self):
        # Maps vehicle_id to a set of its active violations
        self.vehicle_violations = {}
        # Tracks if a pothole warning has already been sent for the video
        self.pothole_reported = False

    def reset_state(self):
        self.vehicle_violations.clear()
        self.pothole_reported = False

# Global instance for tracking state across the current video stream
risk_state = RiskState()

def calculate_risk(no_helmet, overspeed, pothole, crash):
    """
    Calculates the risk score from 4 to 10 based on the provided booleans.
    Overrides combined scores as specified by the user.
    """
    if crash:
        return 10

    if no_helmet and overspeed and pothole:
        return 10

    if no_helmet and overspeed:
        return 9

    if overspeed and pothole:
        return 8

    if no_helmet and pothole:
        return 8

    if no_helmet:
        return 7

    if overspeed:
        return 6

    if pothole:
        return 4
    
    return 0

def process_violation(violation_type, vehicle_id, frame=None):
    """
    Called whenever a violation occurs. Updates the vehicle's state,
    calculates the new risk score, and sends the formatted email alert.
    """
    # Initialize state for this vehicle if not exists
    if vehicle_id is not None and vehicle_id not in risk_state.vehicle_violations:
        risk_state.vehicle_violations[vehicle_id] = set()

    # Track pothole globally or per vehicle
    if violation_type == "pothole":
        if risk_state.pothole_reported:
            return # Only email once about the road condition
        risk_state.pothole_reported = True
        # For calculation, a general pothole applies to all current calculations or acts independently
        no_helmet = False
        overspeed = False
        crash = False
        pothole = True
    else:
        # Add new violation to this specific vehicle's set
        risk_state.vehicle_violations[vehicle_id].add(violation_type)
        
        # Determine the current state booleans for this vehicle
        violations = risk_state.vehicle_violations[vehicle_id]
        no_helmet = "no_helmet" in violations
        overspeed = "overspeed" in violations
        crash = "crash" in violations
        pothole = risk_state.pothole_reported  # Environmental hazard applies to vehicle's risk

    score = calculate_risk(no_helmet, overspeed, pothole, crash)

    if violation_type == "pothole":
        violation_string = "Pothole"
    else:
        # Construct dynamic string like "No Helmet + Overspeed"
        active_str = []
        if no_helmet: active_str.append("No Helmet")
        if overspeed: active_str.append("Overspeed")
        if pothole: active_str.append("Pothole")
        if crash: active_str = ["Crash"] # Override display if crashed
        
        violation_string = " + ".join(active_str)

    # Compose the email body
    email_body = f"Violation Detected: {violation_string}\nRisk Score: {score}/10"

    if vehicle_id is not None:
        email_body += f"\nVehicle ID: {vehicle_id}"

    send_email_alert(
        "Road Safety Alert",
        email_body,
        frame
    )
