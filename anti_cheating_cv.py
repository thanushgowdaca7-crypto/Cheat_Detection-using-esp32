"""
AI Anti-Cheating Demonstration
- MediaPipe Face Mesh estimates head direction.
- Looking toward camera: sends G (green LED).
- Looking to the side: sends R (red LED).
- No face or more than one face: sends R (red LED).

Install the pinned packages in requirements:
    py -m pip install opencv-python==4.10.0.84 mediapipe==0.10.21 numpy==1.26.4 pyserial

Close Arduino Serial Monitor before running this script.
Press Q in the camera window to quit.
"""

import time
from collections import deque

import cv2
import mediapipe as mp
import numpy as np
import serial

# ---------------- SETTINGS ----------------

SERIAL_PORT = "COM7"       # Change to your ESP32 COM port
BAUD_RATE = 115200
CAMERA_INDEX = 0

YAW_LIMIT_DEGREES = 25.0    # Increase if normal head movement triggers an alert
STABLE_FRAMES = 5           # Require this many consistent frames before switching
NO_FACE_GRACE_SECONDS = 0.8 # Briefly tolerate a missed face detection

# Face Mesh landmark indices:
# nose tip, chin, left eye outer corner, right eye outer corner,
# left mouth corner, right mouth corner.
LANDMARK_IDS = [1, 152, 33, 263, 61, 291]

# Approximate 3D facial reference points used by solvePnP.
MODEL_POINTS = np.array([
    (0.0, 0.0, 0.0),          # Nose tip
    (0.0, -330.0, -65.0),     # Chin
    (-225.0, 170.0, -135.0),  # Left eye outer corner
    (225.0, 170.0, -135.0),   # Right eye outer corner
    (-150.0, -150.0, -125.0), # Left mouth corner
    (150.0, -150.0, -125.0)   # Right mouth corner
], dtype=np.float64)


def connect_esp32():
    try:
        board = serial.Serial(
            port=SERIAL_PORT,
            baudrate=BAUD_RATE,
            timeout=1,
            write_timeout=1
        )
        time.sleep(2.5)  # ESP32 may reset when serial port opens
        board.reset_input_buffer()
        print(f"ESP32 connected on {SERIAL_PORT}")
        return board
    except serial.SerialException as exc:
        raise SystemExit(
            f"Could not connect to {SERIAL_PORT}: {exc}\n"
            "Check the COM port and close Arduino Serial Monitor."
        )


def estimate_head_yaw(face_landmarks, frame_width, frame_height):
    """Return estimated yaw angle in degrees, or None on estimation failure."""
    image_points = []

    for landmark_id in LANDMARK_IDS:
        landmark = face_landmarks.landmark[landmark_id]
        x = landmark.x * frame_width
        y = landmark.y * frame_height
        image_points.append((x, y))

    image_points = np.array(image_points, dtype=np.float64)

    focal_length = float(frame_width)
    camera_matrix = np.array([
        [focal_length, 0, frame_width / 2.0],
        [0, focal_length, frame_height / 2.0],
        [0, 0, 1]
    ], dtype=np.float64)

    distortion = np.zeros((4, 1), dtype=np.float64)

    success, rotation_vector, _ = cv2.solvePnP(
        MODEL_POINTS,
        image_points,
        camera_matrix,
        distortion,
        flags=cv2.SOLVEPNP_ITERATIVE
    )

    if not success:
        return None

    rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
    angles = cv2.RQDecomp3x3(rotation_matrix)[0]

    # RQDecomp3x3 returns pitch, yaw, roll in degrees.
    yaw = float(angles[1])
    return yaw


def send_status(board, status, previous_status):
    """Send only when the status changes."""
    if status != previous_status:
        board.write(status.encode("ascii"))
        board.flush()
        print("Sent to ESP32:", status)
        return status

    return previous_status


def main():
    board = connect_esp32()

    camera = cv2.VideoCapture(CAMERA_INDEX)
    if not camera.isOpened():
        board.close()
        raise SystemExit("Could not open webcam. Check CAMERA_INDEX.")

    mp_face_mesh = mp.solutions.face_mesh

    previous_status = None
    candidate_status = None
    stable_count = 0
    yaw_history = deque(maxlen=5)
    last_face_seen = time.time()

    try:
        with mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=2,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as face_mesh:

            print("Anti-cheating detection running. Press Q to quit.")

            while True:
                success, frame = camera.read()
                if not success:
                    print("Could not read webcam frame.")
                    break

                frame = cv2.flip(frame, 1)
                height, width = frame.shape[:2]

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(rgb_frame)

                desired_status = "R"
                status_text = "SYSTEM: CHECKING"
                detail_text = ""
                box_color = (0, 0, 255)

                faces = results.multi_face_landmarks

                if faces and len(faces) == 1:
                    last_face_seen = time.time()
                    face = faces[0]

                    yaw = estimate_head_yaw(face, width, height)

                    # Draw a face bounding rectangle from the mesh landmarks.
                    xs = [int(p.x * width) for p in face.landmark]
                    ys = [int(p.y * height) for p in face.landmark]
                    x_min = max(0, min(xs))
                    y_min = max(0, min(ys))
                    x_max = min(width - 1, max(xs))
                    y_max = min(height - 1, max(ys))

                    if yaw is not None:
                        yaw_history.append(yaw)
                        smooth_yaw = float(np.median(yaw_history))

                        if abs(smooth_yaw) <= YAW_LIMIT_DEGREES:
                            desired_status = "G"
                            status_text = "SYSTEM: CORRECT"
                            box_color = (0, 255, 0)
                            detail_text = f"Facing camera | Yaw: {smooth_yaw:.1f}"
                        else:
                            desired_status = "R"
                            status_text = "SYSTEM: LOOKING AWAY"
                            box_color = (0, 0, 255)
                            detail_text = f"Head turned | Yaw: {smooth_yaw:.1f}"
                    else:
                        detail_text = "Estimating head direction..."

                    cv2.rectangle(
                        frame, (x_min, y_min), (x_max, y_max),
                        box_color, 2
                    )

                elif faces and len(faces) > 1:
                    last_face_seen = time.time()
                    yaw_history.clear()
                    desired_status = "R"
                    status_text = "SYSTEM: MULTIPLE FACES"
                    detail_text = "More than one face detected"

                else:
                    yaw_history.clear()
                    if time.time() - last_face_seen >= NO_FACE_GRACE_SECONDS:
                        desired_status = "R"
                        status_text = "SYSTEM: NO FACE DETECTED"
                        detail_text = "Please face the camera"
                    else:
                        # Keep the previous state during a brief tracking loss.
                        desired_status = previous_status or "R"
                        status_text = "SYSTEM: CHECKING"
                        detail_text = "Face tracking..."

                # Require several consecutive frames before changing the LEDs.
                if desired_status == candidate_status:
                    stable_count += 1
                else:
                    candidate_status = desired_status
                    stable_count = 1

                if stable_count >= STABLE_FRAMES:
                    previous_status = send_status(
                        board, desired_status, previous_status
                    )

                # Status banner.
                banner_color = (
                    (0, 100, 0) if desired_status == "G"
                    else (0, 0, 150)
                )
                cv2.rectangle(frame, (0, 0), (width, 42), banner_color, -1)
                cv2.putText(
                    frame, status_text, (12, 29),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (255, 255, 255), 2
                )
                cv2.putText(
                    frame, detail_text, (12, height - 18),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                    (255, 255, 255), 2
                )

                cv2.imshow("ESP32 AI Anti-Cheating Detection", frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

    finally:
        try:
            board.write(b"N")
            board.flush()
            board.close()
        except Exception:
            pass

        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
