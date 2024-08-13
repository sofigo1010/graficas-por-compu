import math

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
    dirLight = kwargs["dirLight"]

    # Sabiendo que las coordenadas de textura
    # están en la 4ta y 5ta posicion de cada
    # indice del vertice, los obtenemos y
    # guardamos

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    # Sabiendo que los valores de las normales 
    # están en la 6ta, 7ma y 8va posición 
    # de cada vértice, los obtenemos y guardamos

    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]
    
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


def unlitShader(**kwargs):
    # Se lleva a cabo por cada pixel individual
    
    # Obtenemos la informacion requerida
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    # Sabiendo que las coordenadas de textura
    # estan en la 4ta y 5ta posición de cada 
    # índice del vértice, los obtenemos y
    # guardamos

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    # Empezamos siempre con color blanco
    r = 1
    g = 1
    b = 1

    # P = uA + vB + wC
    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]
    
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
        
    # Se regresa el color
    return [r, g, b]


def gouradShader(**kwargs):
    
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]
    
    normal = [u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2]]
    
    r = 1
    g = 1
    b = 1

    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]
    
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
        
    # intensity = normal DOT -dirlight
    dirLight_neg = [-dirLight[0], -dirLight[1], -dirLight[2]]
    intensity = (normal[0] * dirLight_neg[0] + 
                 normal[1] * dirLight_neg[1] + 
                 normal[2] * dirLight_neg[2])
    
    intensity = max(0, intensity)
    r *= intensity
    g *= intensity
    b *= intensity
    
    # Se regresa el color
    return [r, g, b]

def flatShader(**kwargs):
    
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]
    
    normal = [(nA[0] + nB[0] + nC[0]) / 3,
              (nA[1] + nB[1] + nC[1]) / 3,
              (nA[2] + nB[2] + nC[2]) / 3]
    
    r = 1
    g = 1
    b = 1

    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]
    
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
        
    # intensity = normal DOT -dirlight
    dirLight_neg = [-dirLight[0], -dirLight[1], -dirLight[2]]
    intensity = (normal[0] * dirLight_neg[0] + 
                 normal[1] * dirLight_neg[1] + 
                 normal[2] * dirLight_neg[2])
    
    intensity = max(0, intensity)
    r *= intensity
    g *= intensity
    b *= intensity
    
    # Se regresa el color
    return [r, g, b]


def toonShader(**kwargs):
    
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]
    
    normal = [u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2]]
    
    r = 1
    g = 1
    b = 1

    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]
    
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
        
    # intensity = normal DOT -dirlight
    dirLight_neg = [-dirLight[0], -dirLight[1], -dirLight[2]]
    intensity = (normal[0] * dirLight_neg[0] + 
                 normal[1] * dirLight_neg[1] + 
                 normal[2] * dirLight_neg[2])
    
    intensity = max(0, intensity)
    
    if intensity < 0.33:
        intensity = 0.3
    elif intensity < 0.66:
        intensity = 0.6
    else:
        intensity = 1.0

    r *= intensity
    g *= intensity
    b *= intensity
    
    # Se regresa el color
    return [r, g, b]

def bluetoonShader(**kwargs):
    
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]
    
    normal = [u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2]]
    
    r = 1
    g = 1
    b = 1

    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]
    
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
        
    # intensity = normal DOT -dirlight
    dirLight_neg = [-dirLight[0], -dirLight[1], -dirLight[2]]
    intensity = (normal[0] * dirLight_neg[0] + 
                 normal[1] * dirLight_neg[1] + 
                 normal[2] * dirLight_neg[2])
    
    intensity = max(0, intensity)
    
    if intensity < 0.33:
        intensity = 0.3
    elif intensity < 0.66:
        intensity = 0.6
    else:
        intensity = 1.0

    r *= intensity
    g *= intensity
    b *= intensity
    
    b = 1
    
    
    # Se regresa el color
    return [r, g, b]

def glowShader(**kwargs):
    
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]
    modelMatrix = kwargs["modelMatrix"]
    camMatrix = kwargs["camMatrix"]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]
    
    normal = [u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2]]
    
    # GLOW
    yellowGlow = [1, 1, 0]
    
    camForward = [
        camMatrix[0][2],
        camMatrix[1][2],
        camMatrix[2][2]
    ]
    
    glowIntensity = 1 - (normal[0] * camForward[0] + normal[1] * camForward[1] + normal[2] * camForward[2])
    glowIntensity = min(1, max(0, glowIntensity))
    
    r = 0.2 
    g = 0.2
    b = 0.2

    r += yellowGlow[0] * glowIntensity
    g += yellowGlow[1] * glowIntensity
    b += yellowGlow[2] * glowIntensity

    # Se regresa el color
    return [min(1, r), min(1, g), min(1, b)]





def infraredShader(**kwargs):
    
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]


    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    

    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]
    

    normal = [u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2]]
    

    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]
    
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
    else:
        texColor = [1, 1, 1]
    

    dirLight_neg = [-dirLight[0], -dirLight[1], -dirLight[2]]
    intensity = (normal[0] * dirLight_neg[0] + 
                 normal[1] * dirLight_neg[1] + 
                 normal[2] * dirLight_neg[2])
    
    intensity = max(0, min(1, intensity))
    

    if intensity < 0.25:

        r = 0
        g = 4 * intensity
        b = 1
    elif intensity < 0.5:

        r = 0
        g = 1
        b = 1 - 4 * (intensity - 0.25)
    elif intensity < 0.75:

        r = 4 * (intensity - 0.5)
        g = 1
        b = 0
    else:

        r = 1
        g = 1 - 4 * (intensity - 0.75)
        b = 0
    

    r *= texColor[0]
    g *= texColor[1]
    b *= texColor[2]
    
    # Se regresa el color final
    return [r, g, b]

def stripeDistortionShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]
    
    
    frequency = 200.0  
    amplitude = 0.2  

    
    distorted_u = vtP[0] + amplitude * math.sin(frequency * vtP[1])

    
    distorted_v = vtP[1]

    
    distorted_u = max(0, min(1, distorted_u))
    distorted_v = max(0, min(1, distorted_v))

    r, g, b = 1, 1, 1
    if texture:
        texColor = texture.getColor(distorted_u, distorted_v)
        if texColor:
            r *= texColor[0]
            g *= texColor[1]
            b *= texColor[2]

    return [r, g, b]

def whitengrayShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]
    
    
    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]
    
    normal = [
        u * nA[0] + v * nB[0] + w * nC[0],
        u * nA[1] + v * nB[1] + w * nC[1],
        u * nA[2] + v * nB[2] + w * nC[2]
    ]

    
    intensity = abs(normal[0] * dirLight[0] +
                    normal[1] * dirLight[1] +
                    normal[2] * dirLight[2])
    
    
    if intensity < 0.2:
        return [1, 1, 1]  
    
    
    return [0.5, 0.5, 0.5]  



