import math

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