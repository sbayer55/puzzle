import cv2

FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.6
FONT_THICKNESS = 2
FONT_LINE_TYPE = cv2.LINE_AA
DEFAULT_FONT_COLOR = (255, 255, 255)
DEFAULT_TEXT_POS = (0, 20)

def label(img, text, pos=DEFAULT_TEXT_POS, color=DEFAULT_FONT_COLOR):
    cv2.putText(
        img=img,
        text=text,
        org=pos,
        fontFace=FONT,
        fontScale=0.6,
        color=DEFAULT_FONT_COLOR,
        thickness=FONT_THICKNESS,
        lineType=FONT_LINE_TYPE,
    )

def labels(img, texts, color=DEFAULT_FONT_COLOR):
    x = 10
    y = 10
    for text in texts:
        text(img, text, x, y, color)
        y += 24

def label_contour(img, contour, text, color=DEFAULT_FONT_COLOR):
    M = cv2.moments(contour)

    try:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    except ZeroDivisionError as e:
        cX = 0
        cY = 0

    cv2.putText(
        img=img,
        text=text,
        org=(cX, cY),
        fontFace=FONT,
        fontScale=0.6,
        color=DEFAULT_FONT_COLOR,
        thickness=FONT_THICKNESS,
        lineType=FONT_LINE_TYPE,
    )