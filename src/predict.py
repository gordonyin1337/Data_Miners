from keras.models import load_model
import numpy as np
from PIL import Image
from skimage import transform
import os


def predict(model_name,input_folder):
    model = load_model(model_name)
    name_dict = {0: 'Beach', 1: 'BirchForest', 2: 'BirchForestHills', 3:'ColdBeach', 4: 'ColdTaiga',
                 5: 'ColdTaigaHills', 6: 'Desert', 7: 'DesertHills', 8: 'ExtremeHills', 9: 'Forest', 10: 'ForestHills', 
                 11: 'IceMountains', 12: 'IcePlains', 13: 'Jungle', 14: 'JungleHills', 15:'MegaTaiga', 16: 'MegaTaigaHills', 
                 17: 'Mesa', 18: 'MushroomIsland', 19: 'Plains', 20: 'RoofedForest', 21: 'Savanna', 22: 'SavannaPlateau', 
                 23: 'StoneBeach', 24: 'Swampland', 25: 'Taiga', 26: 'TaigaHills'}
    predictions = []
    for filename in os.listdir(input_folder):
        image = Image.open(input_folder + '/' + filename)
        image = np.array(image).astype('float32') / 255
        image = transform.resize(image, (150, 150, 3))
        image = np.expand_dims(image, axis=0)
        result = model.predict_classes(image)[0]
        predictions.append(result)
    print(predictions)

    max_occurrence = max(predictions, key=predictions.count)
    return name_dict[max_occurrence]


def main():
    model_name = 'conv_network.h5' #this should stay the same
    input_folder = "C:\\Malmo2\\CS175_Homework\\Data_Miners\\src\\Test" #change this to your own location
    biome_prediction = predict(model_name,input_folder)
    print(biome_prediction)





