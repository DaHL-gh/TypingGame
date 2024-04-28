import freetype as ft
import moderngl as mgl
import numpy as np

face = ft.Face('RobotoMono-Regular.ttf')
w = 32 << 6
h = 32 << 6
face.set_char_size(w, h)
face.load_char('.')
glyph = face.glyph

x = np.array(glyph.bitmap.buffer) / 255
x = x.reshape((glyph.bitmap.rows, glyph.bitmap.width))

# ctx = mgl.Context()
# texture = ctx.texture(size=(glyph.bitmap.rows, glyph.bitmap.width), data=x, components=1)
print(x)

