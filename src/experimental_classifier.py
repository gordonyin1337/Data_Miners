import numpy as np
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation
from keras import applications
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras import backend as K

def create_h5():
    img_width, img_height = 150, 150
    train_data_dir = 'C:\MinecraftFiles' #replace this with your own directory for pictures
    nb_train_samples = 7800
    nb_validation_samples = 2600
    batch_size = 16

    train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        validation_split=.25)

    #reads images in from the directory, the "subset" parameters automatically splits the data
    train_generator = train_datagen.flow_from_directory(
        train_data_dir,  # this is the target directory
        target_size=(150, 150),  # all images will be resized to 150x150
        batch_size=batch_size,
        class_mode='categorical',
        subset='training',
        shuffle = 'true')

    validation_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(150, 150),
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation',
        shuffle = 'true')

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
    model.add(Dense(13, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# h saves history of classifier which is used for plotting
    H =model.fit_generator(
        train_generator,
        steps_per_epoch=7800 // batch_size,
        epochs=25,
        validation_data=validation_generator,
        validation_steps=2600 // batch_size)
    model.save('conv_network.h5')  #saves the model. once you have this file saved it's possible to open it somewhere else with keras


def main():
    create_h5()

main()