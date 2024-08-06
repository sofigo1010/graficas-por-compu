def vertexShader(vertex, **kwargs):
    modelMatrix = kwargs["modelMatrix"]
    
    vt = [vertex[0], vertex[1], vertex[2], 1]
    
    vt = matrix_multiply_vector(modelMatrix, vt)
    
    if vt[3] != 0:
        vt = [vt[0] / vt[3], vt[1] / vt[3], vt[2] / vt[3]]
    
    return vt

def matrix_multiply_vector(matrix, vector):
    result = [0 for _ in range(len(vector))]
    for i in range(len(matrix)):
        for j in range(len(vector)):
            result[i] += matrix[i][j] * vector[j]
    return result