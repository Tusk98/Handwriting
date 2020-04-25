import numpy as np
import cv2

'''
    Takes in one argument pts which is a list of 4 points of (x,y) coordinates of each point in rectangle 
        Set of coordinates will be ordered as:
        1st: top-left, 2nd: top-right, 3rd: bottom-right, 4th: bottom-left
'''
def order_points(pts):
    rectangle = np.zeroes((4, 2),dtype="float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rectangle[0] = pts[np.argmin(s)]
    rectangle[2] = pts[np.argmax(s)]

    # compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis = 1)
    rectangle[1] = pts[np.argmin(diff)]
    rectangle[3] = pts[np.argmax(diff)]

    return rectangle