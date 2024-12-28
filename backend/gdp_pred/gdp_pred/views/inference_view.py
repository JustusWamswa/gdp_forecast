from django.http import JsonResponse
import json
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
# from ..RFBNNPSO.main import get_output

import math
import numpy as np

# Extension for Double (Python float already supports operations directly)
def squared(x):
    return x ** 2

# Squared Euclidean distance
def sqeuclidean(arr1, arr2):
    return sum((a - b) ** 2 for a, b in zip(arr1, arr2))

# Gaussian RBF
def gaussian_rbf(point1, point2, beta):
    return math.exp(-sqeuclidean(point1, point2) / (2 * (beta ** 2)))

class InputNeuron:
    def __init__(self, center, beta):
        self.center = center
        self.beta = beta

    def unweighted_activation(self, x):
        return gaussian_rbf(x, self.center, self.beta)

class InputLayer:
    def __init__(self, centers, betas):
        self.neurons = [InputNeuron(center, beta) for center, beta in zip(centers, betas)]

    def unweighted_activation(self, x):
        return [neuron.unweighted_activation(x) for neuron in self.neurons]

class HiddenNeuron:
    def __init__(self, weights):
        self.weights = weights

    def raw_activation(self, input_layer_activation):
        return sum(w * act for w, act in zip(self.weights, input_layer_activation))

class HiddenLayer:
    def __init__(self, weights_array):
        self.neurons = [HiddenNeuron(weights) for weights in weights_array]

    def raw_activations(self, input_layer_activation):
        return [neuron.raw_activation(input_layer_activation) for neuron in self.neurons]

class Output:
    def __init__(self, weights):
        self.weights = weights

    def compute(self, hidden_layer_outputs):
        return sum(w * output for w, output in zip(self.weights, hidden_layer_outputs))

class RFBN:
    def __init__(self, input_centers, input_betas, hidden_weights):
        self.input_centers = input_centers
        self.input_betas = input_betas
        self.hidden_weights = hidden_weights

    def predict(self, x):
        input_layer = InputLayer(self.input_centers, self.input_betas)
        input_layer_activation = input_layer.unweighted_activation(x)
        return sum(w * act for w, act in zip(self.hidden_weights, input_layer_activation))

# Constants
centres = [
    [0.616, 0.224, -0.322, -0.002, 0.152, 0.527, 0.648, 0.224, 0.693, -0.35, 0.036, -0.67, -0.576, 0.498, 0.514, -0.016, 0.134, 0.302],
    [0.054, 0.164, -0.394, -0.151, -0.026, -0.235, 0.225, 0.164, 0.199, -0.036, 0.04, 0.183, -0.116, -0.318, -0.362, -0.266, -0.037, -0.14],
    [-0.47, -0.378, -0.553, -0.549, -0.587, -0.736, -0.066, -0.378, -0.39, -0.007, -0.66, -0.211, -0.589, -0.638, -0.641, -0.609, -0.552, -0.611],
    [0.723, 0.559, 0.464, 0.672, 0.747, 0.712, 0.116, 0.559, 0.477, 0.474, 0.572, 0.438, 0.548, 0.651, 0.701, 0.566, 0.604, 0.648],
    [0.402, 0.636, -0.318, 0.136, 0.236, 0.107, 0.229, 0.636, 0.571, -0.51, 0.274, 0.584, 0.183, 0.09, 0.131, -0.139, 0.176, 0.284]
]
weights = [5.156660155498186, -41.57575045121054, 2.6660048651192625, 14.59634934369921, 19.426231831720173]
betas = [15.524714097531648] * 5
denorm_list_mins = [1990.33, 455366.67, -874000000.0, -9900333333.33, -9940666666.67, -128177000000.0, 19650.0, 455366.67, 4266.67, -1.22, -4933833333.33, -23491.33, -5614833333.33, -15534783333.33, 95548.0, 2282420447.49, 2939534754.37, -27477601550.27]
denorm_list_maxes = [2027.67, 612433.33, 134982000000.0, 398942333333.33, 412848666666.67, 962311000000.0, 56850.0, 612433.33, 35733.33, 12.52, 42536833333.33, 1602679.33, 99079833333.33, 233222683333.33, 365692.0, 31129939936.07, 137944637892.23, 495624800221.47]
denorm_ref_min = -28546333333.33
denorm_ref_max = 761792333333.33

model = RFBN(input_centers=centres, input_betas=betas, hidden_weights=weights)

@csrf_exempt
@require_POST
def get_inference(request):
    try:
        data = json.loads(request.body)
        inputs = data.get('inputs')
        # inputs = [1995,475000, 16108000000, 41205000000, 42908000000, 8134000000, 24300, 475000, 9800, 6, 1000000000, 422463, 7472000000, 15559900000, 129316, 6591338686, 19815172647, 37910198671, 70246000000]
        # output = get_output(inputs)
        normalized_inputs = [
            2 * ((val - min_val) / (max_val - min_val)) - 1
            for val, min_val, max_val in zip(inputs, denorm_list_mins, denorm_list_maxes)
        ]
        predicted_value = model.predict(normalized_inputs)

        denormalized_value = (
            predicted_value * 0.5 * (denorm_ref_max - denorm_ref_min)
            + ((denorm_ref_max + denorm_ref_min) / 2)
        )
        denormalized_value = max(0, denormalized_value)
        print(denormalized_value)
        return JsonResponse({'status': 'success', 'prediction': denormalized_value}, status=201)
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)