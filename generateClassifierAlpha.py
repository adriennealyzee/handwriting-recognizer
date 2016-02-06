# Import the modules
import cv2
from sklearn.externals import joblib
from sklearn import datasets
from skimage.feature import hog
from sklearn.svm import LinearSVC
import numpy as np
from collections import Counter
from skimage import io
import os
from PIL import Image

# features = []
# labels = []

# Go into each directory in alphadata
# images = io.imread_collection('alphadata/Sample011/*.png')

letter_image_features = []#np.array([])
labels = [] #np.array([])

imagedir = "alphadata"


for subdir, dirs, files in os.walk(imagedir):
    print subdir
    if subdir == imagedir + "/Sample011": # if we're looking at 'A'
        for f in files:
            imagepath= os.path.join(subdir, f)
            curImage = Image.open(imagepath)

            curImageCropped = curImage.crop((0, 0, 900, 900))

            size = 28, 28
            curImageCropped.thumbnail(size, Image.ANTIALIAS)

            curImageCroppednp = np.asarray(curImageCropped)
            im_gray = cv2.cvtColor(curImageCroppednp, cv2.COLOR_BGR2GRAY)
            im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)

            letter_image_features.append(im_gray)
            labels.append("A")

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
joblib.dump(clf, "digits_cls_alpha1.pkl", compress=3)


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