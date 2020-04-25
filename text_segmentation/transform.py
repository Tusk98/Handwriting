import numpy as np
import cv2
import argparse
import imutils

from skimage.filters import threshold_local

'''
    Takes in one argument pts which is a list of 4 points of (x,y) coordinates of each point in rectangle 
        Set of coordinates will be ordered as:
        1st: top-left, 2nd: top-right, 3rd: bottom-right, 4th: bottom-left
'''
def order_points(pts):
    rectangle = np.zeros((4, 2),dtype="float32")

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

def edge_detection(img):
    ### Edge detection ###
    # load image and compute ratio of old height to new height, then resize it
    image = cv2.imread(img)

    # Ratio of old height + original image
    ratio = image.shape[0] / 500.0
    og_img = image.copy()

    image = imutils.resize(image, height=500)

    # Convert image to grascale, then blur, to find edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)

    #cv2.imshow("Original: ", image)
    #cv2.imshow("Edged: ", edged)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return edged, og_img, ratio

def find_contours(edged):
    # Find contours in edged image, keep only largest ones
    conts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    conts = imutils.grab_contours(conts)

    # Get yo contours here
    conts = sorted(conts, key = cv2.contourArea, reverse=True)[:5]

    # Loop over contours, approximate the number of points in that contour
    screenCont = []
    print("AAA")
    for c in conts:
        # Approximate the contours
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        print("BBB")
        # If our contour has 4 points, assume we've found document
        if len(approx) == 4:
            print("CCC")
            screenCont = approx
            print("SCREENCONT: ", screenCont)
            break

    if screenCont == []:
        print("Unable to detect document in your image")
        exit()

    #cv2.drawContours(image, screenCont, -1, (0, 255, 0), 2)
    #cv2.drawContours(image, [screenCont], -1, (0,255,0),2)
    #cv2.imgshow("Outline", image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return screenCont

def warp_and_save(original, ratio):
    ### Perspective transform and threshold ###
    warped = four_point_transform(original, contours.reshape(4, 2) * ratio)

    # Convert warped to graysacle, then threshold it to give "black and white" effect
    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    T = threshold_local(warped, 11, offset=10, method="gaussian")
    warped = (warped > T).astype("uint8") * 255

    cv2.imwrite("result.jpg", imutils.resize(warped))


if __name__ == "__main__":
    # Argument parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required = True, help="Path to the image that's to be scanned")
    args = vars(ap.parse_args())

    # Pass through path to image to edge detection
    edged, og_img, ratio = edge_detection(args["image"])

    # Find contours
    contours = find_contours(edged)

    warp_and_save(og_img, ratio)
















