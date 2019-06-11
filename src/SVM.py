#https://www.kaggle.com/manikg/training-svm-classifier-with-hog-features

import numpy as np
import os
import cv2
from PIL import Image
from matplotlib import pyplot as plt
from sklearn.model_selection import learning_curve
from skimage import color, transform
from skimage.feature import hog
from sklearn import svm
from sklearn.metrics import classification_report,accuracy_score
from warnings import simplefilter

simplefilter(action='ignore', category=FutureWarning)

input_folder = "/Users/hiimanthonyc/Documents/MinecraftScreenshots"

labels = []
hog_images = []
hog_features = []
currentdir = 0
for filename in os.listdir(input_folder):
    if (filename != ".DS_Store"):
        curr_dir = input_folder + '/'+ filename
        for image in os.listdir(curr_dir):
            if (image != ".DS_Store"):
                img = cv2.imread(curr_dir + '/' + image)
                img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                img = cv2.resize(img, (150, 150))
                fd,hog_image = hog(img, orientations=8, pixels_per_cell=(16,16),cells_per_block=(1, 1),block_norm= 'L2',visualize=True)
                hog_images.append(hog_image)
                labels.append(currentdir)
                hog_features.append(fd)
    currentdir += 1
    
clf = svm.SVC()
labels = np.array(labels).reshape(len(labels),1)
hog_features = np.array(hog_features)
data_frame = np.hstack((hog_features,labels))
np.random.shuffle(data_frame)
partition = int(len(hog_features)*.75)
x_train, x_test = data_frame[:partition,:-1],  data_frame[partition:,:-1]
y_train, y_test = data_frame[:partition,-1:].ravel() , data_frame[partition:,-1:].ravel()

clf.fit(x_train,y_train)

train_sizes,train_scores, test_scores=learning_curve(clf,x_train,y_train)
train_scores_mean = np.mean(train_scores, axis=1)
test_scores_mean = np.mean(test_scores, axis=1)
plt.style.use("ggplot")
plt.figure()
plt.title("SVM Classifier")
plt.xlabel("Train Sizes")
plt.ylabel("Error Rate")

plt.plot(train_sizes,1-train_scores_mean,label="train error")
plt.plot(train_sizes,1-test_scores_mean,label="test error")
plt.legend()
plt.legend(loc="lower left")
plt.savefig("svmplot.png")
plt.show()

y_pred = clf.predict(x_test)

print("Accuracy: "+str(accuracy_score(y_test, y_pred)))
print(classification_report(y_test, y_pred))
