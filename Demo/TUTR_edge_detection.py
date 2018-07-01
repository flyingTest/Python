import cv2
import numpy as np

'''REFER: https://hub.packtpub.com/opencv-detecting-edges-lines-shapes/'''
'''Yonv1943 2018-06-30 23:00:14'''


def draw_contours(img, cnts):  # conts = contours
    img = np.copy(img)
    img = cv2.drawContours(img, cnts, -1, (0, 255, 0), 2)
    return img


def draw_min_rect_circle(img, cnts):  # conts = contours
    img = np.copy(img)
    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  # blue

        min_rect = cv2.minAreaRect(cnt)  # min_area_rectangle
        min_rect = np.int0(cv2.boxPoints(min_rect))
        cv2.drawContours(img, [min_rect], 0, (0, 255, 0), 2)  # green

        (x, y), radius = cv2.minEnclosingCircle(cnt)
        center, radius = (int(x), int(y)), int(radius)  # center and radius of minimum enclosing circle
        img = cv2.circle(img, center, radius, (0, 0, 255), 2)  # red
    return img


def draw_approx_hull_polygon(img, cnts):
    # img = np.copy(img)
    img = np.zeros(img.shape, dtype=np.uint8)
    for cnt in cnts:
        img = cv2.drawContours(img, cnts, -1, (255, 0, 0), 2)  # blue

        epsilon = 0.02 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        cv2.polylines(img, [approx, ], True, (0, 255, 0), 2)  # green

        hull = cv2.convexHull(cnt)
        cv2.polylines(img, [hull, ], True, (0, 0, 255), 2)  # red
    return img


def run():
    image = cv2.imread('test.png')

    # ret, thresh = cv2.threshold(cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)
    thresh = cv2.Canny(image, 128, 256)

    thresh, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    """
    print("hierarchy:", hierarchy)
    hierarchy: [[[1, -1, -1, -1],
                 [2,  0, -1, -1],
                 [3,  1, -1, -1],
                 [-1, 2, -1, -1],]]
    """

    imgs = [
        image, thresh,
        draw_min_rect_circle(image, contours),
        draw_approx_hull_polygon(image, contours),
    ]

    for img in imgs:
        cv2.imwrite("%s.jpg" % id(img), img)
        cv2.imshow("contours", img)
        cv2.waitKey(1234)


if __name__ == '__main__':
    run()
pass
