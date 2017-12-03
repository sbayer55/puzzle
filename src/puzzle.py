"""Module to recognise puzzle peaces
"""

import cv2

SAVE_VIDEO = False

CAPURE_SCALE = 0.25
RENDER_SCALE = 4.0
WIDTH = int(640 * CAPURE_SCALE)
HEIGHT = int(480 * CAPURE_SCALE)
FPS = 4


def text(img, str_list):
    y = 24
    for s in str_list:
        cv2.putText(
            img=img,
            text=s,
            org=(10, y),
            fontFace=font,
            fontScale=0.6,
            color=(255,),
            thickness=2,
            lineType=cv2.LINE_AA,
        )
        y += 24

def render(img):
    global RENDER_SCALE

    img = cv2.resize(
        img,
        None,
        fx=RENDER_SCALE,
        fy=RENDER_SCALE,
        interpolation=cv2.INTER_CUBIC,
    )

    cv2.imshow('frame', img)

def on_keypress(key):
    global RENDER_SCALE
    global is_running

    if key == ord("q"):
        is_running = False
    elif key == ord("w"):
        RENDER_SCALE -= 0.1
    elif key == ord("e"):
        RENDER_SCALE += 0.1

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier("./resources/haarcascade_frontalface_alt.xml")
font = cv2.FONT_HERSHEY_SIMPLEX
is_running = True

if SAVE_VIDEO:
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, FPS, (WIDTH, HEIGHT))

cap.set(cv2.CAP_PROP_FPS, FPS)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

while cap.isOpened() and is_running:
    ret, frame = cap.read()
    str_list = list()

    if ret:
        frame = cv2.flip(frame, 1)

        if SAVE_VIDEO:
            out.write(frame)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for x, y, w, h in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)


        # str_list.append("Shape: {}".format(gray.shape))
        # str_list.append("Scale: {}".format(RENDER_SCALE))
        # text(gray, str_list)

        render(frame)

        key = cv2.waitKey(1) & 0xFF
        on_keypress(key)

cap.release()
cv2.destroyAllWindows()
