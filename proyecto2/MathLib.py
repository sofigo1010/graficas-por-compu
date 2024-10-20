import math
def barycentricCoords(A, B, C, P):
    # Se calcula el área de los subtriángulos y del triángulo
    # mayor usando el Teorema de Shoelace, una fórmula que permite
    # calcular el área de un polígono de cualquier cantidad de vértices.

    areaPCB = abs((P[0] * C[1] + C[0] * B[1] + B[0] * P[1]) -
                  (P[1] * C[0] + C[1] * B[0] + B[1] * P[0]))

    areaACP = abs((A[0] * C[1] + C[0] * P[1] + P[0] * A[1]) -
                  (A[1] * C[0] + C[1] * P[0] + P[1] * A[0]))

    areaABP = abs((A[0] * B[1] + B[0] * P[1] + P[0] * A[1]) -
                  (A[1] * B[0] + B[1] * P[0] + P[1] * A[0]))

    areaABC = abs((A[0] * B[1] + B[0] * C[1] + C[0] * A[1]) -
                  (A[1] * B[0] + B[1] * C[0] + C[1] * A[0]))

    # Si el área del triángulo es 0, retornar nada para
    # prevenir división por 0.
    if areaABC == 0:
        return None

    # Determinar las coordenadas baricéntricas dividiendo el 
    # área de cada subtriángulo por el área del triángulo mayor.
    u = areaPCB / areaABC
    v = areaACP / areaABC
    w = areaABP / areaABC

    # Si cada coordenada está entre 0 a 1 y la suma de las tres
    # es igual a 1, entonces son válidas.
    if 0<=u<=1 and 0<=v<=1 and 0<=w<=1:
        return (u, v, w)
    else:
        return None

def TranslationMatrix(x, y, z):
    return [
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ]

def ScaleMatrix(x, y, z):
    return [
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [0, 0, z, 0],
        [0, 0, 0, 1]
    ]

def rotationmatrix(pitch, yaw, roll):
    pitch = math.radians(pitch)
    yaw = math.radians(yaw)
    roll = math.radians(roll)

    pitchMat = [
        [1, 0, 0, 0],
        [0, math.cos(pitch), -math.sin(pitch), 0],
        [0, math.sin(pitch), math.cos(pitch), 0],
        [0, 0, 0, 1]
    ]

    yawMat = [
        [math.cos(yaw), 0, math.sin(yaw), 0],
        [0, 1, 0, 0],
        [-math.sin(yaw), 0, math.cos(yaw), 0],
        [0, 0, 0, 1]
    ]

    rollMat = [
        [math.cos(roll), -math.sin(roll), 0, 0],
        [math.sin(roll), math.cos(roll), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]
    rotationMat = matrix_multiply(matrix_multiply(pitchMat, yawMat), rollMat)
    return rotationMat

def matrix_multiply(A, B):
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_inverse(matrix):
        n = len(matrix)
        identity = [[1 if i == j else 0 for i in range(n)] for j in range(n)]
        inverse = [[matrix[i][j] for j in range(n)] for i in range(n)]
        
        for i in range(n):
            factor = inverse[i][i]
            for j in range(n):
                inverse[i][j] /= factor
                identity[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = inverse[k][i]
                    for j in range(n):
                        inverse[k][j] -= factor * inverse[i][j]
                        identity[k][j] -= factor * identity[i][j]
        
        return identity
    

def reflectVector(normal, direction):
    # R = 2 * (N . L) * N - L
    dot_product = sum([normal[i] * direction[i] for i in range(3)])
    reflect = [2 * dot_product * normal[i] for i in range(3)]
    reflect = [reflect[i] - direction[i] for i in range(3)]
    norm = math.sqrt(sum([reflect[i]**2 for i in range(3)]))
    reflect = [reflect[i] / norm for i in range(3)]
    return reflect
