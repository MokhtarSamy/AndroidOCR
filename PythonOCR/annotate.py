input = [
    [[[2879.0, 365.0], [3398.0, 57.0], [3466.0, 177.0], [2946.0, 485.0]], ("UniveRsi", 0.8513504862785339)],
    [[[1482.0, 894.0], [2944.0, 288.0], [3031.0, 507.0], [1569.0, 1113.0]], ("I WosKaFFhe ", 0.8089697957038879)],
    [[[1688.0, 1217.0], [2376.0, 1041.0], [2441.0, 1307.0], [1753.0, 1483.0]], ("Hello", 0.9300691485404968)],
    [[[2435.0, 1268.0], [3120.0, 1206.0], [3138.0, 1421.0], [2454.0, 1483.0]], ("Univesity", 0.947674036026001)],
    [[[1933.0, 1533.0], [2222.0, 1502.0], [2280.0, 2080.0], [1990.0, 2110.0]], ("Work", 0.6628354787826538)],
    [[[2738.0, 1701.0], [3570.0, 1743.0], [3556.0, 2019.0], [2725.0, 1977.0]], ("Weanesday", 0.9160200953483582)],
    [[[1318.0, 2330.0], [2746.0, 2202.0], [2765.0, 2421.0], [1336.0, 2548.0]], ("my name is yamn", 0.9382486343383789)],
    [[[2304.0, 2560.0], [3158.0, 2612.0], [3143.0, 2874.0], [2289.0, 2822.0]], ("Something", 0.9717532396316528)],
]


import cv2
import numpy as np
import math


def addText(x, y, a, size, txt, src):
    height, width, _ = src.shape
    img = np.zeros((height, width, 3), dtype=np.uint8)

    # Draw the text using cv2.putText()
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, txt, (x, y), font, size, (0, 0, 255), 5)

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


def add_annotations(img):
    for i in input:
        (p0, p1, p2, p3) = i[0]
        (txt, _) = i[1]

        a = ang([mid(p0, p3), mid(p1, p2)], [[0, 0], [100, 0]])

        if math.dist(p0, p1) < math.dist(p1, p2):
            a = 360 - ang([mid(p0, p1), mid(p2, p3)], [[0, 0], [100, 0]])

        addText(int(p0[0]), int(p0[1]), a, 5, txt, img)


img = cv2.imread("IMG_2999.jpg")
add_annotations(img)
cv2.imwrite("img.png", img)
