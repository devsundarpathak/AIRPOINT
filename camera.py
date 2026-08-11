import numpy as np
import cv2 as cv

class Camera:
    def __init__(self):
        self.cap = None

    def open(self):
        '''creates the videocapture obeject'''
        self.cap = cv.VideoCapture(0)

        if not self.cap.isOpened():
            return False
        else:
            return True

    def get_frame(self):
        '''returns mirrored camera frame'''
        ret, frame = self.cap.read() 

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            return None
        frame = cv.flip(frame, 1)

        return frame
    
    def release(self):
        '''releases the video capture object and destroy the window created'''
        self.cap.release()
        cv.destroyAllWindows()
