import numpy as np  # numpy must be installed in order to run
data_filename = "X_data.txt"
label_filename = "Y_data.txt"
with open(label_filename) as f:
    lines=f.readlines()
    for line in lines:
        labels = np.fromstring(line, dtype=int, sep=' ')  # creates numpy array

#print(label_data[152])  # verifies size of array

file = open(data_filename).read()
file = file.split(";")
file = file[:-1]

two_dim_list = []
for i in file:
    test = i.split(',')
    test = test[:-1]
    two_dim_list.append(test)

data = np.array(two_dim_list)

# variable "data" is a 2d numpy array with every block type for all 153 chunks
# variable "labels" is a numpy array with labels for all 153 chunks
