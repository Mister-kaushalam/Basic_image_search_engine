#importing necessary packages
import numpy as np
import cv2
import imutils

class HSVDescriptor:
    def __init__(self, bins):
        #store the number of bins for the histogram
        self.bins = bins

    def describe(self, image):
        #convert the image to HSV color space
        #initialize the features used to quantify the image

        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        features = []

        #grab the dimenstions and compute the center of the image
        (h, w) = image.shape[:2]
        (cX, cY) = (int(h * 0.5) , int(w * 0.5))

        #divide the image into four segments/ rectangle. This is done to compute local histogram of image rather than a global histogram
        #(top-left,top-right, bottom-right, bottom-left)
        segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h), (0, cX, cY, h)]

        #contruct an elliptical mask representing the center of the image
        (axesX, axesY) = (int(w * 0.75) // 2, int(h*0.75) // 2)
        ellipMask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)

        # loop over the segments
        for (startX, endX, startY, endY) in segments:
            # construct a mask for each corner of the image, subtracting
            # the elliptical center from it

            cornerMask = np.zeros(image.shape[:2], dtype="uint8")
            cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
            cornerMask = cv2.subtract(cornerMask, ellipMask)

            #extract the color histogram from the image, then update the feature vector
            hist = self.histogram(image, cornerMask)
            features.extend(hist)
        #extract the color histogram from the eliptical region and update the feature vector
        hist = self.histogram(image, ellipMask)
        features.extend(hist)

        #return the feature vector
        return np.array(features)

    def histogram(self, image, mask=None):
        # extract a 3D color histogram from the masked region of the
		# image, using the supplied number of bins per channel; then
		# normalize the histogram

        hist = cv2.calcHist([image], [0,1,2], mask, self.bins, [0,180, 0,256, 0,256])

        #handle if we are using opencv 2.4
        if imutils.is_cv2():
            hist = cv2.normalize(hist).flatten()
        else: # if we are using OpenCV 3+
            hist = cv2.normalize(hist, hist).flatten()

        return hist
