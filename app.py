import cv2
import numpy as np
import mediapipe as mp
import pygame
import time

# Initialize pygame for sound notifications
pygame.mixer.init()
sound = pygame.mixer.Sound("./level-up-191997.mp3")  # path to your sound file

# Initialize MediaPipe face mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

# Initialize video capture with higher resolution
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

def calculate_distance(point1, point2):
    return np.linalg.norm(np.array(point1) - np.array(point2))

def get_average_distance(num_samples=30, message=""):
    distances = []
    print(message)
    start_message = "Press 'y' when you are ready to start capturing."

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image")
            return None
        # Display the message on the frame
        cv2.putText(frame, start_message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('y'):
            break

    capture_message = "Capturing... Please keep your face steady."

    for i in range(num_samples):
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image")
            return None
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                point1 = (int(face_landmarks.landmark[107].x * frame.shape[1]), int(face_landmarks.landmark[107].y * frame.shape[0]))
                point2 = (int(face_landmarks.landmark[336].x * frame.shape[1]), int(face_landmarks.landmark[336].y * frame.shape[0]))
                distance = calculate_distance(point1, point2)
                distances.append(distance)
                cv2.circle(frame, point1, 2, (0, 255, 0), -1)
                cv2.circle(frame, point2, 2, (0, 255, 0), -1)
                cv2.line(frame, point1, point2, (255, 0, 0), 1)
                cv2.putText(frame, capture_message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(frame, f"Sample {i+1}/{num_samples}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        else:
            i -= 1  # If no landmarks are detected, retry this iteration
        time.sleep(0.2)  # Delay to slow down the sample capture

    avg_distance = np.mean(distances)
    print(f"Average distance: {avg_distance}")
    return avg_distance

# Calibration phase
print("Starting calibration...")

# Relaxed face calibration
relaxed_distance = get_average_distance(message="Please keep your face relaxed for calibration.")

# Prompt before scrunching forehead
print("Now prepare to scrunch your forehead for calibration.")
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image")
        break
    cv2.putText(frame, "Press 'y' to start scrunching calibration", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('y'):
        break

# Scrunch forehead calibration
scrunch_distance = get_average_distance(message="Please scrunch your forehead for calibration.")

threshold = (relaxed_distance + scrunch_distance) / 2
print(f"Calibration complete. Using threshold: {threshold}")

# Main loop
scrunch_detected = False
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image")
        break

    # Convert the frame to RGB as MediaPipe expects RGB images
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Face Mesh
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Coordinates for the points between the eyebrows (landmarks 107 and 336)
            point1 = (int(face_landmarks.landmark[107].x * frame.shape[1]), int(face_landmarks.landmark[107].y * frame.shape[0]))
            point2 = (int(face_landmarks.landmark[336].x * frame.shape[1]), int(face_landmarks.landmark[336].y * frame.shape[0]))

            # Calculate the distance between the points
            distance = calculate_distance(point1, point2)
            print(f"Distance: {distance}")  # Debugging information

            # Detect scrunch based on personalized threshold
            if distance < threshold and not scrunch_detected:
                print("Scrunch detected!")
                sound.play()
                scrunch_detected = True
            elif distance >= threshold:
                scrunch_detected = False

            # Draw circles around the landmarks
            cv2.circle(frame, point1, 2, (0, 255, 0), -1)
            cv2.circle(frame, point2, 2, (0, 255, 0), -1)

            # Draw a line between the landmarks
            cv2.line(frame, point1, point2, (255, 0, 0), 1)

    # Display the frame
    cv2.imshow('frame', frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
