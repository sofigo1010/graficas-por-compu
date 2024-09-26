from camera import *
import struct
from math import * 
import pygame
import random

def char(c):
    # 1 byte
    return struct.pack("=c", c.encode("ascii"))

def word(w):
    # 2 bytes
    return struct.pack("=h", w)

def dword(d):
    # 4 bytes
    return struct.pack("=l", d)

class RendererRT(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.camera = Camera()
        self.glViewport(0,0,self.width, self.height)
        self.glProjection()
        self.glColor(1,1,1)
        self.glClearColor(0,0,0)
        self.glClear()
        self.scene = []
        self.Lights = []

    def glViewport(self, x, y, width, height):
        self.vpX = int(x)
        self.vpY = int(y)
        self.vpWidth = width
        self.vpHeight = height

    def glProjection(self, n=0.1, f=1000, fov=60):
        self.nearPlane = n
        self.farPlane = f
        self.fov = fov * math.pi / 180  
        aspectRatio = self.vpWidth / self.vpHeight
        self.topEdge = math.tan(self.fov / 2) * self.nearPlane
        self.rightEdge = self.topEdge * aspectRatio   
    
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
                                  
    def glCastRay(self, orig, direction, sceneObj=None):
        depth = float('inf')
        intercept = None
        hit = None

        for obj in self.scene:
            if obj != sceneObj:
                intercept = obj.ray_intersect(orig, direction)
                if intercept != None:
                    if intercept.distance < depth:
                        hit = intercept
                        depth = intercept.distance

        return hit

    def glRender(self):       
        indeces = [(i,j) for i in range (self.vpWidth) for j in range(self.vpHeight)]
        random.shuffle(indeces)
        for i,j in indeces:
            x = i + self.vpX
            y = j+self.vpY
            if 0 <= x < self.width and 0 <= y < self.height:
                # Coordenadas normalizadas
                # Que van de -1 a 1
                pX = ((x + 0.5 - self.vpX) / self.vpWidth) * 2 - 1
                pY = ((y + 0.5 - self.vpY) / self.vpHeight) * 2 - 1
                pX *= self.rightEdge
                pY *= self.topEdge
                dir = [pX, pY, -self.nearPlane]
                dir_magnitude = math.sqrt(dir[0]**2 + dir[1]**2 + dir[2]**2)
                dir = [component / dir_magnitude for component in dir]
                intercept = self.glCastRay(self.camera.translate, dir)
                if intercept != None:
                    color = intercept.obj.material.GetSurfaceColor(intercept, self)
                    self.glPoint(x, y, color)
                    pygame.display.flip()
                    
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    