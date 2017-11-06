import math
from abc import ABC, abstractmethod
from typing import Optional

from shapely.ops import unary_union


class FillAttribs:
    __slots__ = ('color', 'opacity')

    def __init__(self, color, opacity=None):
        self.color = color
        self.opacity = opacity


class StrokeAttribs:
    __slots__ = ('color', 'width', 'min_px', 'opacity')

    def __init__(self, color, width, min_px=None, opacity=None):
        self.color = color
        self.width = width
        self.min_px = min_px
        self.opacity = opacity


class RenderEngine(ABC):
    # draw an svg image. supports pseudo-3D shadow-rendering
    def __init__(self, width: int, height: int, xoff=0, yoff=0, scale=1, buffer=0, background='#FFFFFF'):
        self.width = width
        self.height = height
        self.minx = xoff
        self.miny = yoff
        self.scale = scale
        self.buffer = int(math.ceil(buffer*self.scale))
        self.background = background

        self.maxx = self.minx + width / scale
        self.maxy = self.miny + height / scale

        # how many pixels around the image should be added and later cropped (otherwise rsvg does not blur correctly)
        self.buffer = int(math.ceil(buffer*self.scale))
        self.buffered_width = self.width + 2 * self.buffer
        self.buffered_height = self.height + 2 * self.buffer

        self.background_rgb = tuple(int(background[i:i + 2], 16) for i in range(1, 6, 2))

        # keep track which area of the image has which altitude currently
        self.altitudes = {}
        self.last_altitude = None

    @abstractmethod
    def get_png(self) -> bytes:
        # render the image to png.
        pass

    @staticmethod
    def hex_to_rgb(hexcolor):
        return tuple(int(hexcolor[i:i + 2], 16)/255 for i in range(1, 6, 2))

    def clip_altitudes(self, new_geometry, new_altitude=None):
        # register new geometry with an altitude
        # a geometry with no altitude will reset the altitude information of its area as if nothing was ever there
        if self.last_altitude is not None and self.last_altitude > new_altitude:
            raise ValueError('Altitudes have to be ascending.')

        if new_altitude in self.altitudes:
            self.altitudes[new_altitude] = unary_union([self.altitudes[new_altitude], new_geometry])
        else:
            self.altitudes[new_altitude] = new_geometry

    def add_geometry(self, geometry, fill: Optional[FillAttribs] = None, stroke: Optional[StrokeAttribs] = None,
                     altitude=None, height=None, shape_cache_key=None):
        # draw a shapely geometry with a given style
        # altitude is the absolute altitude of the upper bound of the element
        # height is the height of the element
        # if altitude is not set but height is, the altitude will depend on the geometries below

        # if fill_color is set, filter out geometries that cannot be filled
        if fill is not None:
            try:
                geometry.geoms
            except AttributeError:
                if not hasattr(geometry, 'exterior'):
                    return
            else:
                geometry = type(geometry)(tuple(geom for geom in geometry.geoms if hasattr(geom, 'exterior')))
        if geometry.is_empty:
            return

        self._add_geometry(geometry=geometry, fill=fill, stroke=stroke,
                           altitude=altitude, height=height, shape_cache_key=shape_cache_key)

    @abstractmethod
    def _add_geometry(self, geometry, fill: Optional[FillAttribs] = None, stroke: Optional[StrokeAttribs] = None,
                      altitude=None, height=None, shape_cache_key=None):
        pass