from math import acos, asin, pi, sqrt

def dot_product(vec1, vec2):
    return sum(v1 * v2 for v1, v2 in zip(vec1, vec2))

def magnitude(vec):
    return sqrt(sum(v ** 2 for v in vec))

def normalize(vec):
    mag = magnitude(vec)
    return [v / mag for v in vec]

def scalar_multiply(scalar, vec):
    return [scalar * v for v in vec]

def vector_add(vec1, vec2):
    return [v1 + v2 for v1, v2 in zip(vec1, vec2)]

def vector_subtract(vec1, vec2):
    return [v1 - v2 for v1, v2 in zip(vec1, vec2)]

def refractVector(normal, incident, n1, n2):
    # Producto punto
    c1 = dot_product(normal, incident)

    if c1 < 0:
        c1 = -c1
    else:
        normal = scalar_multiply(-1, normal)
        n1, n2 = n2, n1

    n = n1 / n2
    incident_plus_c1_normal = vector_add(incident, scalar_multiply(c1, normal))
    root_term = sqrt(1 - n ** 2 * (1 - c1 ** 2))
    T = vector_subtract(scalar_multiply(n, incident_plus_c1_normal), scalar_multiply(root_term, normal))

    # Normalización del vector
    return normalize(T)

def totalInternalReflection(normal, incident, n1, n2):
    c1 = dot_product(normal, incident)
    if c1 < 0:
        c1 = -c1
    else:
        n1, n2 = n2, n1

    if n1 < n2:
        return False

    theta1 = acos(c1)
    thetaC = asin(n2 / n1)

    return theta1 >= thetaC

def fresnel(normal, incident, n1, n2):
    c1 = dot_product(normal, incident)
    if c1 < 0:
        c1 = -c1
    else:
        n1, n2 = n2, n1

    s2 = (n1 * sqrt(1 - c1 ** 2)) / n2
    c2 = sqrt(1 - s2 ** 2)

    F1 = (((n2 * c1) - (n1 * c2)) / ((n2 * c1) + (n1 * c2))) ** 2
    F2 = (((n1 * c2) - (n2 * c1)) / ((n1 * c2) + (n2 * c1))) ** 2

    Kr = (F1 + F2) / 2
    Kt = 1 - Kr
    return Kr, Kt
