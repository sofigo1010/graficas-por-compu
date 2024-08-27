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
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    textureList = kwargs["textureList"]
    dirLight = kwargs["dirLight"]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    r = 1
    g = 1
    b = 1

    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]
    
    if len(textureList) > 0:
        texColor = textureList[0].getColor(vtP[0], vtP[1])
        if texColor:
            r *= texColor[0]
            g *= texColor[1]
            b *= texColor[2]
        
    return [r, g, b]

def unlitShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    textureList = kwargs["textureList"]
    dirLight = kwargs["dirLight"]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    r = 1
    g = 1
    b = 1

    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]
    
    if len(textureList) > 0:
        texColor = textureList[0].getColor(vtP[0], vtP[1])
        
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
        
    return [r, g, b]

def gouradShader(**kwargs):
    
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    textureList = kwargs["textureList"]
    dirLight = kwargs["dirLight"]
    modelMatrix = kwargs["modelMatrix"]
    
    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]
    
    normal = [
        u * nA[0] + v * nB[0] + w * nC[0],
        u * nA[1] + v * nB[1] + w * nC[1],
        u * nA[2] + v * nB[2] + w * nC[2],
        0
    ]

    normal = [
        sum(modelMatrix[i][j] * normal[j] for j in range(4))
        for i in range(3)
    ]


    norm = math.sqrt(sum(comp**2 for comp in normal))
    normal = [comp / norm for comp in normal]
        
    r = 1
    g = 1
    b = 1

    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]
    
    if len(textureList)> 0:
        texColor = textureList[0].getColor(vtP[0], vtP[1])
        
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
        

    dirLight_neg = [-dirLight[0], -dirLight[1], -dirLight[2]]
    intensity = sum(normal[i] * dirLight_neg[i] for i in range(3))
    
    intensity = max(0, intensity)
    r *= intensity
    g *= intensity
    b *= intensity

    return [r, g, b]

def flatShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    textureList = kwargs["textureList"]
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
    
    if len(textureList) > 0:
        texColor = textureList[0].getColor(vtP[0], vtP[1])
        
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]

    dirLight_neg = [-dirLight[0], -dirLight[1], -dirLight[2]]
    intensity = (normal[0] * dirLight_neg[0] + 
                 normal[1] * dirLight_neg[1] + 
                 normal[2] * dirLight_neg[2])
    
    intensity = max(0, intensity)
    r *= intensity
    g *= intensity
    b *= intensity
    
    return [r, g, b]

def toonShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    textureList = kwargs["textureList"]
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
    
    if len(textureList) > 0:
        texColor = textureList[0].getColor(vtP[0], vtP[1])
        
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]

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
    
    return [r, g, b]

def bluetoonShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    textureList = kwargs["textureList"]
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
    
    if len(textureList) > 0:
        texColor = textureList[0].getColor(vtP[0], vtP[1])
        
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]

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
    
    return [r, g, b]

def glowShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    textureList = kwargs["textureList"]
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

    if len(textureList) > 0:
        texColor = textureList[0].getColor(u, v)
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]

    r += yellowGlow[0] * glowIntensity
    g += yellowGlow[1] * glowIntensity
    b += yellowGlow[2] * glowIntensity

    return [min(1, r), min(1, g), min(1, b)]

def infraredShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    textureList = kwargs["textureList"]
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
    
    if len(textureList) > 0:
        texColor = textureList[0].getColor(vtP[0], vtP[1])
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
    
    return [r, g, b]

def stripeDistortionShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    textureList = kwargs["textureList"]
    
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
    if len(textureList) > 0:
        texColor = textureList[0].getColor(distorted_u, distorted_v)
        if texColor:
            r *= texColor[0]
            g *= texColor[1]
            b *= texColor[2]

    return [r, g, b]

def whitengrayShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    textureList = kwargs["textureList"]
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


def lineShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    textureList = kwargs["textureList"]
    dirLight = kwargs["dirLight"]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    r = 1
    g = 1
    b = 1

    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]
    
    if len(textureList) > 0:
        texColor = textureList[0].getColor(vtP[0], vtP[1])
        
        if texColor:
            r *= texColor[0]
            g *= texColor[1]
            b *= texColor[2]
        else:
            pass
    
    height = u * A[1] + v * B[1] + w * C[1]

    value = math.sin(height)

    if value < -0.5:
        return None    
    
    return [r, g, b]

def textureBlendShader(**kwargs):
    
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    textureList = kwargs["textureList"]
    dirLight = kwargs["dirLight"]
    modelMatrix = kwargs["modelMatrix"]
    
    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]
    
    normal = [
        u * nA[0] + v * nB[0] + w * nC[0],
        u * nA[1] + v * nB[1] + w * nC[1],
        u * nA[2] + v * nB[2] + w * nC[2],
        0
    ]

    normal = [
        sum(modelMatrix[i][j] * normal[j] for j in range(4))
        for i in range(3)
    ]


    norm = math.sqrt(sum(comp**2 for comp in normal))
    normal = [comp / norm for comp in normal]
        
    r = 1
    g = 1
    b = 1

    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]
    
    dirLight_neg = [-dirLight[0], -dirLight[1], -dirLight[2]]
    intensity = sum(normal[i] * dirLight_neg[i] for i in range(3))
    
    intensity = max(0, intensity)
    
    if len(textureList) >= 2:
        texColor1 = textureList[0].getColor(vtP[0], vtP[1])
        texColor2 = textureList[1].getColor(vtP[0], vtP[1])

        r *= (texColor1[0] * intensity) + (texColor2[0] * (1 - intensity))
        g *= (texColor1[1] * intensity) + (texColor2[1] * (1 - intensity))
        b *= (texColor1[2] * intensity) + (texColor2[2] * (1 - intensity))
            
    return [r, g, b]






def darkerBackgroundShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    textureList = kwargs["textureList"]

    
    
    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]


    texColor = [1, 1, 1]  
    if len(textureList) > 0:
        texColor = textureList[0].getColor(vtP[0], vtP[1])


    bgColor = kwargs["background"].getColor(vtP[0], vtP[1])


    darkenFactor = 0.7
    bgColor = [comp * darkenFactor for comp in bgColor]


    blendedColor = [
        (texColor[i] * 0.7 + bgColor[i] * 0.3)  
        for i in range(3)
    ]

    return blendedColor

def scamShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    textureList = kwargs["textureList"]
    dirLight = kwargs["dirLight"]
    modelMatrix = kwargs["modelMatrix"]

    
    y = u * A[1] + v * B[1] + w * C[1]

    
    y = (y - min(A[1], B[1], C[1])) / (max(A[1], B[1], C[1]) - min(A[1], B[1], C[1]))

    
    start_color = [1, 0, 0]  
    end_color = [0, 1, 1]    

    
    r = start_color[0] * (1 - y) + end_color[0] * y
    g = start_color[1] * (1 - y) + end_color[1] * y
    b = start_color[2] * (1 - y) + end_color[2] * y

    
    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]
    
    normal = [
        u * nA[0] + v * nB[0] + w * nC[0],
        u * nA[1] + v * nB[1] + w * nC[1],
        u * nA[2] + v * nB[2] + w * nC[2],
        0
    ]

    
    normal = [
        sum(modelMatrix[i][j] * normal[j] for j in range(4))
        for i in range(3)
    ]

    
    norm = math.sqrt(sum(comp ** 2 for comp in normal))
    normal = [comp / norm for comp in normal]


    
    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]

    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]

    if len(textureList) > 0:
        texColor = textureList[0].getColor(vtP[0], vtP[1])
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]

    
    r = max(0, min(1, r))
    g = max(0, min(1, g))
    b = max(0, min(1, b))

    return [r, g, b]

def distortionShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    textureList = kwargs["textureList"]
    
    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]
    
    frequency = 20.0  
    amplitude = 0.2  

    
    triangle_wave = 2 * amplitude * abs((vtP[1] * frequency) % 1 - 0.5)

    distorted_u = vtP[0] + triangle_wave
    distorted_v = vtP[1]

    
    distorted_u = max(0, min(1, distorted_u))
    distorted_v = max(0, min(1, distorted_v))

    
    stripe_threshold = 0.05 
    if abs(triangle_wave) < stripe_threshold:
        return None  
    
    
    r, g, b = 1, 1, 1
    if len(textureList) > 0:
        texColor = textureList[0].getColor(distorted_u, distorted_v)
        if texColor:
            r *= texColor[0]
            g *= texColor[1]
            b *= texColor[2]

    return [r, g, b]

def pixelateShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    textureList = kwargs["textureList"]
    
    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    
    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]
    
    pixel_size = 0.05  

    
    pixelated_u = math.floor(vtP[0] / pixel_size) * pixel_size
    pixelated_v = math.floor(vtP[1] / pixel_size) * pixel_size

   
    pixelated_u = max(0, min(1, pixelated_u))
    pixelated_v = max(0, min(1, pixelated_v))

    r, g, b = 1, 1, 1
    if len(textureList) > 0:
        texColor = textureList[0].getColor(pixelated_u, pixelated_v)
        if texColor:
            r *= texColor[0]
            g *= texColor[1]
            b *= texColor[2]

    return [r, g, b]

