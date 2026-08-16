import pyautogui
from gestures import Gesture
from pynput.mouse import Controller, Button


class MouseController:

    def __init__(self):

        self.screen_width, self.screen_height = pyautogui.size()
        pyautogui.PAUSE = 0
        pyautogui.FAILSAFE = False

        self.prev_x = 0
        self.prev_y = 0
        self.prev_filtered_x = 0
        self.prev_filtered_y = 0
        self.is_initialized = False

        self.min_speed = 0
        self.max_speed = 150
        self.min_alpha = 0.10
        self.max_alpha = 0.6

        self.active_width = 0.60

        self.camera_aspect_width = 16
        self.camera_aspect_height = 9

        self.active_height = (self.active_width * self.camera_aspect_height/ self.camera_aspect_width)

        self.active_left = (1.0 - self.active_width) / 2
        self.active_right = self.active_left + self.active_width

        self.active_top = (1.0 - self.active_height) / 2
        self.active_bottom = self.active_top + self.active_height

        self.previous_gesture = Gesture.NONE

        self.mouse = Controller()

    def update(self, hand, gesture):

        if gesture is Gesture.MOVE:

            self._move_cursor(hand)

        elif ( gesture is Gesture.DOUBLE_CLICK and self.previous_gesture is not Gesture.DOUBLE_CLICK):

            self._double_click()

        self.previous_gesture = gesture

    def _move_cursor(self, hand):

        index_tip = hand.index_tip

        x = index_tip.x
        y = index_tip.y

        x = max(self.active_left, min(x, self.active_right))
        y = max(self.active_top, min(y, self.active_bottom))

        x_factor = ( (x - self.active_left) / (self.active_right - self.active_left))

        y_factor = ( (y - self.active_top) / (self.active_bottom - self.active_top))

        screen_x = int(x_factor * self.screen_width)
        screen_y = int(y_factor * self.screen_height)

        if not self.is_initialized:

            self.prev_x = screen_x
            self.prev_y = screen_y
            self.prev_filtered_x = screen_x
            self.prev_filtered_y = screen_y
            self.is_initialized = True

            pyautogui.moveTo(screen_x, screen_y)
            return

        dx = screen_x - self.prev_x
        dy = screen_y - self.prev_y
        speed = (dx ** 2 + dy ** 2) ** 0.5

        alpha = self._calculate_alpha(speed)

        filtered_x = ( alpha * screen_x + (1 - alpha) * self.prev_filtered_x )

        filtered_y = ( alpha * screen_y + (1 - alpha) * self.prev_filtered_y )

        pyautogui.moveTo(int(filtered_x), int(filtered_y))

        self.prev_x = screen_x
        self.prev_y = screen_y
        self.prev_filtered_x = filtered_x
        self.prev_filtered_y = filtered_y

    def _calculate_alpha(self, speed):

        if speed < self.min_speed:
            speed = self.min_speed

        if speed > self.max_speed:
            speed = self.max_speed

        alpha = (self.min_alpha+ (speed - self.min_speed)* (self.max_alpha - self.min_alpha)/ (self.max_speed - self.min_speed))

        return alpha

    def _double_click(self):

        self.mouse.click(Button.left, 2)
        
