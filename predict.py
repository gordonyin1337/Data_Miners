from keras.models import load_model
import numpy as np
from PIL import Image
from skimage import transform
import os


def classify(model_name,input_folder):
    model = load_model(model_name)
    my_dict = {0: 'ColdTaiga', 1: 'IceMountains', 2: 'IcePlains'}
    predictions = []
    for filename in os.listdir(input_folder):
        image = Image.open(input_folder + '/' + filename)
        image = np.array(image).astype('float32') / 255
        image = transform.resize(image, (150, 150, 3))
        image = np.expand_dims(image, axis=0)
        result = model.predict_classes(image)[0]
        predictions.append(result)

    max_occurrence = max(predictions, key=predictions.count)
    return my_dict[max_occurrence]


def main():
    model_name = 'conv_network.h5' #this should stay the same
    input_folder = 'C:/test' #change this to your own location
    biome_prediction = classify(model_name,input_folder)
    print(biome_prediction)


main()





