from __future__ import division
import random
import math
import numpy
from scipy.spatial.distance import cdist
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split


from .RFBNN_core import *
from .PSO_RFBNN import *
from .Training_Data import *

import matplotlib.pyplot as plt

import os

# Get the absolute path to the current file's directory (RFBNNPSO folder)
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, 'Data.csv')

# Use this path in readData
data = readData(data_path)
keys = data[0]
values = data[1]



xtrain, xtest, ytrain, ytest = train_test_split(keys, values, train_size=0.90)


def randX0(particles, length):
    x0list = []
    for i in range(0, particles):
      x0 = []
      for _ in range(0, length):
        x0.append(random.random())
      x0list.append(x0)
    print(x0list)
    return x0list

def fitnessFunction(position):
    model = fitness_model(position, xtrain, ytrain)
    return calculate_fit(model, xtrain, ytrain)

print(len(randX0(numParticles, dims)[0]))



model = PSOModel(randX0(numParticles, dims), bounds, fitnessFunction, maxiter=numIter)
convergence = model.begin()

FinalModel = fitness_model(model.posbestgroup, xtrain, ytrain)


print("MAE:", MAE(FinalModel, xtest, ytest))
print("RMSE:", RMSE(FinalModel, xtest, ytest))
print("MAPE:", MAPE(FinalModel, xtest, ytest))
print("R2", R2(FinalModel, xtest, ytest))

l = []
for arr in list(FinalModel.centres):
    l2 = (list(arr))
    l3 = []
    for ele in l2:
        l3.append(round(ele, 3))
    l.append(l3)


##
# print("Centers:", l)
# print("Weights:", list(FinalModel.weights))
# print("Betas:", FinalModel.inputBetas)

# Normalize input function
def normalize_inputs(inputs, mins, maxes):
    normalized_list = []
    for i in range(len(inputs)):
        # Normalization formula
        val = (inputs[i] - mins[i]) / (maxes[i] - mins[i])
        normalized_val = 2.0 * val - 1.0
        normalized_list.append(normalized_val)
    return normalized_list

# Deformalize output function
def denormalize_output(value, ref_min, ref_max):
    # Denormalization formula
    denorm_val = (value * 0.5) * (ref_max - ref_min) + ((ref_max + ref_min) / 2.0)
    # Ensure output is non-negative
    return max(denorm_val, 0.0)


def get_output(inputs):

    denorm_list_mins = [1990.33, 455366.67, -874000000.0, -9900333333.33, -9940666666.67, -128177000000.0, 19650.0, 455366.67, 4266.67, -1.22, -4933833333.33, -23491.33, -5614833333.33, -15534783333.33, 95548.0, 2282420447.49, 2939534754.37, -27477601550.27]
    denorm_list_maxes = [2027.67, 612433.33, 134982000000.0, 398942333333.33, 412848666666.67, 962311000000.0, 56850.0, 612433.33, 35733.33, 12.52, 42536833333.33, 1602679.33, 99079833333.33, 233222683333.33, 365692.0, 31129939936.07, 137944637892.23, 495624800221.47]
    denorm_ref_min = -28546333333.33
    denorm_ref_max = 761792333333.33

    # Normalize inputs
    normalized_inputs = normalize_inputs(inputs, denorm_list_mins, denorm_list_maxes)
    print("Normalized Inputs:", normalized_inputs)

    # flist = normalized_inputs
    normalized_output = FinalModel.predict(normalized_inputs)
    print("Predicted for 2024 (normalized):", normalized_output)

    # Denormalize output
    denormalized_output = denormalize_output(normalized_output, denorm_ref_min, denorm_ref_max)
    print("Denormalized Output:", denormalized_output)
    
    return denormalized_output

#
# testlist = [0.696, 0.360, 0.178, 0.595, 0.745, 0.673, 0.266, 0.368, 0.528, 0.750, 0.395, 0.255, 0.340, 0.552, 0.652, 0.382, 0.458, 0.545]
# testlist2 = [0.804, 0.290, 1.423, 0.818, 0.846, -0.763, -0.094, 64.089, 1.006, -0.328, -0.121, 0.751, 0.356, 3.717, 2.054, 1.027, 1.100, 0.890]
# print("Test List:", FinalModel.predict(xtest[0]), ytest[0])
# print("Also Test/Train List:", FinalModel.predict(testlist), 0.517)
# print("Out of range:", FinalModel.predict(testlist2), 0.75)


########### PLOTTING ###################

# PlotY = convergence
# PlotX = range(1, len(PlotY) + 1)

# plt.plot(PlotX, PlotY)
# plt.xlabel("Iteration Number")
# plt.ylabel("Compound error (MAE + MAPE + RMSE)")
# plt.title("RFBN-PSO Convergence Curve")
# plt.show()

