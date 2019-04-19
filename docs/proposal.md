---
layout: default
title: Proposal
---
Project Proposal
========

### Summary:
The main idea of our project is to implement a machine learning algorithm that can identify different biomes that exist in Minecraft and be able to tell which biome an agent is in based on the environment around them. Our Project should take a large number of randomly generated chunks as well as the biome type of each chunk as input for training, validation, and test data. From this it should be able to output a program that can identify the biome at the players current location based on the light percentage, animals, height and type of blocks, height of the agent, etc. within the area. An additional feature we may also implement is for the program to be able to navigate through the world until it encounters the next biome in a chosen direction when prompted by a command.

### AI/ML Algorithms:
We plan to use Machine Learning classification algorithms to classify biomes using input data from our generated worlds, and use path-finding algorithms and graph algorithms to navigate through the minecraft world and find a new biome.

### Evaluation Plan:
For the quantitative evaluation, the metric used will be the percentage of biomes guessed correctly and the Machine Learning algorithms AUC or MSE. The baseline to achieve that would be randomly guessing the biome that an agent is situated in, which should guess correctly about 2% of the time. In order to detail our progression and improvement regarding our approach, we hope to significantly increase the accuracy of biomes guessed correctly from the 2% of our baseline up to at least 50% accuracy. The data that will be evaluated includes the prediction accuracy of randomly generated worlds, the AUC algorithm to represent probability, as well as the test data at the end. 

The qualitative evaluation will simply be seeing our algorithm output the correct biome in a world it has never seen before, and then see our agent navigate to another biome. This could include both a prebuilt and preplanned world by us, and a default randomly generated world. After training our ML algorithm, we can plot and visualize its error rate with validation and test data. If our algorithm fails to improve, we can tweak parameters and look for improvement, or change our ML algorithm approach to a more appropriate one. Our moonshot case would be a ML algorithm that can detect biomes with 100% accuracy, and an agent that can efficiently navigate to a new biome in the world.
