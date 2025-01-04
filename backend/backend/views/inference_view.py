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
centres = [[8.166, 11.496, -5.689, 2.929, 4.633, 3.623, 2.077, 11.496, 10.294, -7.85, 6.671, 12.185, 5.091, 3.979, 2.799, 4.746, -1.868, 3.589, 6.332], [-3.976, -2.12, -7.655, -1.906, -7.02, -11.871, 7.853, -2.12, -3.093, -2.038, -10.155, -1.006, -6.987, -8.711, -8.398, -8.926, -8.101, -6.368, -7.886], [-7.118, -6.366, -7.429, -7.206, -7.445, -7.937, -4.885, -6.366, -7.333, 1.313, -7.881, -3.777, -7.538, -7.7, -7.091, -7.772, -6.844, -7.434, -7.623], [8.933, 4.723, 2.285, 9.626, 9.562, 8.638, 3.414, 4.723, 6.777, 9.626, 5.147, 3.273, 4.441, 7.046, 8.805, 8.368, 4.903, 5.827, 7.021], [2.642, 6.408, -13.44, 0.944, -0.263, -6.975, 6.958, 6.408, 5.219, -8.123, 3.258, 5.834, -3.873, -9.42, -8.607, -11.307, -8.509, -0.443, -4.012], [10.079, -0.219, -4.797, 2.712, 4.185, 10.001, 8.559, -0.219, 9.97, -3.762, 0.941, -11.757, -9.343, 6.709, 8.559, 8.904, 0.721, 3.543, 5.157], [-2.448, -0.965, -9.487, -9.213, -3.9, -8.18, 6.606, -0.965, 1.11, 11.57, -3.33, 2.395, -3.824, -10.164, -8.735, -11.296, -7.207, -4.546, -6.72], [-5.893, -4.559, -6.514, -7.774, -7.884, -10.119, -0.553, -4.559, -3.633, -0.58, -8.269, -2.266, -7.875, -8.579, -8.304, -8.56, -8.563, -7.119, -8.189], [6.646, 12.711, -7.052, 3.904, 4.062, -0.683, 7.887, 12.711, 11.3, -11.171, 3.278, 9.016, 0.429, -2.155, -0.92, -1.388, -4.068, 2.815, 3.458], [7.481, 7.481, 7.481, 7.481, 7.481, 7.481, -0.349, 7.481, 4.249, 1.965, 7.481, 6.204, 7.481, 7.481, 7.481, 7.481, 7.481, 7.481, 7.481], [8.932, 6.991, -5.11, 2.623, 0.546, 6.308, 11.373, 6.991, 11.373, -6.96, 0.561, -8.962, -8.416, 8.689, 6.9, 6.991, -1.183, 0.637, 4.125]]
weights = [-4.643940251062254, -0.3124526385493942, -6.4169600211625575, -18.30116389573287, -49.18595684742707, 70.19565077452407, 4.259157969962892, -19.077826989181474, 62.81606369518751, 31.39776420373495, -69.93657946318774]
betas = [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0]
scaling = 1.0

denorm_list_mins = [1990.33,455366.67,-874000000.00,-3333333333.33,-9940666666.67,-128177000000.00,19650.00,455366.67,4266.67,-1.22,-5681316666.67,-23491.33,-5614833333.33,-15513450000.00,-60877500000.00,95548.00,2282420448.00,2951034754.83,-27438101550.50]
denorm_list_maxes = [2027.67,612433.33,134982000000.00,343333333333.33,412848666666.67,962311000000.00,56850.00,612433.33,35733.33,12.52,42643616666.67,1602679.33,99079833333.33,233073350000.00,598982500000.00,365692.00,31129939936.00,137864137892.17,495348300221.50]
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
        denormalized_value = max(0, float(list(numpy.array(denormalized_value).flat)[0]))
        return JsonResponse({'status': 'success', 'prediction': denormalized_value}, status=201)
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
