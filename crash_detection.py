from risk_assessment import process_violation

previous_speeds = {}
low_speed_frames = {}

LOW_SPEED_THRESHOLD = 15
CONFIRM_FRAMES = 5
MIN_PRE_CRASH_SPEED = 25
SPEED_DROP_THRESHOLD = 20


def boxes_collide(box1, box2):

    x1, y1, x2, y2 = box1
    x3, y3, x4, y4 = box2

    overlap_w = min(x2, x4) - max(x1, x3)
    overlap_h = min(y2, y4) - max(y1, y3)

    if overlap_w <= 0 or overlap_h <= 0:
        return False

    overlap_area = overlap_w * overlap_h

    area1 = (x2 - x1) * (y2 - y1)
    area2 = (x4 - x3) * (y4 - y3)

    min_area = min(area1, area2)

    if overlap_area > 0.2 * min_area:
        return True

    return False


def reset_crash_data():
    global previous_speeds, low_speed_frames
    previous_speeds.clear()
    low_speed_frames.clear()

def detect_crash(vehicle_data, frame=None):

    ids = list(vehicle_data.keys())

    # detect potential crash
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):

            id1 = ids[i]
            id2 = ids[j]

            box1 = vehicle_data[id1]["box"]
            box2 = vehicle_data[id2]["box"]

            speed1 = vehicle_data[id1]["speed"]
            speed2 = vehicle_data[id2]["speed"]

            prev1 = previous_speeds.get(id1, speed1)
            prev2 = previous_speeds.get(id2, speed2)

            drop1 = prev1 - speed1
            drop2 = prev2 - speed2

            collision = boxes_collide(box1, box2)

            if collision:

                cond1 = prev1 > MIN_PRE_CRASH_SPEED and drop1 > SPEED_DROP_THRESHOLD
                cond2 = prev2 > MIN_PRE_CRASH_SPEED and drop2 > SPEED_DROP_THRESHOLD

                # require both vehicles to slow down (reduces overtaking false positives)
                if cond1 and cond2:

                    low_speed_frames[id1] = 0
                    low_speed_frames[id2] = 0


    # confirm crash by checking sustained low speed
    for vid in vehicle_data:

        speed = vehicle_data[vid]["speed"]

        if vid in low_speed_frames:

            if speed < LOW_SPEED_THRESHOLD:
                low_speed_frames[vid] += 1
            else:
                low_speed_frames[vid] = 0

            if low_speed_frames[vid] >= CONFIRM_FRAMES:
                print(f"CRASH CONFIRMED for vehicle {vid}")
                
                process_violation("crash", vid, frame)

                low_speed_frames.pop(vid)


    # update previous speeds
    for vid in vehicle_data:
        previous_speeds[vid] = vehicle_data[vid]["speed"]