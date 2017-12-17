import sys
import cv2
import imutils
import logging
from time import sleep
from service.img_service import ImgService

INPUT_DEVICE = 0
INIT_PAUSE = 0.2
FPS = 30
FRAME_LENGTH = int(1000 / FPS)
SCALE = 0.5
WIDTH = int(1920 * SCALE)
HEIGHT = int(1080 * SCALE)


class Puzzle(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.logger.setLevel(logging.DEBUG)
        self.logger.disabled = False
        self.logger.filters = []
        
        stream_handler = logging.StreamHandler(stream=sys.stdout)
        stream_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(stream_handler)

        self.logger.debug("Puzzle.__init__()")

        self.img_service = ImgService(FRAME_LENGTH)
        self.running = False
        self.skipped_frames = 0
        self.key = 0
        self.text = "__init__"

    def run(self):
        self.logger.debug("Puzzle.run()")
        self.cap = cv2.VideoCapture(INPUT_DEVICE)
        self.cap.set(cv2.CAP_PROP_FPS, FPS)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

        self.logger.debug("Pausing for VideoCapture init")
        sleep(INIT_PAUSE)

        self.running = True
        self.loop()

    def stop(self):
        self.running = False

    def on_key(self, key):
        self.logger.debug("Puzzle.on_key()")

        self.key = key
        self.text = str(key)

        if key == 113:
            self.stop()
        elif key == 111:
            self.img_service.dynamic_value -= 1
        elif key == 112:
            self.img_service.dynamic_value += 1

    def on_frame(self, frame):
        self.logger.debug("Puzzle.onframe()")

        self.img_service.show(frame)
        self.img_service.isolate_puzzle(frame)

    def on_skipped_frame(self):
        self.logger.debug("Puzzle.on_skipped_frame()")
        self.skipped_frames += 1

        if self.skipped_frames > 10:
            self.running = False

    def loop(self):
        self.logger.debug("Puzzle.loop()")
        while self.running:
            self.logger.debug("Puzzle.loop() -> loop")

            if self.cap.isOpened():
                ret, frame = self.cap.read()

                if ret:
                    self.on_frame(frame)
                    self.on_key(self.img_service.get_key())
                else:
                    self.on_skipped_frame()
            else:
                self.logger.error("Unable to open video capture")
                self.stop()
        self.cap.release()
        cv2.destroyAllWindows()

puzzle = Puzzle()
puzzle.run()
