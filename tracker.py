import cv2
from ultralytics import YOLO
import supervision as sv
from crash_detection import detect_crash, reset_crash_data
from violation import check_overspeed, reset_violation_data
from risk_assessment import process_violation, risk_state

# load models
vehicle_model = YOLO("yolov8n.pt")
helmet_model = YOLO("best.pt")
pothole_model = YOLO("pothole_yolo.pt")   # added pothole model

print(helmet_model.names)

def process_video(video_path):
    # Reset external states for new video
    reset_crash_data()
    reset_violation_data()
    risk_state.reset_state()

    # open video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video: {video_path}")
        return
        
    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = int(1000 / fps) if fps > 0 else 30

    previous_positions = {}
    speed_history = {}

    tracker = sv.ByteTrack(track_activation_threshold=0.25)

    box_annotator = sv.BoxAnnotator()
    label_annotator = sv.LabelAnnotator()

    TARGET_CLASSES = [0,1,2,3,5,7,16]

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        vehicle_data = {}
        helmet_data = {}

        # ---------------- VEHICLE DETECTION ----------------
        results = vehicle_model(frame, conf=0.25, imgsz=512, verbose=False)[0]
        detections = sv.Detections.from_ultralytics(results)

        mask = [class_id in TARGET_CLASSES for class_id in detections.class_id]
        detections = detections[mask]

        detections = tracker.update_with_detections(detections)

        labels = []

        for xyxy, tracker_id, class_id in zip(
            detections.xyxy,
            detections.tracker_id,
            detections.class_id
        ):
            name = vehicle_model.names[class_id]

            if tracker_id is None:
                labels.append(name)
                continue

            x1, y1, x2, y2 = xyxy

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            speed = 0

            if tracker_id in previous_positions:
                prev_x, prev_y = previous_positions[tracker_id]
                distance = ((center_x - prev_x)**2 + (center_y - prev_y)**2) ** 0.5
                box_height = y2 - y1

                reference_height = 60
                perspective_factor = reference_height / box_height
                perspective_factor = max(0.7, min(1.8, perspective_factor))

                if 1 < distance < 20:
                    speed = distance * 3.8 * perspective_factor
                else:
                    speed = 0

            previous_positions[tracker_id] = (center_x, center_y)

            if tracker_id not in speed_history:
                speed_history[tracker_id] = []

            speed_history[tracker_id].append(speed)

            if len(speed_history[tracker_id]) > 5:
                speed_history[tracker_id].pop(0)

            sorted_speeds = sorted(speed_history[tracker_id])
            filtered_speed = sorted_speeds[len(sorted_speeds)//2]

            vehicle_data[tracker_id] = {
                "box": (x1, y1, x2, y2),
                "speed": filtered_speed
            }

            label = f"{name} ID {tracker_id} {int(filtered_speed)} km/h"
            labels.append(label)

        # ---------------- HELMET DETECTION ----------------
        helmet_results = helmet_model(frame, conf=0.25, imgsz=512, verbose=False)[0]
        helmet_detections = sv.Detections.from_ultralytics(helmet_results)

        for xyxy, class_id in zip(
            helmet_detections.xyxy,
            helmet_detections.class_id
        ):
            name = helmet_model.names[class_id]
            x1, y1, x2, y2 = xyxy

            if name == "no_helmet":
                for v_id, v in vehicle_data.items():
                    vx1, vy1, vx2, vy2 = v["box"]

                    overlap_w = min(x2, vx2) - max(x1, vx1)
                    overlap_h = min(y2, vy2) - max(y1, vy1)

                    if overlap_w > 0 and overlap_h > 0:
                        if v_id not in risk_state.vehicle_violations or "no_helmet" not in risk_state.vehicle_violations[v_id]:
                            print(f"⚠ Helmet violation | Vehicle ID: {v_id}")
                            process_violation("no_helmet", v_id, frame)

                cv2.putText(
                    frame,
                    "⚠ NO HELMET",
                    (int(x1), int(y1)-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0,0,255),
                    2
                )

        # ---------------- POTHOLE DETECTION ----------------
        pothole_results = pothole_model(frame, conf=0.25, imgsz=512, verbose=False)[0]
        pothole_detections = sv.Detections.from_ultralytics(pothole_results)

        for xyxy in pothole_detections.xyxy:
            x1, y1, x2, y2 = xyxy

            if not risk_state.pothole_reported:
                print("⚠ Road contains potholes")
                process_violation("pothole", None, frame)

            cv2.putText(
                frame,
                "⚠ POTHOLE",
                (int(x1), int(y1)-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,0,255),
                2
            )

        # ---------------- MODULES ----------------
        detect_crash(vehicle_data, frame)
        check_overspeed(vehicle_data, frame)

        # ---------------- DRAWING ----------------
        annotated_frame = box_annotator.annotate(
            scene=frame,
            detections=detections
        )

        annotated_frame = label_annotator.annotate(
            scene=annotated_frame,
            detections=detections,
            labels=labels
        )

        annotated_frame = box_annotator.annotate(
            scene=annotated_frame,
            detections=pothole_detections
        )

        display_frame = cv2.resize(annotated_frame, (1280, 720))
        
        # Convert BGR to RGB for Streamlit/Web rendering
        output_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        
        # Yield the output frame so Streamlit can display it
        yield output_frame

    cap.release()