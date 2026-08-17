import camera
import cv2 as cv
import hand_tracker
import gestures
import mouse_controller

import time

cam = camera.Camera()
tracker = hand_tracker.HandTracker()
recog = gestures.GestureRecognizer()
controller = mouse_controller.MouseController()


cam.open()
start_time = time.perf_counter()

try:

    while True:
        
        frame =cam.get_frame()
        if frame is None: 
            continue
        timestamp_ms = int((time.perf_counter() - start_time) * 1000)
        hands = tracker.detect(frame,timestamp_ms)
    
        for hand in hands :
            gesture = recog.detect(hand)
            controller.update(hand,gesture)
    
        v_frame = tracker.visualize(frame,hands)
    
    
        cv.imshow('AirPoint', v_frame)

        if cv.waitKey(1) & 0xFF == ord("q"):
            break

except KeyboardInterrupt : 

    print("Keyboard Interruption . Stopping ... ")
    
finally:
    cam.release()

