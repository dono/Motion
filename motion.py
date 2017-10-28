#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import time
import datetime
import os


device = 0
threshold = 30


# event() is executed when a moving object is detected.
def event():
    pass


# frame_diff() use Frame Difference Method and return True when moving objects are detected.
def frame_diff(images):
    # Grayscale image list.
    gray_images = [cv2.cvtColor(im, cv2.COLOR_RGB2GRAY) for im in images]

    diff1 = cv2.absdiff(gray_images[0], gray_images[1])
    diff2 = cv2.absdiff(gray_images[1], gray_images[2])

    intersection = cv2.bitwise_and(diff1, diff2)

    # Binarization.
    _, mask = cv2.threshold(intersection, threshold, 255, cv2.THRESH_BINARY)

    # Remove salt-and-pepper noize; kernel size is 7.
    mask = cv2.medianBlur(mask, 7)

    if np.any(mask):
        return True

    return False


if __name__ == '__main__':
    cam = cv2.VideoCapture(device)
    images = [cam.read()[1] for _ in range(3)]

    while cam.isOpened():
        if frame_diff(images):
            event()

        images[0] = images[1]
        images[1] = images[2]
        _, images[2] = cam.read()
