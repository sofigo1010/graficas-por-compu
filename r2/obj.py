class Obj(object):
    def __init__(self, filename):
        # Asumiendo que el archivo es .obj
        with open(filename, "r") as file:
            lines = file.read().splitlines()

        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []

        for line in lines:
            try:
                prefix, value = line.split(" ", 1)

            except:
                continue
                
            if prefix == "v": #vertices
                vert = list(map(float, value.split(" ")))
                self.vertices.append(vert)

            elif prefix == "vt": #coordenadas de textura
                vts = list(map(float, value.split(" ")))
                self.texcoords.append(vts)

            if prefix == "vn": #normales
                norm = list(map(float, value.split(" ")))
                self.normals.append(norm)

            elif prefix == "f": #caras
                face = []
                verts = value.split(" ")
                for vert in verts:
                    vert = list(map(int, vert.split("/")))
                    face.append(vert)
                self.faces.append(face)