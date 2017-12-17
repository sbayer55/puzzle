import cv2
from imutils import contours
import logging
from service.shape_detector_service import ShapeDetector, label_service
from service import label_service

DEFAULT_WINDOW_TITLE = "frame"
DEFAULT_WINDOW_POS = (0, 0)
CONTOUR_COLOR = (0, 255, 0)
CONTOUR_WIDTH = 1


class ImgService(object):
    def __init__(self, frame_length):
        self.logger = logging.getLogger(__name__)
        self.key = 0
        self.frame_length = frame_length
        self.dynamic_value = 127
        self.shape_detector = ShapeDetector()

    def show(self, img, title=DEFAULT_WINDOW_TITLE, pos=DEFAULT_WINDOW_POS):
        self.logger.debug("Puzzle.show()")
        text = "K: {} - DV: {}".format(self.key, self.dynamic_value)

        label_service
        label_service.label(img, text)
        cv2.imshow(title, img)

        x, y = pos
        cv2.moveWindow(title, x, y)

        self.key = cv2.waitKey(self.frame_length)

    def isolate_puzzle(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, 0)
        _, contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        contours = [c for c in contours if self.shape_detector.is_puzzle(c)]

        for contour in contours:
            cv2.drawContours(img, [contour], 0, CONTOUR_COLOR, CONTOUR_WIDTH)

        x, y, _ = img.shape
        self.show(thresh, "Thresh IMG", pos=(x * 2, 0))
        self.show(img, "Contours", pos=(0, y))

    def get_key(self):
        return self.key
