
import cv2
import numpy as np
import math

def addText(x, y, a, size, txt, src, points):
    (p0, p1, p2, p3) = points
    height, width, _ = src.shape
    img = np.zeros((height, width, 3), dtype=np.uint8)
    
    fontScale = int(abs(p3[1] - p0[1]))
    if math.dist(p0, p1) < math.dist(p1, p2):
        fontScale = int(abs(p1[0] - p0[0]))

    # Draw the text using cv2.putText()
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, txt, (x, y), font, cv2.getFontScaleFromHeight(cv2.FONT_HERSHEY_SIMPLEX, fontScale, 0)/2, (0, 0, 255), 5)

    # Rotate the image using cv2.warpAffine()
    M = cv2.getRotationMatrix2D((x, y), a, 1)
    s_img = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))

    y1, y2 = 0, height
    x1, x2 = 0, width

    alpha_s = s_img[:, :, 2] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        src[y1:y2, x1:x2, c] = alpha_s * s_img[:, :, c] + alpha_l * src[y1:y2, x1:x2, c]


def dot(vA, vB):
    return vA[0] * vB[0] + vA[1] * vB[1]


def ang(lineA, lineB):
    vA = [(lineA[0][0] - lineA[1][0]), (lineA[0][1] - lineA[1][1])]
    vB = [(lineB[0][0] - lineB[1][0]), (lineB[0][1] - lineB[1][1])]

    dot_prod = dot(vA, vB)

    magA = dot(vA, vA) ** 0.5
    magB = dot(vB, vB) ** 0.5

    angle = math.acos(dot_prod / magB / magA)
    ang_deg = math.degrees(angle) % 360

    if ang_deg - 180 >= 0:
        return 360 - ang_deg
    else:
        return ang_deg


def mid(p1, p2):
    return [int((p1[0] + p2[0]) / 2), int((p1[1] + p2[1]) / 2)]


def add_annotations(img, input):
    txt_call = []
    for i in input:
        (p0, p1, p2, p3) = i[0]
        (txt, _) = i[1]

        if math.dist(p0, p1) < math.dist(p1, p2):
            s0, s1 = mid(p0, p1), mid(p2, p3)
            a = 360 - ang([s0, s1], [[0, 0], [100, 0]])
        else:
            s0, s1 = mid(p0, p3), mid(p1, p2)
            a = ang([s0, s1], [[0, 0], [100, 0]])

        box = np.int0(i[0])
        cv2.drawContours(img, [box], 0, (200, 200, 200, 0.5), thickness=cv2.FILLED)

        txt_call.append((s0[0], s0[1], a, 5, txt, img))

    for (x, y, a, size, txt, img) in txt_call:
        addText(x, y, a, size, txt, img, i[0])