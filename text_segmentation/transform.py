import numpy as np
import cv2

'''
    Takes in one argument pts which is a list of 4 points of (x,y) coordinates of each point in rectangle 
        Set of coordinates will be ordered as:
        1st: top-left, 2nd: top-right, 3rd: bottom-right, 4th: bottom-left
'''
def order_points(pts):
    rectangle = np.zeroes((4, 2),dtype="float32")

    # the top-left point will have the smallest x + y sum
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rectangle[0] = pts[np.argmin(s)]
    rectangle[2] = pts[np.argmax(s)]

    # compute the difference (x - y) between the points
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis = 1)
    rectangle[1] = pts[np.argmin(diff)]
    rectangle[3] = pts[np.argmax(diff)]

    return rectangle

def four_point_transform(image, pts):
    # Order the image coordinates using helper function
    rectangle = order_points(pts)
    (top_left, top_right, bottom_right, bottom_left) = order_points(pts)

    # Determine width of new, transformed image using max distance between
    # either top or bottom set of coordinates
    widthBottom = np.sqrt(((bottom_right[0] - bottom_left[0]) ** 2) + ((bottom_right[1] - bottom_left[1]) ** 2))
    widthTop = np.sqrt(((top_right[0] - top_left[0]) ** 2) + ((top_right[1] + top_right[1])**2))
    new_width = max(int(widthBottom), int(widthTop))

    # Determine new height using similar technique but with right and left instead
    heightLeft = np.sqrt(((top_left[0] - bottom_left[0]) ** 2) + ((top_left[1] - bottom_left[1]) ** 2))
    heightRight = np.sqrt(((top_right[0] - bottom_right[0]) ** 2) + ((top_right[1] - bottom_right[1]) ** 2))
    new_height = max(int(heightLeft), int(heightRight))

    # Define our top-down view (the coordinates of the corners of our new image
    new_coords = np.array([
        [0, 0],                             # Top left corner
        [new_width - 1, 0],                 # Top right
        [new_width - 1, new_height - 1],    # Bottom right
        [0, new_height - 1]],               # Bottom left
        dtype="float32")

    # lol cv2 what is this even
    Matrix = cv2.getPerspectiveTransform(rectangle, new_coords)
    warped = cv2.warpPerspective(image, Matrix, (new_width, new_height))

    return warped