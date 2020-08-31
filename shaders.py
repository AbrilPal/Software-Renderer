from gl import *
from mate import *


def gourad(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = ta.x * u + tb.x * v + tc.x * w
        ty = ta.y * u + tb.y * v + tc.y * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = V3(nx, ny, nz)

    intensity = np.dot(normal, render.light)

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def sombreadoCool(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = ta.x * u + tb.x * v + tc.x * w
        ty = ta.y * u + tb.y * v + tc.y * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = V3(nx, ny, nz)

    intensity = np.dot(normal, render.light)
    if intensity < 0:
        intensity = 0

    b *= intensity
    g *= intensity
    r *= intensity

    if render.active_texture2:
        texColor = render.active_texture2.getColor(tx, ty)

        b += (texColor[0] / 255) * (1 - intensity)
        g += (texColor[1] / 255) * (1 - intensity)
        r += (texColor[2] / 255) * (1 - intensity)


    return r, g, b

def toon(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    tax, tbx, tcx, tay, tby, tcy = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = (nx, ny, nz)

    intensity = punto(normal, render.lightx,render.lighty,render.lightz)

    if (intensity >= 0 and intensity <= 0.15):
        intensity = 0.3
    elif (intensity > 0.15 and intensity <= 0.3):
        intensity = 0.45
    elif (intensity > 0.3 and intensity <= 0.45):
        intensity = 0.6
    elif (intensity > 0.45 and intensity <= 0.6):
        intensity = 0.8
    elif (intensity > 0.6 and intensity <= 0.85):
        intensity = 0.9
    # elif (intensity > 0.9 and intensity<= 1):
    #     intensity = 1
    elif (intensity > 0.85):
        intensity = 1
    else:
        intensity = 0

    b *= intensity
    g *= intensity
    r *= intensity

    print("entro putoss", b, g, r, intensity)

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0
