from django.http import JsonResponse
import json
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import numpy

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
  def __init__(self, centres, inputBetas, weights):
    self.inputBetas = inputBetas
    self.centres = centres
    self.weights = weights
  
  def hiddenLayerActivationMatrix(self, X): # X is an array of points, not a single one
    matrixlist = []
    for point in X:
      row = [gaussian_rbf(point, centre, self.inputBetas[index]) for index, centre in enumerate(self.centres)]
      matrixlist.append(row)

    # Now, matrixlist is a 2-dimensional list
    return numpy.array(matrixlist) # This is the matrix of activations
    
  def predict(self, X):
    M = self.hiddenLayerActivationMatrix([X])
    return M @ self.weights


    

# Constants
centres = [[-0.322, -0.154, -0.87, -0.51, -0.546, -1.006, 0.728, -0.154, -0.092, 0.51, -0.706, 0.077, -0.54, -0.957, -1.027, -0.772, -0.548, -0.736], [1.089, 1.252, -0.113, 0.658, 0.842, 0.712, 0.274, 1.252, 1.108, -0.374, 0.828, 1.211, 0.724, 0.673, 0.777, 0.228, 0.671, 0.884], [-1.071, -0.901, -1.148, -1.268, -1.26, -1.481, -0.453, -0.901, -0.907, 0.063, -1.364, -0.499, -1.267, -1.337, -1.342, -1.264, -1.197, -1.3], [1.232, 0.447, -0.643, -0.004, 0.303, 1.054, 1.296, 0.447, 1.386, -0.699, 0.072, -1.341, -1.151, 0.997, 1.029, -0.032, 0.267, 0.603], [0.321, 0.695, -0.751, -0.108, 0.136, -0.297, 0.578, 0.695, 0.598, -0.655, 0.203, 0.489, -0.163, -0.443, -0.489, -0.469, 0.077, -0.035]]
weights = [-16.39572824435811, 37.882555093607046, 2.291104467915524, 9.1847908278924, -32.63222088440711]
betas = [24.02377264864287, 24.02377264864287, 24.02377264864287, 24.02377264864287, 24.02377264864287, 24.02377264864287, 24.02377264864287, 24.02377264864287, 24.02377264864287, 24.02377264864287, 24.02377264864287, 24.02377264864287, 24.02377264864287, 24.02377264864287, 24.02377264864287, 24.02377264864287, 24.02377264864287, 24.02377264864287, 24.02377264864287, 24.02377264864287, 24.02377264864287, 24.02377264864287, 24.02377264864287]
scaling = 2.0

denorm_list_mins = [1990.33, 455366.67, -874000000.0, -9900333333.33, -9940666666.67, -128177000000.0, 19650.0, 455366.67, 4266.67, -1.22, -4933833333.33, -23491.33, -5614833333.33, -15534783333.33, 95548.0, 2282420447.49, 2939534754.37, -27477601550.27]
denorm_list_maxes = [2027.67, 612433.33, 134982000000.0, 398942333333.33, 412848666666.67, 962311000000.0, 56850.0, 612433.33, 35733.33, 12.52, 42536833333.33, 1602679.33, 99079833333.33, 233222683333.33, 365692.0, 31129939936.07, 137944637892.23, 495624800221.47]
denorm_ref_min = -28546333333.33
denorm_ref_max = 761792333333.33
model = RFBN(centres, betas, weights)

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
        denormalized_value = max(0, float(denormalized_value))
        return JsonResponse({'status': 'success', 'prediction': denormalized_value}, status=201)
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)