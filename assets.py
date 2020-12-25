import pygame as pg

from os.path import join

_sand_top_path = join("assets", "BeachSide-Pinball", "sand_top.png")
_sand_bottom_path = join("assets", "BeachSide-Pinball", "sand_bottom.png")
_border_top_path = join("assets", "BeachSide-Pinball", "bordertop.png")
_border_bottom_path = join("assets", "BeachSide-Pinball", "borderbottom.png")
_pinball_bar_path = join("assets", "BeachSide-Pinball", "pinballbar.png")
_pinball_small_bar_path = join("assets", "BeachSide-Pinball", "pinbalsmallbars.png")
_buttons_path = join("assets", "BeachSide-Pinball", "buttons.png")
_lighthouses_path = join("assets", "BeachSide-Pinball", "lighthouses.png")
_ball_path = join("assets", "ball1.png")


_sand_top_scale = (600, 300)
_sand_bottom_scale = (550, 300)
_border_top_scale = (600, 200)
_border_bottom_scale = (550, 200)
_pinball_bar_scale = (540, 540)
_pinball_small_bar_scale = (440, 330)
_buttons_scale = (200, 100)
_lighthouses_scale = (200, 100)
_ball_scale = (35, 35)


class _Base(pg.sprite.Sprite):

    def __init__(self, image):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()

    def set_position(self, x, y):

        # Change my rectangle

        self.rect.x = x
        self.rect.y = y


class SandTop(_Base):

    def __init__(self):
        image = pg.transform.scale(pg.image.load(
            _sand_top_path).convert_alpha(), _sand_top_scale)
        _Base.__init__(self, image)


class SandBottom(_Base):

    def __init__(self):
        image = pg.transform.scale(pg.image.load(
            _sand_bottom_path).convert_alpha(), _sand_bottom_scale)
        _Base.__init__(self, image)


class BorderTop(_Base):

    def __init__(self):
        image = pg.transform.scale(pg.image.load(
            _border_top_path).convert_alpha(), _border_top_scale)
        _Base.__init__(self, image)


class BorderBottom(_Base):

    def __init__(self):
        image = pg.transform.scale(pg.image.load(
            _border_bottom_path).convert_alpha(), _border_bottom_scale)
        _Base.__init__(self, image)


class PinballBar(_Base):

    def __init__(self):
        image = pg.transform.scale(pg.image.load(
            _pinball_bar_path).convert_alpha(), _pinball_bar_scale)
        _Base.__init__(self, image)


class PinballSmallBar(_Base):

    def __init__(self):
        image = pg.transform.scale(pg.image.load(
            _pinball_small_bar_path).convert_alpha(), _pinball_small_bar_scale)
        _Base.__init__(self, image)


class Buttons(_Base):

    def __init__(self):
        image = pg.transform.scale(pg.image.load(
            _buttons_path).convert_alpha(), _buttons_scale)
        _Base.__init__(self, image)

    
class Lighthouses(_Base):

    def __init__(self):
        image = pg.transform.scale(pg.image.load(
            _lighthouses_path).convert_alpha(), _lighthouses_scale)
        _Base.__init__(self, image)


class Ball(_Base):

    def __init__(self):
        image = pg.transform.scale(pg.image.load(
            _ball_path).convert_alpha(), _ball_scale)
        _Base.__init__(self, image)

        self.rotate_image = image

