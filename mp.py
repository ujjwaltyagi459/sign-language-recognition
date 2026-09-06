import cv2
import mediapipe as mp
import numpy as np

class SignLanguageDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils

    def detect_sign(self, hand_landmarks, handedness):
        if not hand_landmarks:
            return "No hand detected", ""

        # Get all important landmarks
        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        middle_tip = hand_landmarks.landmark[12]
        ring_tip = hand_landmarks.landmark[16]
        pinky_tip = hand_landmarks.landmark[20]
        wrist = hand_landmarks.landmark[0]

        # Determine if the palm is facing the camera
        palm_facing_camera = thumb_tip.z < wrist.z

        # Thumb detection logic (not used for new "Yes" gesture)
        thumb_up = (thumb_tip.x > hand_landmarks.landmark[2].x) if handedness == "Right" else (thumb_tip.x < hand_landmarks.landmark[2].x)

        # Finger detection for the index, middle, ring, and pinky
        index_up = index_tip.y < hand_landmarks.landmark[6].y  # PIP joint of index finger
        middle_up = middle_tip.y < hand_landmarks.landmark[10].y  # PIP joint of middle finger
        ring_up = ring_tip.y < hand_landmarks.landmark[14].y  # PIP joint of ring finger
        pinky_up = pinky_tip.y < hand_landmarks.landmark[18].y  # PIP joint of pinky finger

        # If palm is facing the camera, flip the detection for thumb
        if palm_facing_camera:
            thumb_up = not thumb_up

        # Debugging text for finger states
        debug_text = f"T={thumb_up}, I={index_up}, M={middle_up}, R={ring_up}, P={pinky_up}"

        # Gesture detection logic: New "Yes" is when only the index finger is raised
        if index_up and not (thumb_up or middle_up or ring_up or pinky_up):
            return "Yes", debug_text  # Only index raised
        elif thumb_up and pinky_up and not (index_up or middle_up or ring_up):
            return "Hello", debug_text  # Thumb and pinky raised
        elif index_up and middle_up and not (thumb_up or ring_up or pinky_up):
            return "Thank You", debug_text  # Index and middle fingers raised
        elif thumb_up and index_up and middle_up and ring_up and pinky_up:
            return "No", debug_text  # All fingers raised

        return "Unknown sign", debug_text

    def start_detection(self):
        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Failed to capture video")
                break

            # Flip the image horizontally for a later selfie-view display
            image = cv2.flip(image, 1)

            # Convert the BGR image to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Process the image and detect hands
            results = self.hands.process(image_rgb)

            # Clear background for better visibility
            image.fill(255)  # White background

            # Draw hand landmarks and process gestures
            if results.multi_hand_landmarks and results.multi_handedness:
                for hand_landmarks, handedness_info in zip(results.multi_hand_landmarks, results.multi_handedness):
                    # Determine handedness
                    handedness = handedness_info.classification[0].label  # "Left" or "Right"

                    # Draw landmarks
                    self.mp_draw.draw_landmarks(
                        image,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_draw.DrawingSpec(color=(0, 0, 255), thickness=4, circle_radius=8),
                        self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=4)
                    )

                    # Detect and display the sign
                    sign, debug_info = self.detect_sign(hand_landmarks, handedness)

                    # Display sign with larger text
                    cv2.putText(
                        image,
                        f"Sign: {sign} ({handedness})",
                        (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        2,  # Larger font size
                        (0, 0, 255),  # Red color
                        3
                    )

                    # Display debug info
                    cv2.putText(
                        image,
                        debug_info,
                        (20, 100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2
                    )

            # Display the image
            cv2.imshow('Sign Language Detector', image)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release resources
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    print("Starting Sign Language Detection...")
    print("\nGESTURE INSTRUCTIONS:")
    print("1. Hello: Thumb and pinky raised, others down")
    print("2. Thank You: Index and middle fingers raised, others down")
    print("3. Yes: Only index raised, others down")
    print("4. No: All fingers raised\n")
    print("Press 'q' to quit")
    detector = SignLanguageDetector()
    detector.start_detection()
