#!/usr/bin/env python
# coding: utf-8

# In[11]:


import numpy as np
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation
from keras import applications
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras import backend as K


# In[12]:


img_width, img_height = 150, 150
train_data_dir = 'C:\MinecraftFiles' #replace this with your own directory for pictures
nb_train_samples = 2400
nb_validation_samples = 600
epochs = 50 #number of passes over the data, can be set to less or more. Accuracy of .66 seems to be the limit after around ~40
batch_size = 16


# In[13]:


train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        validation_split=.25)


# In[14]:


#reads images in from the directory, the "subset" parameters automatically splits the data
train_generator = train_datagen.flow_from_directory(
        train_data_dir,  # this is the target directory
        target_size=(150, 150),  # all images will be resized to 150x150
        batch_size=batch_size,
        class_mode='binary',
        subset='training')  

validation_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(150, 150),
        batch_size=batch_size,
        class_mode='binary',
        subset='validation')


# In[15]:


#these are the parameters we could try changing to get better results, things such as adding additional convolution layers.
if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])


# In[ ]:


model.fit_generator(
        train_generator,
        steps_per_epoch=1600 // batch_size,
        epochs=50,
        validation_data=validation_generator,
        validation_steps=600 // batch_size)
model.save_weights('first_try.h5')  #saves the model. once you have this file saved it's possible to open it somewhere else with keras


# In[ ]:





# In[ ]:




