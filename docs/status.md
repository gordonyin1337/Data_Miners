---
layout: default
title: Status
---

Status Report
===

### Project Summary:
The goal of our project is to classify Minecraft biomes using a Convolutional Neural Network and screenshots of the game as training and input data. This is a computer vision and image classification project that is not only able to print out the biome a Malmo agent is spawned in, but also compares a baseline SVM classification algorithm to a more advanced Convolutional Neural Network.

### Approach:
To gather image data for training our classification algorithms, we run a Malmo mission in which the agent spawns in a single biome, and teleports to 100 different locations using "tp" commands and a random number generator and takes 8 screenshots while spinning around. For our screenshot script, we used the modules win32gui, win32ui, ctypes, and PIL. It uses win32gui to locate the active Minecraft application and get its dimensions of the bounding rectangle. It then retrieves its device context and making a replica, making it compatible specifically to Minecraft. It then creates a bitmap with the device context as well as the dimensions. It then prints the window into the device context and creates an image using the bitmap information. If an image has been successfully created, it will be saved as a jpg file in the same directory as the script. After the mission, there is a total of 800 screenshots per biome to train with, separated into their own directories. 

(ADD LIBRARIES FOR SVM AND PARAMETERS FOR BASELINE)
(ADD LIBRARIES FOR CNN AND PARAMETERS USED, FUNCTIONS, RECTIFIERS, EVERYTHING YOU CAN THINK OF)

### Evaluation:
For our quantitiative evaluation, we compare the accuracy of our baseline classification algorithm and our Neural Network for training and test data. With a 75/25 split for training and test data, our baseline achieves an accuracy of (ACCURACY) and our CNN achieves an accuracy of (ACCURACY) on the test data. The Neural Network is (SLIGHTLY/SIGNIFICANTLY) more accurate than the baseline according to this data. These are the plots of both classification algorithms’ accuracy:

(PLOTS AND GRAPHS OF BOTH CLASSIFIERS)

For our qualitative evaluation, we use our working test model within Malmo. The agent randomly chooses between the biomes that the Neural Network was trained on, and is spawned in a random location within that one biome Minecraft world. The agent then gathers input data similarly to how we gathered the training data: the agent spins around in a 360 degree circle and takes 8 screenshots of the game. Our classifier then classifies these 8 screenshots and picks the highest occurring classification, then prints its guess to the Minecraft chat bar. We can evaluate the accuracy of its guess by pressing “F3” within the Minecraft game to bring up the debug menu, which contains the biome information.

![](images/WorkingModel.png)

### Remaining Goals and Challenges:

### Resources Used:
