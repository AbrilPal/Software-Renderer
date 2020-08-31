# Andrea Abril Palencia Gutierrez, 18198
# SR6: Transformations --- Graficas por computadora, seccion 20
# 17/08/2020 - 24/08/2020

from gl import Render
from obj import Obj 
from textura import Texture
from shaders import *

modelo = Render(2160,1920)
fondo = Texture('./models/noche.bmp')
modelo.pixels = fondo.pixels
posModel = (210, 220, -400)
modelo.lookAt(posModel, (5, 5, 0))
# modelo.loadModel('./models/model.obj', posModel, (1,1,1),(0,0,0))
# # piso
# textura = Texture('./models/madera.bmp')
# modelo.loadModel('./models/piso.obj', (290,-61,-400), (13, 5, 1), textura, (0, 0, 0))
# # hombre
# textura = Texture('./models/hombre.bmp')
# modelo.loadModel('./models/hombre.obj', (20, -12, -460), (1, 1, 1), textura, (0, 30, 20))
# # faro
# textura3 = Texture('./models/faro_L.bmp')
# modelo.loadModel('./models/faro.obj', (350, 2, -460), (5, 5, 5), textura3, (0, 0, 0))
# # # banca 
# textura = Texture('./models/metal_dec.bmp')
# modelo.loadModel('./models/bench_bright.obj', (440, 50, -400), (8, 6, 6), textura, (0, -20, 0))
# # mujer
# textura = Texture('./models/mujer.bmp')
# modelo.loadModel('./models/mujer.obj', (400, -2, -460), (0.15, 0.15, 0.15), textura, (1, 160, 0))
# luna
# modelo.active_texture = Texture('./models/luna-imagenes.bmp')
modelo.active_shader = toon
modelo.active_texture = Texture('./models/luna-imagenes.bmp')
modelo.loadModel('./models/earth.obj', (50, 800, -800), (0.1, 0.1, 0.1), (5, 20, 0))
modelo.glFinish('modelo_obj.bmp')
print("¡Listo! La imagen esta creada con el nombre de 'modelo_obj.bmp'.")