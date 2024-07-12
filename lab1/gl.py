import struct
def char(c):
    #1 byte
    #numeros
    return struct.pack("=c", c.encode(("ascii")))

def word(w):
    #2 bytes
    return struct.pack("=h", w)

def dword(d):
    #4 bytes
    return struct.pack("=l",d)

class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.glColor(1,1,1)
        self.glClearColor(0,0,0)
        self.glClear()

    def glColor(self, r,g,b):
        r= min(1, max(0,r))
        g= min(1, max(0,g))
        b= min(1, max(0,b))
        
        self.currColor= [r,g,b]

    def glClearColor(self, r,g,b):
        r= min(1, max(0,r))
        g= min(1, max(0,g))
        b= min(1, max(0,b))
        
        self.clearColor = [r,g,b]
    
    def glClear(self):
        color = [int(i*255) for i in self.clearColor]
        self.screen.fill(color)

        self.frameBuffer = [[self.clearColor for y in range(self.height)]
                            for x in range(self.width)]
        

    def glPoint(self, x, y, color=None):
        if(0<=x<self.width) and (0<=y<self.height):
            color = [int(i*255) for i in (color or self.currColor)]
            self.screen.set_at((x, self.height - 1 - y), color)
            self.frameBuffer[x][y] = color

    def glLine(self,v0,v1,color=None):

        x0 = int(v0[0])
        x1 = int(v1[0])
        y0 = int(v0[1])
        y1 = int(v1[1])

        if x0 == x1 and y0 == y1:
            self.glPoint(x0,y0)
            return 
    
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx 

        if steep: 
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset = 0
        limit = 0.75
        m = dy / dx
        y = y0


        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint(y, x, color or self.currColor)
            else:
                self.glPoint(x, y, color or self.currColor)

            offset += m
            
            if offset >= limit:
                if y0 < y1:
                    y += 1
                else:
                    y -= 1
                
                limit += 1

    def glGenerateFramebuffer(self, filename):
        #w es write la b escribir en binario
        with open(filename, "wb") as file:
            #HEADER
            file.write(char("B"))
            file.write(char("M"))
            #14 del header 40 del info header y la otra cosa es la tabla de colores
            file.write(dword(14+40+(self.width*self.height*3)))
            file.write(dword(0))
            #offset
            file.write(dword(14+40))
            
            
            #INFO HEADER
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width*self.height*3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            
            
            
            #COLOR TABLE
            for y in range(self.height):
                for x in range(self.width):
                    color=self.frameBuffer[x][y]
                    #vuelve 1 byte por cada color: rojo, verde, azul
                    color = bytes([color[2], color[1], color[0]])
                    file.write(color)
                    
                    
    def fill_polygon(self, polygon, color=None):
        min_y = min(p[1] for p in polygon)
        max_y = max(p[1] for p in polygon)
        
        for y in range(min_y, max_y + 1):
            intersections = []
            for i in range(len(polygon)):
                start, end = polygon[i], polygon[(i + 1) % len(polygon)]
                # para llenar full las intersecciones mientras no esten en lados horizontales
                if start[1] != end[1]:  
                    if (start[1] < y <= end[1] or end[1] < y <= start[1]):
                        dx, dy = end[0] - start[0], end[1] - start[1]
                        x = start[0] + (y - start[1]) * dx / dy if dy else start[0]
                        intersections.append(x)
            #ordeno de izq a derecha            
            intersections.sort()
            
            
            for i in range(0, len(intersections), 2):
                if i + 1 < len(intersections):
                    x_start, x_end = int(intersections[i]), int(intersections[i + 1])
                    #el 1 para llenar el ultimo puntito
                    for x in range(x_start, x_end + 1):  
                        self.glPoint(x, y, color or self.currColor)

    def poligono(self, listapuntos, color):
        self.glColor(*color) 
        for i in range(len(listapuntos)):
            self.glLine(listapuntos[i], listapuntos[(i + 1) % len(listapuntos)])
        self.fill_polygon(listapuntos, self.currColor)