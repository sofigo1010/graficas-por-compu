def vertexShader(vertex, **kwargs):
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    viewportMatrix = kwargs["viewportMatrix"]

    vt = [vertex[0], vertex[1], vertex[2], 1]

    vt = matrix_multiply_vector(modelMatrix, vt)
    vt = matrix_multiply_vector(viewMatrix, vt)
    vt = matrix_multiply_vector(projectionMatrix, vt)
    vt = matrix_multiply_vector(viewportMatrix, vt)

    if vt[3] != 0:
        vt = [vt[0] / vt[3], vt[1] / vt[3], vt[2] / vt[3]]

    return vt

def matrix_multiply_vector(matrix, vector):
    result = [0 for _ in range(len(vector))]
    for i in range(len(matrix)):
        for j in range(len(vector)):
            result[i] += matrix[i][j] * vector[j]
    return result

def fragmentShader(**kwargs):
    # Se lleva a cabo por cada pixel individual
    
    # Obtenemos la informacion requerida
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]

    # Sabiendo que las coordenadas de textura
    # están en la 4ta y 5ta posicion de cada
    # indice del vertice, los obtenemos y
    # guardamos

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    
    # Empezamos siempre con color blanco
    r = 1
    g = 1
    b = 1

    vtP = [ u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]
    
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
        
    # Se regresa el color
    return [r,g,b]