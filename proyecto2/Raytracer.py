import pygame
from pygame.locals import *
from gl import *
from figures import *
from material import *
from lights import *
from texture import *

width = 540
height = 540
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

rt = RendererRT(screen)
rt.envMap = Texture("textures/underfondo.bmp")

yellow_material = Material(diffuse=[1, 1, 0], spec=128, Ks=0.5, matType=OPAQUE)
orange_material = Material(diffuse=[1, 0.5, 0], spec=128, Ks=0.5, matType=OPAQUE)
black_material = Material(diffuse=[0, 0, 0], spec=128, Ks=0.5, matType=OPAQUE)
white_material = Material(diffuse=[1, 1, 1], spec=128, Ks=0.5, matType=OPAQUE)
grey_material = Material(diffuse=[0.5, 0.5, 0.5], spec=128, Ks=0.5, matType=OPAQUE)
transparent_material = Material(diffuse=[0.3, 0.3, 1], spec=128, Ks=0.1, matType=TRANSPARENT)
green_material = Material(diffuse=[0.2, 0.8, 0.2], spec=32, Ks=0.3, matType=OPAQUE)
light_green_material = Material(diffuse=[0.5, 1, 0.5], spec=32, Ks=0.3, matType=OPAQUE)

cuerpo_pez = Triangle(
    v0=[2.0, 0.5, -5],
    v1=[1.3, -0.5, -5],
    v2=[2.7, -0.5, -5],
    material=yellow_material
)
rt.scene.append(cuerpo_pez)

aleta_superior_izquierda = Triangle(
    v0=[1.4, 0.0, -5.05],
    v1=[1.86, 0.3, -5.05],
    v2=[1.6, -0.3, -5.05],
    material=orange_material
)
rt.scene.append(aleta_superior_izquierda)

aleta_derecha = Triangle(
    v0=[2.4, -0.1, -5],
    v1=[2.8, 0.2, -5],
    v2=[2.8, -0.4, -5],
    material=orange_material
)
rt.scene.append(aleta_derecha)

aleta_inferior = Triangle(
    v0=[2.0, -0.4, -4.95],
    v1=[2.1, -0.2, -4.95],
    v2=[1.9, -0.2, -4.95],
    material=orange_material
)
rt.scene.append(aleta_inferior)

ojo_blanco = Sphere(
    position=[1.65, -0.15, -4.9], 
    radius=0.06, 
    material=white_material
)
rt.scene.append(ojo_blanco)

ojo_negro = Sphere(
    position=[1.65, -0.15, -4.85],
    radius=0.03, 
    material=black_material
)
rt.scene.append(ojo_negro)

boca = Disk(
    position=[1.4, -0.2, -4.9],
    normal=[0, 1, 0],
    radius=0.1,
    material=black_material
)
rt.scene.append(boca)

beige_material = Material(diffuse=[0.96, 0.87, 0.70], spec=32, Ks=0.3, matType=OPAQUE)
sand_plane = Plane(
    position=[0, -6, -6], 
    normal=[0, 1, 0], 
    material=beige_material
)
rt.scene.append(sand_plane)

large_rock1 = Sphere(
    position=[-2.0, -3.5, -4.98],
    radius=1.0,
    material=grey_material
)
rt.scene.append(large_rock1)

large_rock2 = Sphere(
    position=[0.0, -3.8, -4.98],
    radius=1.2,
    material=grey_material
)
rt.scene.append(large_rock2)

large_rock3 = Sphere(
    position=[2.5, -3.2, -4.98],
    radius=0.9,
    material=grey_material
)
rt.scene.append(large_rock3)

starfish_texture = Texture("textures/pinkstar.bmp")
pink_material_with_texture = Material(
    diffuse=[1.0, 0.75, 0.8], 
    spec=32,
    Ks=0.5,
    matType=OPAQUE,
    texture=starfish_texture
)

starfish = Star(
    position=[0.0, -0.4, -5.5],
    size=0.5,
    material=pink_material_with_texture
)
rt.scene.append(starfish)

bottle_body = Cylinder(
    position=[-1.5, -0.4, -5.5],
    radius=0.1,
    height=0.5,
    material=transparent_material
)
rt.scene.append(bottle_body)

bottle_cap = Hemisphere(
    position=[-1.5, 0.1, -5.5],
    radius=0.1,
    material=grey_material,
    orientation='up'
)
rt.scene.append(bottle_cap)

bubble_material = Material(
    diffuse=[0.8, 0.9, 1],
    spec=64,
    Ks=0.1,
    matType=TRANSPARENT
)
bubble = Ellipsoid(
    position=[1.0, 1.0, -4.8],
    radii=[0.15, 0.2, 0.15],
    material=bubble_material
)
rt.scene.append(bubble)

plant1 = Triangle(
    v0=[-1.8, -3.0, -4.95],
    v1=[-2.0, -0.4, -4.95],
    v2=[-1.6, -3.0, -4.95],
    material=green_material
)
rt.scene.append(plant1)

plant2 = Triangle(
    v0=[-2.2, -3.0, -4.95],
    v1=[-2.4, -0.6, -4.95],
    v2=[-2.0, -3.0, -4.95],
    material=light_green_material
)
rt.scene.append(plant2)

plant3 = Triangle(
    v0=[0.2, -3.5, -4.95],
    v1=[0.1, -0.5, -4.95],
    v2=[0.5, -3.5, -4.95],
    material=green_material
)
rt.scene.append(plant3)

plant4 = Triangle(
    v0=[1.8, -3.2, -4.95],
    v1=[2.2, -0.7, -4.95],
    v2=[1.4, -3.2, -4.95],
    material=light_green_material
)
rt.scene.append(plant4)

plant5 = Triangle(
    v0=[-1.0, -3.0, -4.95],
    v1=[-1.4, -0.3, -4.95],
    v2=[-0.6, -3.0, -4.95],
    material=green_material
)
rt.scene.append(plant5)

plant6 = Triangle(
    v0=[0.5, -3.5, -4.95],
    v1=[0.2, -0.8, -4.95],
    v2=[0.8, -3.5, -4.95],
    material=light_green_material
)
rt.scene.append(plant6)

plant7 = Triangle(
    v0=[-1.5, -3.3, -4.95],
    v1=[-1.8, -0.2, -4.95],
    v2=[-1.2, -3.3, -4.95],
    material=green_material
)
rt.scene.append(plant7)

plant8 = Triangle(
    v0=[1.0, -3.5, -4.95],
    v1=[1.3, -1.0, -4.95],
    v2=[0.7, -3.5, -4.95],
    material=green_material
)
rt.scene.append(plant8)

plant9 = Triangle(
    v0=[1.5, -3.4, -4.95],
    v1=[1.8, -0.9, -4.95],
    v2=[1.2, -3.4, -4.95],
    material=light_green_material
)
rt.scene.append(plant9)

plant10 = Triangle(
    v0=[0.8, -3.3, -4.95],
    v1=[1.0, -0.6, -4.95],
    v2=[0.6, -3.3, -4.95],
    material=green_material
)
rt.scene.append(plant10)

rt.Lights.append(AmbientLight(intensity=0.6))

sunlight = DirectionalLight(
    color=[1, 1, 0.9],
    intensity=1.0,
    direction=[-1, -1, -1]
)
rt.Lights.append(sunlight)

star_spotlight = Spotlight(
    color=[1, 0.5, 0.5],
    intensity=1.2,
    position=[0.0, 0.5, -5.5],
    direction=[0, -1, 0],
    innerAngle=20, 
    outerAngle=30
)
rt.Lights.append(star_spotlight)

fish_spotlight = Spotlight(
    color=[1, 1, 0.8],
    intensity=1.0,
    position=[2.0, 0.8, -5.0],
    direction=[0, -1, 0],
    innerAngle=25,
    outerAngle=35
)
rt.Lights.append(fish_spotlight)

eye_and_fin_spotlight = Spotlight(
    color=[1, 1, 0.8],
    intensity=1.5,
    position=[1.5, 0.2, -4.9],
    direction=[0, -1, 0],
    innerAngle=30,
    outerAngle=40
)
rt.Lights.append(eye_and_fin_spotlight)

rt.glRender()

isRunning = True

while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    pygame.display.flip()
    rt.glGenerateFramebuffer("render.bmp")
    clock.tick(60)

pygame.quit()
