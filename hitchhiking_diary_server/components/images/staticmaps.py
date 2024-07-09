# py-staticmaps
# Based on the ImageMarker from py-staticmaps
# Copyright (c) 2020 Florian Pigorsch; see /LICENSE for licensing information

import io
import typing

import s2sphere
from PIL import Image
from staticmaps import ImageMarker, Object


class CustomImageMarker(ImageMarker):
    def __init__(self, latlng: s2sphere.LatLng, file: str, size: typing.Tuple[int, int]) -> None:
        Object.__init__(self)
        self._latlng = latlng
        self._file = file
        self._origin_x = 0
        self._origin_y = 0
        self._width = 0
        self._height = 0
        self._size = size
        self._image_data: typing.Optional[bytes] = None

    def load_image_data(self) -> None:
        """Load image data for the image marker"""
        with open(self._file, "rb") as f:
            self._image_data = f.read()
        image = Image.open(io.BytesIO(self._image_data))
        image.thumbnail(self._size, Image.Resampling.LANCZOS)

        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        self._image_data = buffer.getvalue()

        self._width, self._height = image.size
