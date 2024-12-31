from django.http import JsonResponse
import json
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from numpy import *

import math

# Extension for Double (Python float already supports operations directly)
def squared(x):
    return x ** 2

# Squared Euclidean distance
def sqeuclidean(arr1, arr2):
    return sum((a - b) ** 2 for a, b in zip(arr1, arr2))

# Gaussian RBF
def gaussian_rbf(point1, point2, beta):
    return math.exp(-sqeuclidean(point1, point2) / (2 * (beta ** 2)))

class RFBN:
  def __init__(self, input_centers, input_betas, hidden_weights):
    self.input_betas = input_betas
    self.input_centers = input_centers
    self.hidden_weights = hidden_weights

  
  def hiddenLayerActivationMatrix(self, X): # X is an array of points, not a single one
    matrixlist = []
    for point in X:
      row = [gaussian_rbf(point, centre, self.input_betas[index]) for index, centre in enumerate(self.input_centers)]
      matrixlist.append(row)

    # Now, matrixlist is a 2-dimensional list
    return array(matrixlist) # This is the matrix of activations

  
  def predict(self, X):
    M = self.hiddenLayerActivationMatrix([X])
    return array((M @ self.hidden_weights).flat)[0]

# Constants
centres = [[-0.107, -0.042, -0.416, -0.27, -0.171, -0.359, 0.29, -0.042, 0.049, 0.507, -0.162, 0.105, -0.168, -0.446, -0.495, -0.316, -0.199, -0.295], [0.536, 0.727, -0.341, 0.167, 0.31, 0.284, 0.078, 0.727, 0.693, -0.75, 0.399, 0.73, 0.313, 0.454, 0.375, -0.085, 0.215, 0.425], [-0.536, -0.348, -0.579, -0.61, -0.608, -0.743, 0.04, -0.348, -0.451, 0.182, -0.75, -0.26, -0.632, -0.668, -0.685, -0.75, -0.611, -0.653], [0.589, 0.461, -0.337, -0.088, 0.036, 0.416, 0.75, 0.461, 0.75, -0.459, 0.024, -0.591, -0.555, 0.573, 0.461, -0.078, 0.041, 0.273], [0.214, 0.431, -0.343, 0.022, 0.152, -0.119, 0.361, 0.431, 0.394, -0.308, 0.301, 0.257, -0.07, -0.218, -0.187, -0.205, 0.072, 0.028], [0.348, 0.623, -0.284, 0.117, 0.196, 0.036, 0.328, 0.623, 0.538, -0.655, 0.063, 0.521, 0.12, -0.016, 0.03, -0.153, 0.155, 0.242], [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, -0.035, 0.75, 0.426, 0.197, 0.75, 0.622, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75], [-0.268, -0.16, -0.471, -0.498, -0.454, -0.722, 0.433, -0.16, -0.165, -0.182, -0.636, -0.072, -0.462, -0.542, -0.55, -0.531, -0.41, -0.499], [-0.696, -0.652, -0.716, -0.714, -0.714, -0.747, -0.544, -0.652, -0.708, 0.109, -0.75, -0.379, -0.723, -0.733, -0.738, -0.664, -0.718, -0.729], [0.107, 0.187, -0.362, -0.103, 0.059, -0.204, 0.239, 0.187, 0.191, 0.124, 0.059, 0.215, -0.077, -0.235, -0.305, -0.237, -0.001, -0.096], [0.643, -0.014, -0.306, 0.084, 0.267, 0.638, 0.546, -0.014, 0.636, -0.24, 0.048, -0.75, -0.596, 0.424, 0.568, 0.046, 0.226, 0.33], [0.027, 0.154, -0.465, -0.226, -0.11, -0.242, 0.134, 0.154, 0.096, -0.43, -0.102, 0.14, -0.175, -0.308, -0.41, -0.3, -0.043, -0.178], [0.455, 0.655, -0.334, 0.169, 0.256, 0.179, 0.145, 0.655, 0.566, -0.32, 0.382, 0.714, 0.294, 0.125, 0.233, -0.123, 0.209, 0.347], [-0.482, -0.393, -0.532, -0.596, -0.6, -0.741, -0.298, -0.393, -0.343, -0.211, -0.267, -0.164, -0.621, -0.657, -0.642, -0.639, -0.563, -0.623], [-0.402, -0.332, -0.422, -0.566, -0.558, -0.734, -0.075, -0.332, -0.207, 0.037, -0.73, -0.146, -0.544, -0.616, -0.607, -0.578, -0.489, -0.582]]
weights = [-285.8213484316939, 805.6811318556302, 336.1612535719091, -644.6576241532944, 4748.572644275802, -4996.77190996746, 172.07967762598616, 455.58643291073884, 368.4195605810919, -4743.733812191356, 353.98407108122944, 2055.7501443498677, 1985.3465376158601, -3260.5535927555356, 2652.445152276083]
betas = [30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0]

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
        normalized_inputs = [
            2 * ((val - min_val) / (max_val - min_val)) - 1
            for val, min_val, max_val in zip(inputs, denorm_list_mins, denorm_list_maxes)
        ]
        predicted_value = model.predict(normalized_inputs)

        denormalized_value = (
            predicted_value * 0.5 * (denorm_ref_max - denorm_ref_min)
            + ((denorm_ref_max + denorm_ref_min) / 2)
        )

        denormalized_value = float(denormalized_value)
       
        return JsonResponse({'status': 'success', 'prediction': denormalized_value}, status=201)
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
