# Import the modules
import cv2
from sklearn.externals import joblib
from skimage.feature import hog
import numpy as np
from PIL import Image

# Load the classifier
clf = joblib.load("digits_cls_alpha6.pkl")

# Read the input image 
im = cv2.imread("adrienne2b.jpg")
im_pil = Image.open("adrienne2b.jpg")

# Convert to grayscale and apply Gaussian filtering
im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)

# Threshold the image
ret, im_th = cv2.threshold(im_gray, 90, 255, cv2.THRESH_BINARY_INV)

# Find contours in the image
ctrs, hier = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Get rectangles contains each contour
rects = [cv2.boundingRect(ctr) for ctr in ctrs]

# store tuples of size 2 digit/alpha bounding boxes
# the two elements in the tuple represent the vertices of the bounding box on the image

digit_alphabet_bounding_boxes = []

# cropped_images = []

# For each rectangular region, calculate HOG features and predict
# the digit using Linear SVM.

for rect in rects:
    # Draw the rectangles
    cv2.rectangle(im, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 3) 

    v1 = (rect[0], rect[1])
    v2 = (rect[0] + rect[2], rect[1] + rect[3])

    # append bounding box
    # digit_alphabet_bounding_boxes.append((v1,v2))

    print "v1"
    print rect[0]
    print rect[1]
    print " - - - "
    print "v2"
    print rect[0] + rect[2]
    print rect[1] + rect[3]
    print " - - - "
    print "rect[0]", rect[0]
    print "rect[1]", rect[1]
    print "rect[2]", rect[2]
    print "rect[3]", rect[3]
    

    box = (rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3])
    digit_alphabet_bounding_boxes.append(box)

    # Make the rectangular region around the digit
    leng = int(rect[3] * 1.6)
    pt1 = int(rect[1] + rect[3] // 2 - leng // 2)
    pt2 = int(rect[0] + rect[2] // 2 - leng // 2)
    roi = im_th[pt1:pt1+leng, pt2:pt2+leng]
    # Resize the image
    roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
    roi = cv2.dilate(roi, (3, 3))
    # Calculate the HOG features
    roi_hog_fd = hog(roi, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
    nbr = clf.predict(np.array([roi_hog_fd], 'float64'))
    cv2.putText(im, str(nbr[0]), (rect[0], rect[1]),cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 255), 3)

    print "# # # # IDENTIFIED ITEM", str(nbr[0])
    # ^ ^ IDENTIFIED NUMBER = str(int(nbr[0]))

digit_alphabet_bounding_boxes2 = sorted(digit_alphabet_bounding_boxes, key=lambda x: x[0])

i=0
for item in digit_alphabet_bounding_boxes2:
    temp_region = im_pil.crop(item)
    temp_str = 'jeremy2region' + str(i)
    temp_region.save(temp_str, 'jpeg')
    i += 1


cv2.imshow("Resulting Image with Rectangular ROIs", im)
cv2.waitKey()




# input: Image
# output: number


