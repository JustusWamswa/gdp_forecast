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
centres = [[-0.17, -0.067, -0.659, -0.427, -0.271, -0.568, 0.459, -0.067, 0.077, 0.804, -0.257, 0.166, -0.266, -0.706, -0.785, -0.501, -0.316, -0.467], [0.721, 1.044, -0.501, 0.249, 0.409, 0.282, 0.234, 1.044, 0.939, -0.819, 0.531, 1.091, 0.426, 0.284, 0.367, -0.177, 0.319, 0.537], [-0.933, -0.705, -1.007, -1.017, -1.028, -1.178, -0.26, -0.705, -0.957, 0.257, -1.188, -0.452, -1.055, -1.097, -1.121, -1.042, -1.027, -1.078], [1.018, -0.022, -0.485, 0.133, 0.423, 1.011, 0.865, -0.022, 1.007, -0.38, 0.076, -1.188, -0.944, 0.672, 0.9, 0.073, 0.358, 0.523], [1.188, 1.188, 1.188, 1.188, 1.188, 1.188, -0.055, 1.188, 0.675, 0.312, 1.188, 0.985, 1.188, 1.188, 1.188, 1.188, 1.188, 1.188], [0.085, 0.262, -0.682, -0.293, -0.086, -0.363, 0.268, 0.262, 0.202, -0.388, -0.077, 0.261, -0.225, -0.449, -0.594, -0.442, -0.046, -0.239], [-0.382, -0.204, -0.735, -0.369, -0.674, -1.14, 0.754, -0.204, -0.297, -0.196, -1.014, -0.097, -0.671, -0.836, -0.857, -0.778, -0.612, -0.757], [0.382, 0.767, -0.53, 0.07, 0.253, -0.14, 0.6, 0.767, 0.677, -0.617, 0.338, 0.482, -0.057, -0.278, -0.232, -0.318, 0.141, 0.131], [-0.636, -0.519, -0.709, -0.92, -0.895, -1.163, -0.095, -0.519, -0.345, -0.156, -0.945, -0.223, -0.884, -0.971, -0.961, -0.936, -0.784, -0.921], [1.102, 0.583, 0.282, 0.942, 1.18, 1.066, 0.421, 0.583, 0.836, 1.188, 0.626, 0.404, 0.548, 0.874, 1.033, 0.605, 0.725, 0.863], [-1.145, -1.114, -1.161, -1.152, -1.158, -1.186, -1.034, -1.114, -1.107, 0.15, -1.188, -0.653, -1.164, -1.178, -1.176, -1.07, -1.159, -1.172], [0.933, 0.73, -0.534, -0.139, 0.057, 0.659, 1.188, 0.73, 1.188, -0.727, 0.038, -0.936, -0.879, 0.908, 0.73, -0.124, 0.065, 0.432]]
weights = [-406.0368049680577, 345.31458642017276, 1092.4325895699926, 376.8181414889366, -87.6310208949576, 634.8098442907911, -357.82957471877125, -536.7256522131177, 58.86615135411586, 115.47992677517459, -855.9514040013494, -380.2748248444693]
betas = [50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0]
scaling = 1.58

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
