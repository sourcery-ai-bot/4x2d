from colors import *
import pygame
import pygame.freetype
from resources import resource_path
import spritebase

pygame.freetype.init()

FONTS = {
    'small':pygame.freetype.Font(resource_path("assets/Minecraftia-Regular.ttf"), 8),
    'big':pygame.freetype.Font(resource_path("assets/upheavtt.ttf"), 20),
    'huge':pygame.freetype.Font(resource_path("assets/upheavtt.ttf"), 30)
}

for font in FONTS.values():
    font.antialiased = False

class Text(spritebase.SpriteBase):
    type = None
    def __init__(self, text, size, pos, color = PICO_WHITE, border=False, multiline_width = 80):
        spritebase.SpriteBase.__init__(self, pos)
        self._text = text
        self.size = size
        self.color = color
        self.border = border
        self.multiline_width = multiline_width
        self.set_text(text)
        
    def set_text(self, text):
        self._text = text
        self.update()

    def update(self):
        self.image = render_multiline(self._text, self.size, self.color, self.multiline_width)
        w, h = self.image.get_size()
        self._width = w
        self._height = h
        self.rect = (self.pos.x, self.pos.y, w, h)


def render_multiline(text, size, color, wrap_width=None):
    f = FONTS[size]
    if wrap_width is not None:
        words = text.split(" ")
        new_lines = [words[0]]
        for word in words[1:]:
            l = new_lines[-1] + " " + word
            rect = f.get_rect(l)
            if rect[2] >= wrap_width:
                new_lines.append(word)
            else:
                new_lines[-1] = l
        text = "\n".join(new_lines)

    lines = text.split("\n")
    h = 0
    w = 0
    for line in lines:
        _,_,fw,fh = f.get_rect(line)
        h += fh
        w = max(w, fw)
    h += (len(lines) - 1) * 2
    text_surf = pygame.Surface((w,h), pygame.SRCALPHA)
    y = 0
    for line in lines:
        _,_,fw,fh = f.get_rect(line)
        x = (w - fw) // 2
        f.render_to(text_surf, (x,y), line, color, (0,0,0,0))
        y += fh + 2
    return text_surf