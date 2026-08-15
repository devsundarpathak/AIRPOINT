from enum import Enum , auto

class Gesture(Enum):
    
    NONE = auto()
    MOVE = auto()
    DOUBLE_CLICK = auto()

class GestureRecognizer:
    
    def detect(self,hand):

        thumb_index_threshold = 0.045
        thumb_ring_threshold= 0.05
        
        if self._is_touching(hand.thumb_tip,hand.ring_tip,thumb_ring_threshold) :
            return Gesture.DOUBLE_CLICK

        elif self._is_touching(hand.thumb_tip, hand.index_tip,thumb_index_threshold) :
            return Gesture.MOVE
        
        else:
            return Gesture.NONE


    def _is_touching(self, point1, point2, threshold) :
        
        return point1.distance_to(point2) < threshold