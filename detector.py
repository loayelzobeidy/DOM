import cv2
import numpy as np
import matplotlib
from matplotlib.pyplot import imshow
from matplotlib import pyplot as plt

from fuzzy_controller import get_action

def select_white(image):
    lower = np.uint8([230])
    upper = np.uint8([255])
    white_mask = cv2.inRange(image, lower, upper)

    masked = cv2.bitwise_and(image, image, mask=white_mask)
    return masked

def highlight_track(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    height, width = gray.shape

    top = int(height*0.20)
    top_mask = np.ones((height, width), np.uint8)
    top_mask[0:top,:] = 0

    masked = cv2.bitwise_and(gray, gray, mask=top_mask)

    kernel_size = 9
    blur_gray = cv2.GaussianBlur(masked, (kernel_size, kernel_size), 0)

    white_img = select_white(blur_gray)

    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(white_img, low_threshold, high_threshold)

    kernel = np.ones((5,5),np.uint8)
    dialated = cv2.dilate(edges, kernel, iterations=1)

    return dialated

def calculate_weight(img):
    height, width = img.shape
    centerh = int(width/2)
    centerw = int(width/2)
    left = 0
    right = 0
    up = 0
    down = 0
    for i in range(height):
        for j in range(width):
            if img[i][j] > 0:
                if j <= centerw:
                    left += 1
                else:
                    right += 1
                if i <= centerh:
                    up += 1
                else:
                    down += 1
    sum = 1.0*(left + right)
    if(sum > 0):
        return (left/sum, right/sum, up/sum, down/sum)
    else:
        return (0,0,0,0)

def get_score(img):
    height, width, _ = img.shape
    fx = 250 / width
    fy = 250 / height
    img = cv2.resize(img, (0,0), fx=fx, fy=fy)

    result = highlight_track(img)

    wl, wr, wu, wd = calculate_weight(result)
    outputh = int((wr-wl)*100)
    outputv = int((wu-wd)*100)

    # cv2.imshow("After", result)
    # cv2.waitKey(0)

    return (outputh, outputv)


if __name__ == '__main__':
    for i in range(1, 11):
        print('track_images/{}.jpg'.format(i))
        img = cv2.imread('track_images/{}.jpg'.format(i))

        outputh, outputv = get_score(img)

        action = int(get_action(outputh, outputv))

        if action == 1:
            action = 'LEFT'
        elif action == 2:
            action = 'FORWARD'
        elif action == 3:
            action = 'RIGHT'

        #print('vertical: {} horizontal: {}'.format(outputv, outputh))
        print('action: {}'.format(action))
        print()
