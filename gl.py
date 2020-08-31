# Andrea Abril Palencia Gutierrez, 18198
# SR6: Transformations --- Graficas por computadora, seccion 20
# 17/08/2020 - 24/08/2020

# libreria
import struct
from obj import Obj
from textura import Texture
from mate import normal_fro, resta_lis, division_lis_fro, punto, baryCoords, cruz_lis, mult_M, multiplicacion_M
import numpy as np
from numpy import matrix, cos, sin, tan

# para especificar cuanto tamaño quiero guardar en bytes de cada uno
def char(c):
    # solo un byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    # solo 2 bytes
    return struct.pack('=h', w)

def dword(d):
    # solo 4 bytes
    return struct.pack('=l', d)

def convertir(co):
    # 1 ------ 255
    # x ------ y
    color_r = co * 255
    return int(color_r)
    
def color(r, g, b):
    return bytes([int(b), int(g), int(r)])

# colores predeterminados
rosado = color(4,12,58)
negro = color(0,0,0)
blanco = color(255,255,255)

# clase principal
class Render(object):
    # inicializa cualquier objeto dentro de la clase Render
    def __init__(self, ancho, alto):
        # ancho de la imagen
        #self.ancho = ancho
        # alto de la imagen
        #self.alto = alto
        self.glCreateWindow(ancho, alto)
        # color predeterminado del punto en la pantalla
        self.punto_color = negro
        # luz
        self.lightx=0
        self.lighty=0
        self.lightz=1
        # camara
        self.createViewMatrix()
        self.createProjectionMatrix()

    def createViewMatrix(self, camPosition = (0,1,0), camRotation = (1,1,0)):
        camMatrix = self.createObjectMatrix( translate = camPosition, rotate = camRotation)
        self.viewMatrix = np.linalg.inv(camMatrix)

    def lookAt(self, eye, camPosition = (0,0,0)):
        forward = np.subtract(camPosition, eye)
        forward = forward / np.linalg.norm(forward)

        right = np.cross((0,1,0), forward)
        right = right / np.linalg.norm(right)

        up = np.cross(forward, right)
        up = up / np.linalg.norm(up)

        camMatrix = matrix([[right[0], up[0], forward[0], camPosition[0]],
                            [right[1], up[1], forward[1], camPosition[1]],
                            [right[2], up[2], forward[2], camPosition[2]],
                            [0,0,0,1]])

        self.viewMatrix = np.linalg.inv(camMatrix)

        # adelante = resta_lis(
        #     camPosition[0],ojo[0],
        #     camPosition[1],ojo[1],
        #     camPosition[2],ojo[2])

        # adelante = division_lis_fro(
        #     adelante,
        #     normal_fro(adelante))
        
        # derecha = division_lis_fro(
        #     cruz_lis((0,1,0),adelante),
        #     normal_fro(adelante))

        # arriba = cruz_lis(
        #     adelante, 
        #     derecha)
        # arriba = division_lis_fro(
        #     arriba, 
        #     normal_fro(arriba))

        # camMatrix = [[derecha[0], arriba[0], adelante[0], camPosition[0]],
        #             [derecha[1], arriba[1], adelante[1], camPosition[1]],
        #             [derecha[2], arriba[2], adelante[2], camPosition[2]],
        #             [0,0,0,1]]

        # self.viewMatrix = np.linalg.inv(camMatrix)

    def createProjectionMatrix(self, n = 0.1, f = 1000, fov = 60):
        t = tan((fov * np.pi / 180) / 2) * n
        r = t * self.viewport_ancho / self.viewport_alto
        self.projectionMatrix = [[n / r, 0, 0, 0],
                                [0, n / t, 0, 0],
                                [0, 0, -(f+n)/(f-n), -(2*f*n)/(f-n)],
                                [0, 0, -1, 0]]

    def glCreateWindow(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.glClear()
        self.glViewPort(0, 0, ancho, alto)

    def glViewPort(self, x, y, ancho, alto):
        self.viewport_x = x
        self.viewport_y = y
        self.viewport_ancho = ancho
        self.viewport_alto = alto

        self.viewportMatrix = matrix([[ancho/2, 0, 0, x + ancho/2],
                                      [0, alto/2, 0, y + alto/2],
                                      [0, 0, 0.5, 0.5],
                                      [0, 0, 0, 1]])

    # fondo de toda la imagen
    def glClear(self):
        # color de fondo
        #color_fondo = color_f
        self.pixels = [[rosado for x in range(self.ancho)] for y in range(self.alto)]
        self.zbuffer = [ [ -float('inf') for x in range(self.ancho)] for y in range(self.alto) ]

    # crear un punto en cualquier lugar de la pantalla 
    def glVertex(self, x, y, color = None):
        try:
            self.pixels[y][x] = color or self.punto_color
        except:
            pass

    # permite cambiar el color del punto
    def glColor(self, color_p):
        self.punto_color = color_p

    # hacer lineas
    def  glLine( self , x0 , y0 , x1 , y1 ):
        # coordenasdas en pixeles
        # x0 = int((x0 + 1) * (self.viewport_ancho/2) + self.viewport_x)
        # y0 = int((y0 + 1) * (self.viewport_alto/2) + self.viewport_y)
        # x1 = int((x1 + 1) * (self.viewport_ancho/2) + self.viewport_x)
        # y1 = int((y1 + 1) * (self.viewport_alto/2) + self.viewport_y)

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        inclinado = dy > dx

        if inclinado:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        desplazamiento = 0
        limit = 0.5
        
        # si es division por cero el programa no ejecuta nada
        try:
            m = dy/dx
            y = y0

            for x in range(x0, x1 + 1):
                if inclinado:
                    self.glVertex(y, x)
                else:
                    self.glVertex(x, y)

                desplazamiento += m
                if desplazamiento >= limit:
                    y += 1 if y0 < y1 else -1
                    limit += 1
        except ZeroDivisionError:
            pass

    def transform(self, vertex, vMatrix):
        # augVertex = (vertex[0], vertex[1], vertex[2], 1)
        # # Vt = M * V
        # transVertex = mult_M(augVertex, vMatrix)
        # # Vf = [Vtx/Vtw, Vty/Vtw, Vtz/Vtw]
        # transVertex = (transVertex[0]/transVertex[3],
        #                transVertex[1]/transVertex[3],
        #                transVertex[2]/transVertex[3])
    
        # return transVertex
        # pVertex=[ [vertex[0]], [vertex[1]], [vertex[2]], [1]]
        # a=mult_M(self.viewportMatrix, self.projectionMatrix)
        # b=mult_M(a, self.viewMatrix)
        # c=mult_M(b, vMatrix)
        # pVertex=mult_M(c, pVertex)
        
        
        # pVertex=(pVertex[0][0] / pVertex[3][0] ,
        #         pVertex[1][0] / pVertex[3][0] ,
        #         pVertex[2][0]  / pVertex[3][0] )
        
        # return pVertex

        augVertex = ( vertex[0], vertex[1], vertex[2], 1)
        transVertex = self.viewportMatrix @ self.projectionMatrix @ self.viewMatrix @ vMatrix @ augVertex

        transVertex = transVertex.tolist()[0]

        transVertex = (transVertex[0] / transVertex[3],
                         transVertex[1] / transVertex[3],
                         transVertex[2] / transVertex[3])
        print(transVertex)
        return transVertex


    def dirTransform(self, vertex, vMatrix):#transform para las normales
        fVertex = [ [vertex[0]], [vertex[1]], [vertex[2]], [0]]
        a = mult_M(fVertex, vMatrix)
        fVertex = (a[0][0],
                a[1][0],
                a[2][0])
        return fVertex

    def createObjectMatrix(self, translate = (0,0,0), scale = (1,1,1), rotate=(1,1,0)):
        # matriz de traslacion
        translateMatrix = [[1, 0, 0, translate[0]],
                            [0, 1, 0, translate[1]],
                            [0, 0, 1, translate[2]],
                            [0, 0, 0, 1]]
        # matriz de la escala
        scaleMatrix = [[scale[0], 0, 0, 0],
                        [0, scale[1], 0, 0],
                        [0, 0, scale[2], 0],
                        [0, 0, 0, 1]]
        # matriz de rotacion
        rotationMatrix = self.createRotationMatrix(rotate)
        a = multiplicacion_M(translateMatrix, rotationMatrix, 4,4,4,4)
        b = multiplicacion_M(a, scaleMatrix, 4,4,4,4)
        return b

    def createRotationMatrix(self, rotate=(1,1,0)):
        pitch = np.deg2rad(rotate[0])
        yaw = np.deg2rad(rotate[1])
        roll = np.deg2rad(rotate[2])
        #matriz de rotacion en x
        rotationx = [[1, 0, 0, 0],
                            [0, cos(pitch),-sin(pitch), 0],
                            [0, sin(pitch), cos(pitch), 0],
                            [0, 0, 0, 1]]
        #matriz de rotacion en y
        rotationy = [[cos(yaw), 0, sin(yaw), 0],
                            [0, 1, 0, 0],
                            [-sin(yaw), 0, cos(yaw), 0],
                            [0, 0, 0, 1]]
        #matriz de rotacion en z
        rotationZ = [[cos(roll),-sin(roll), 0, 0],
                            [sin(roll), cos(roll), 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]]
        a=multiplicacion_M(rotationx, rotationy, 4,4,4,4)
        b=multiplicacion_M(a, rotationZ, 4,4,4,4)
        return (b)

    def Model(self, filename, translate, scale):
        modelo = Obj(filename)
        for face in modelo.faces:
            vertCount = len(face)
            for vert in range(vertCount):
                v0 = modelo.vertices[ face[vert][0] - 1 ]
                v1 = modelo.vertices[ face[(vert + 1) % vertCount][0] - 1]
                x0 = int(v0[0] * scale[0]  + translate[0])
                y0 = int(v0[1] * scale[1]  + translate[1])
                x1 = int(v1[0] * scale[0]  + translate[0])
                y1 = int(v1[1] * scale[1]  + translate[1])
                self.glLine(x0, y0, x1, y1)

    # dibujar los poligonos
    def Poligonos(self, vertices):
        self.vertices = vertices
        self.size = len(self.vertices)
        for vertice in range(self.size):
            x0 = self.vertices[vertice][0]
            y0 = self.vertices[vertice][1]
            # colocar las x de los poligonos
            if vertice + 1 < self.size:
                x1 = self.vertices[vertice + 1][0]
            else:
                self.vertices[0][0]
            # colocar las y de los poligonos
            if vertice + 1 < self.size:
                y1 = self.vertices[vertice + 1][1] 
            else:
                self.vertices[0][1]
            # hacer los poligonos, conectando los vertices
            self.glLine(x0, y0, x1, y1)
            # alto y ancho del framebuffer
            for x in range(self.ancho):
                for y in range(self.alto):
                    # regla de par-impar
                    # si retorna que es true pinta el punto
                    if self.Regla(x, y) == True:
                        self.glvertice(x, y)

    # regla impar-par
    def Regla(self, x, y):
        num = self.size
        i = 0
        j = num - 1
        c = False
        for i in range(num):
            if ((self.vertices[i][1] > y) != (self.vertices[j][1] > y)) and \
                    (x < self.vertices[i][0] + (self.vertices[j][0] - self.vertices[i][0]) * (y - self.vertices[i][1]) /
                                    (self.vertices[j][1] - self.vertices[i][1])):
                c = not c
            j = i
        return c

    # hace el zbuffer de la imagen
    def glZBuffer(self, filename):
        imagen = open(filename, 'wb')

        imagen.write(bytes('B'.encode('ascii')))
        imagen.write(bytes('M'.encode('ascii')))
        imagen.write(dword(14 + 40 + self.ancho * self.alto * 3))
        imagen.write(dword(0))
        imagen.write(dword(14 + 40))

        imagen.write(dword(40))
        imagen.write(dword(self.ancho))
        imagen.write(dword(self.alto))
        imagen.write(word(1))
        imagen.write(word(24))
        imagen.write(dword(0))
        imagen.write(dword(self.ancho * self.alto * 3))
        imagen.write(dword(0))
        imagen.write(dword(0))
        imagen.write(dword(0))
        imagen.write(dword(0))

        minZ = float('inf')
        maxZ = -float('inf')
        for x in range(self.alto):
            for y in range(self.ancho):
                if self.zbuffer[x][y] != -float('inf'):
                    if self.zbuffer[x][y] < minZ:
                        minZ = self.zbuffer[x][y]

                    if self.zbuffer[x][y] > maxZ:
                        maxZ = self.zbuffer[x][y]

        for x in range(self.alto):
            for y in range(self.ancho):
                depth = self.zbuffer[x][y]
                if depth == -float('inf'):
                    depth = minZ
                depth = (depth - minZ) / (maxZ - minZ)
                imagen.write(color(depth,depth,depth))

        imagen.close()

    # carga el modelo obj 
    def loadModel(self, filename, translate, scale, texture = None, rotate=(1,1,0)):
        modelo = Obj(filename)
        modelMatrix = self.createObjectMatrix(translate, scale, rotate)
        rotationMatrix = self.createRotationMatrix(rotate)

        for face in modelo.faces:

            vertCount = len(face)
            # v0 = modelo.vertices[ face[0][0] - 1 ]
            # v1 = modelo.vertices[ face[1][0] - 1 ]
            # v2 = modelo.vertices[ face[2][0] - 1 ]

            # x0 = int(v0[0] * scale[0]  + translate[0])
            # y0 = int(v0[1] * scale[1]  + translate[1])
            # z0 = int(v0[2] * scale[2]  + translate[2])
            # x1 = int(v1[0] * scale[0]  + translate[0])
            # y1 = int(v1[1] * scale[1]  + translate[1])
            # z1 = int(v1[2] * scale[2]  + translate[2])
            # x2 = int(v2[0] * scale[0]  + translate[0])
            # y2 = int(v2[1] * scale[1]  + translate[1])
            # z2 = int(v2[2] * scale[2]  + translate[2])

            v0 = modelo.vertices[ face[0][0] - 1 ]
            v1 = modelo.vertices[ face[1][0] - 1 ]
            v2 = modelo.vertices[ face[2][0] - 1 ]
            v0 = self.transform(v0, modelMatrix)
            v1 = self.transform(v1, modelMatrix)
            v2 = self.transform(v2, modelMatrix)

            x0 = v0[0]
            y0 = v0[1]
            z0 = v0[2]
            x1 = v1[0]
            y1 = v1[1]
            z1 = v1[2]
            x2 = v2[0]
            y2 = v2[1]
            z2 = v2[2]

            # x0, x1, x2 = int(v0[0]), int(v1[0]), int(v2[0])
            # y0, y1, y2 = int(v0[1]), int(v1[1]), int(v2[1])
            # z0, z1, z2 = int(v0[2]), int(v1[2]), int(v2[2])

            if vertCount > 3: 
                v3 = modelo.vertices[face[3][0] - 1]
                v3 = self.transform(v3, modelMatrix)
                x3 = v3[0]
                y3 = v3[1]
                z3 = v3[2]

            if texture:
                vt0 = modelo.texcoords[face[0][1] - 1]
                vt1 = modelo.texcoords[face[1][1] - 1]
                vt2 = modelo.texcoords[face[2][1] - 1]
                vt0x = vt0[0]
                vt0y = vt0[1]
                vt1x = vt1[0]
                vt1y = vt1[1]
                vt2x = vt2[0]
                vt2y = vt2[1]
                if vertCount > 3:
                    vt3 = modelo.texcoords[face[3][1] - 1]
                    vt3x = vt3[0]
                    vt3y = vt3[1]
            else:
                vt0x = 0
                vt0y = 0
                vt1x = 0
                vt1y = 0
                vt2x = 0
                vt2y = 0
                vt3x = 0
                vt3y = 0

            vn0 = modelo.normals[face[0][2] - 1]
            vn1 = modelo.normals[face[1][2] - 1]
            vn2 = modelo.normals[face[2][2] - 1]
            vn0 = self.dirTransform(vn0, rotationMatrix)
            vn1 = self.dirTransform(vn1, rotationMatrix)
            vn2 = self.dirTransform(vn2, rotationMatrix)
            if vertCount > 3:
                vn3 = modelo.normals[face[3][2] - 1]
                vn3 = self.dirTransform(vn3, rotationMatrix)

            self.triangle_bc(x0, x1, x2, y0, y1, y2, z0, z1, z2, vt0x, vt1x, vt2x, vt0y, vt1y, vt2y, texture = texture)
            if vertCount > 3:
                self.triangle_bc(x0, x2, x3, y0, y2, y3, z0, z2, z3, vt0x, vt2x, vt3x, vt0y, vt2y, vt3y, texture = texture)

            # if vertCount > 3:
            #     self.triangle_bc(x0, x2, x3, y0, y2, y3, z0, z2, z3, vt0x, vt2x, vt3x, vt0y, vt2y, vt3y, texture = texture, intensity = intensity)           
            
    #Barycentric Coordinates
    def triangle_bc(self, Ax, Bx, Cx, Ay, By, Cy, Az, Bz, Cz, tax, tbx, tcx, tay, tby, tcy, _color = rosado, texture = None):
        minx = round(min(Ax, Bx, Cx))
        miny = round(min(Ay, By, Cy))
        maxx = round(max(Ax, Bx, Cx))
        maxy = round(max(Ay, By, Cy))

        for x in range(minx, maxx + 1):
            for y in range(miny, maxy + 1):
                if x >= self.ancho or x < 0 or y >= self.alto or y < 0:
                    continue
                u, v, w = baryCoords(Ax, Bx, Cx, Ay, By, Cy, x,y)

                if u >= 0 and v >= 0 and w >= 0:
                    z = Az * u + Bz * v + Cz * w
                    if z > self.zbuffer[y][x]:
                        b, g , r = _color 
                        b /= 255
                        g /= 255
                        r /= 255

                        if texture:
                            tx = tax * u + tbx * v + tcx * w
                            ty = tay * u + tby * v + tcy * w

                            texColor = texture.getColor(tx, ty)
                            b *= texColor[0] / 255
                            g *= texColor[1] / 255
                            r *= texColor[2] / 255

                        self.glVertex(x, y, texColor)
                        self.zbuffer[y][x] = z

    # escribe el imagen
    def glFinish(self, name):
        imagen = open(name, 'wb')
        imagen.write(bytes('B'.encode('ascii')))
        imagen.write(bytes('M'.encode('ascii')))
        imagen.write(dword(14 + 40 + self.ancho * self.alto * 3))
        imagen.write(dword(0))
        imagen.write(dword(14 + 40))
        imagen.write(dword(40))
        imagen.write(dword(self.ancho))
        imagen.write(dword(self.alto))
        imagen.write(word(1))
        imagen.write(word(24))
        imagen.write(dword(0))
        imagen.write(dword(self.ancho * self.alto * 3))
        imagen.write(dword(0))
        imagen.write(dword(0))
        imagen.write(dword(0))
        imagen.write(dword(0))

        for x in range(self.alto):
            for y in range(self.ancho):
                imagen.write(self.pixels[x][y])
                
        imagen.close()
