import cv2
from service import label_service

MIN_VERTICIES = 10
MAX_VERTICIES = 40
MIN_AREA = 1000
MAX_AREA= 5000

class ShapeDetector:
    def __init__(self):
        pass

    def detect_verticies(self, contour):
        perimeter = cv2.arcLength(contour, True)

        # 0.01 - 0.05
        percent = 0.004

        verticies = cv2.approxPolyDP(contour, percent * perimeter, True)

        return verticies

    def is_puzzle(self, contour):
        verticies = self.detect_verticies(contour)
        num_verticies = len(verticies)

        if num_verticies < MIN_VERTICIES or num_verticies > MAX_VERTICIES:
            return False

        area = cv2.contourArea(contour)
        if area < MIN_AREA or area > MAX_AREA:
            return False

        return True