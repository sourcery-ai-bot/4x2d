from colors import PICO_BLACK, PICO_DARKBLUE, PICO_WHITE
import spritebase
from v2 import V2
import pygame
import text
import resources
import game
from helper import clamp

class Panel(spritebase.SpriteBase):
    def __init__(self, pos, panel_for):
        spritebase.SpriteBase.__init__(self, pos)
        self.panel_for = panel_for
        self._controls = []
        self.padding = 6
        self._background_offset = V2(0,0)

        self.tab = None

    def position_nicely(self, scene):
        x = self.panel_for.x - self._width / 2
        y = self.panel_for.y - self._height / 2
        if x > game.RES[0] / 2:
            x = self.panel_for.x - self.panel_for._width / 2 - self._width - 10
        else:
            x = self.panel_for.x + self.panel_for._width / 2 + 10
        y = clamp(y, 2, game.RES[1] - self._height - 2 - 40)
        self.pos = V2(x,y)
        self._reposition_children()

    def kill(self):
        for ci in self._controls:
            ci['control'].kill()
        spritebase.SpriteBase.kill(self)

    def add(self, control, pos):
        self._controls.append({'control':control,'pos':pos})

    def add_all_to_group(self, group):
        group.add(self)
        for ci in self._controls:
            group.add(ci['control'])

    def _reposition_children(self):
        for ci in self._controls:
            control = ci['control']
            pos = ci['pos']
            control.x = pos.x + self.x + self._background_offset.x
            control.y = pos.y + self.y + self._background_offset.y

    def redraw(self):
        xmin, xmax, ymin, ymax = 0,0,0,0
        for ci in self._controls:
            control = ci['control']
            pos = ci['pos']
            xmax = max(pos.x + control.width, xmax)
            ymax = max(pos.y + control.height, ymax)
        
        box_width = xmax + self.padding * 2
        box_height = ymax + self.padding * 2

        tab_offset = 0
        if self.tab:
            tab_offset = 14

        self.image = pygame.Surface((box_width, box_height + tab_offset), pygame.SRCALPHA)
        pygame.draw.rect(self.image, PICO_DARKBLUE, (0,tab_offset, box_width, box_height), 0)
        self._width = box_width
        self._height = box_height + tab_offset
        pygame.draw.rect(self.image, PICO_WHITE, (0, tab_offset, box_width, box_height), 1)

        if self.tab:
            icon_offset = 0
            icon = None
            if 'icon' in self.tab:
                icon = pygame.image.load(resources.resource_path(self.tab['icon']))
                icon_offset = icon.get_width() + 4            
            tab_text = text.render_multiline(self.tab['text'], 'small', PICO_BLACK)
            tab_width = tab_text.get_size()[0] + 8 + icon_offset
            pygame.draw.rect(self.image, self.tab['color'], (0, 0, tab_width, tab_offset + 1), 0)
            pygame.draw.rect(self.image, PICO_WHITE, (0, 0, tab_width, tab_offset + 1), 1)
            if 'icon' in self.tab:
                self.image.blit(icon, (4,4))
            self.image.blit(tab_text, (4 + icon_offset, 4))

        self._background_offset = V2(self.padding, self.padding + tab_offset)

        self._reposition_children()
        self._recalc_rect()