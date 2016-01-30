# Import the modules
import cv2
from sklearn.externals import joblib
from sklearn import datasets
from skimage.feature import hog
from sklearn.svm import *
import numpy as np
from collections import Counter
from skimage import io
import os
from PIL import Image, ImageChops
from matplotlib import pyplot as plt

# features = []
# labels = []

# Go into each directory in alphadata
# images = io.imread_collection('alphadata/Sample011/*.png')

letter_image_features = []#np.array([])
labels = [] #np.array([])

imagedir = "alphadata"

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


for subdir, dirs, files in os.walk(imagedir):
    print subdir
    
    for f in files:
        if not f.startswith('.'):
            imagepath= os.path.join(subdir, f)
            curImage = Image.open(imagepath)

            curImage2 = trim(curImage)
            img_w2, img_h2 = curImage2.size
            max_Size = max(img_w2, img_h2)
            max_Size = int(max_Size * 1.5)
            
            # Expands the image to 1200 x 1200 by pasting it onto the center of a new canvas
            curImageCropped = Image.new('RGBA', (max_Size, max_Size), (255, 255, 255, 255))
            bg_w, bg_h = curImageCropped.size
            img_w, img_h = curImage2.size
            offset = ((bg_w - img_w) / 2, (bg_h - img_h) / 2)
            curImageCropped.paste(curImage2, offset)

            # Resizes the image to 28 x 28
            size = 28, 28
            curImageCropped.thumbnail(size, Image.ANTIALIAS)

            curImageCroppednp_pre = np.asarray(curImageCropped)
            curImageCroppednp = 255 - curImageCroppednp_pre

            # Run image through filter
            im_gray = cv2.cvtColor(curImageCroppednp, cv2.COLOR_BGR2GRAY)
            # im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)

            # plt.imshow(im_gray)
            # plt.show()

            letter_image_features.append(im_gray)

            if subdir == imagedir + "/Sample011": # if we're looking at 'A'
                labels.append("A")

            if subdir == imagedir + "/Sample012":
                labels.append("B")

            if subdir == imagedir + "/Sample013":
                labels.append("C")

            if subdir == imagedir + "/Sample014":
                labels.append("D")

            if subdir == imagedir + "/Sample015":
                labels.append("E")

            if subdir == imagedir + "/Sample016":
                labels.append("F")

            if subdir == imagedir + "/Sample017":
                labels.append("G")

            if subdir == imagedir + "/Sample018":
                labels.append("H")
            if subdir == imagedir + "/Sample019":
                labels.append("I")
            if subdir == imagedir + "/Sample020":
                labels.append("J")
            if subdir == imagedir + "/Sample021":
                labels.append("K")
            if subdir == imagedir + "/Sample022":
                labels.append("L")
            if subdir == imagedir + "/Sample023":
                labels.append("M")
            if subdir == imagedir + "/Sample024":
                labels.append("N")
            if subdir == imagedir + "/Sample025":
                labels.append("O")
            if subdir == imagedir + "/Sample026":
                labels.append("P")
            if subdir == imagedir + "/Sample027":
                labels.append("Q")
            if subdir == imagedir + "/Sample028":
                labels.append("R")
            if subdir == imagedir + "/Sample029":
                labels.append("S")
            if subdir == imagedir + "/Sample030":
                labels.append("T")
            if subdir == imagedir + "/Sample031":
                labels.append("U")
            if subdir == imagedir + "/Sample032":
                labels.append("V")
            if subdir == imagedir + "/Sample033":
                labels.append("W")
            if subdir == imagedir + "/Sample034":
                labels.append("X")
            if subdir == imagedir + "/Sample035":
                labels.append("Y")
            if subdir == imagedir + "/Sample036":
                labels.append("Z")

        # np.append(letter_image_features, im_gray)
        # np.append(labels, "A")

        # imagename = imagepath.split("/")[2]
        # curImageCropped.save("processed_alpha_test/" + imagename)

# Crop images to 900 x 900
# img2 = curImage.crop((0, 0, 900, 900))
# img2.save("processed_alpha_test/img_a.png")

# Save image > matrix


# Save label

list_hog_fd = []
for feature in letter_image_features:
    print "feature", feature
    fd = hog(feature.reshape((28, 28)), orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
    list_hog_fd.append(fd)
hog_features = np.array(list_hog_fd, 'float64')

print "Count of digits in dataset", Counter(labels)

# Create an linear SVM object
clf = LinearSVC()

# Perform the training
clf.fit(hog_features, labels)

# Save the classifier
joblib.dump(clf, "digits_cls_alpha7.pkl", compress=3)


# LATER:
# [o] First goal: binary classifier for letter 'A'
# [o] might want to preprocess images


# images[0].reshape((30,30))


# Load the dataset
# dataset = datasets.fetch_mldata("MNIST Original")

# # Extract the features and labels
# features = np.array(dataset.data, 'int16') # image represented as numbers
# labels = np.array(dataset.target, 'int') # labels for images [0,1,2,3,4,5]

# # Extract the hog features
# list_hog_fd = []
# for feature in features:
#     fd = hog(feature.reshape((28, 28)), orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
#     list_hog_fd.append(fd)
# hog_features = np.array(list_hog_fd, 'float64')

# print "Count of digits in dataset", Counter(labels)

# # Create an linear SVM object 
# clf = LinearSVC()

# # Perform the training
# clf.fit(hog_features, labels)

# # Save the classifier
# joblib.dump(clf, "alpha_cls.pkl", compress=3)