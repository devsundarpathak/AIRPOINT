import mediapipe as mp
import cv2 as cv
from models import Hand,Landmark

HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),

    (0, 5), (5, 6), (6, 7), (7, 8),

    (5, 9), (9, 10), (10, 11), (11, 12),

    (9, 13), (13, 14), (14, 15), (15, 16),

    (13, 17), (17, 18), (18, 19), (19, 20),

    (0, 17)
]

class HandTracker:
    
    def __init__(self):
        
        BaseOptions = mp.tasks.BaseOptions
        HandLandmarker = mp.tasks.vision.HandLandmarker
        HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        # Create a hand landmarker instance with the image mode
        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
            num_hands=1,
            running_mode=VisionRunningMode.VIDEO)

        self.landmarker = HandLandmarker.create_from_options(options)

    def detect(self, frame , timestamp_ms):
        
        image_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)

        result = self.landmarker.detect_for_video(mp_image,timestamp_ms)
        
        hands = []

        for mp_hand_landmarks, mp_handedness in zip(
            result.hand_landmarks,
            result.handedness,
        ):
            hand = self._convert_hand(
                mp_hand_landmarks,
                mp_handedness,
            )
            hands.append(hand)

        return hands

    def _convert_hand(
        self,
        mp_hand_landmarks,
        mp_handedness,
    ) -> Hand:

        landmarks = [
            Landmark(
                x=lm.x,
                y=lm.y,
                z=lm.z,
            )
            for lm in mp_hand_landmarks
        ]

        classification = mp_handedness[0]

        return Hand(
            landmarks=landmarks,
            handedness=classification.category_name,
            handedness_score=classification.score,
        )

    def visualize(self, frame, hands: list[Hand]):
        h, w = frame.shape[:2]

        for hand in hands:
            # Draw landmark points
            for landmark in hand.landmarks:
                x = int(landmark.x * w)
                y = int(landmark.y * h)

                cv.circle(frame, (x, y), 8, (0, 255, 0), -1)

            # Draw connections
            for start_idx, end_idx in HAND_CONNECTIONS:
                start = hand.landmarks[start_idx]
                end = hand.landmarks[end_idx]

                start_point = (
                    int(start.x * w),
                    int(start.y * h),
                )
                end_point = (
                    int(end.x * w),
                    int(end.y * h),
                )

                cv.line(frame, start_point, end_point, (255, 0, 0), 2)

        return frame
    