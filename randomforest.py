#https://www.kaggle.com/manikg/training-svm-classifier-with-hog-features

import numpy as np
import os
import cv2
from PIL import Image
from matplotlib import pyplot as plt
from skimage import color, transform
from skimage.feature import hog
from sklearn import svm
from sklearn.metrics import classification_report,accuracy_score

input_folder = "/Users/hiimanthonyc/Documents/test2"

name_dict = {0: 'ColdTaiga', 1: 'IceMountains', 2: 'IcePlains'}
predictions = []

labels = []
hog_images = []
hog_features = []
for filename in os.listdir(input_folder):
    if (filename != ".DS_Store"):
        curr_dir = input_folder + '/'+ filename
        for images in os.listdir(curr_dir):
            img = cv2.imread(curr_dir + '/' + images)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.resize(img, (150, 150))
            fd,hog_image = hog(img, orientations=8, pixels_per_cell=(16,16),cells_per_block=(1, 1),block_norm= 'L2',visualize=True)
            hog_images.append(hog_image)
            labels.append(filename)
            hog_features.append(fd)
#            plt.imshow(hog_image)
#            plt.show()
    
clf = svm.SVC()
labels = np.array(labels)
print(labels.shape)
hog_features = np.array(hog_features)
print(hog_features.shape)
data_frame = np.hstack((hog_features,labels))
np.random.shuffle(data_frame)

partition = int(len(hog_features)*.75)

x_train, x_test = data_frame[:partition,:-1],  data_frame[partition:,:-1]
y_train, y_test = data_frame[:partition,-1:].ravel() , data_frame[partition:,-1:].ravel()

clf.fit(x_train,y_train)

y_pred = clf.predict(x_test)

print("Accuracy: "+str(accuracy_score(y_test, y_pred)))
print('\n')
print(classification_report(y_test, y_pred))
