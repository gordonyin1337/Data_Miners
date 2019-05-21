from keras.models import load_model
import numpy as np
from PIL import Image
from skimage import transform
import os


def classify(model_name,input_folder):
    model = load_model(model_name)
    predictions = []
    for filename in os.listdir(input_folder):
        image = Image.open(input_folder + '/' + filename)
        image = np.array(image).astype('float32') / 255
        image = transform.resize(image, (150, 150, 3))
        image = np.expand_dims(image, axis=0)
        result = model.predict_classes(image)[0]
        predictions.append(result)
    return predictions


def main():
    model_name = 'conv_network.h5' #this should be the same
    input_folder = 'C:/test' #change this to your own location
    predictions = classify(model_name,input_folder)
    print(predictions)


main()



