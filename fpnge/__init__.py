from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from numpy.typing import NDArray
	from PIL.Image import Image
	from cv2 import Mat
import fpnge.binding
import fpnge.binding

def fromPIL(im: 'Image') -> bytes:
	mode_map = {
	  "L":    (1, 8),
	  "RGB":  (3, 8),
	  "RGBA": (4, 8),
	  "PA":   (2, 8),
	  "RGBX": (4, 8),
	}
	if im.mode not in mode_map:
		conv_map = {
		  "1": "L",
		  "P": "RGBA",
		  "CMYK": "RGB",
		  "YCbCr": "RGB",
		  "LAB": "RGB",
		  "HSV": "RGB",
		  "LA": "RGBA",
		  "RGBa": "RGBA",
		  "La": "PA",
		}
		im = im.convert(mode=conv_map[im.mode])
	
	imbytes = im.tobytes()
	return fpnge.binding.encode_bytes(imbytes, im.width, im.height, *mode_map[im.mode])

def frombytes(bytes, width, height, channels, bits_per_channel, stride=0) -> bytes:
	return fpnge.binding.encode_bytes(bytes, width, height, channels, bits_per_channel, stride)

def fromNP(ndarray: 'NDArray') -> bytes:
	if ndarray.ndim != 3:
		raise Exception("Must have 3 dimensions (height x width x channels)")
	# This definition of shape agrees with: https://numpy.org/doc/stable/reference/generated/numpy.ndarray.shape.html#numpy.ndarray.shape
	return fpnge.binding.encode_view(ndarray.data, ndarray.shape[1], ndarray.shape[0], ndarray.shape[2], ndarray.dtype.itemsize * 8)

def fromMat(mat: 'Mat') -> bytes:
	try:
		import cv2
	except ImportError as _:
		raise ImportError("Cannot use fromMat without opencv-python installed")
	if mat.ndim != 3:
		raise Exception("Must have 3 dimensions (width x height x channels)")
	# cv2 Mats are BGR, needs to be RGB:
	mat = cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)
	return fromNP(mat)

def fromview(view: memoryview, width=0, height=0, channels=0, bits_per_channel=0, stride=0) -> bytes:
	if stride == 0 and width == 0:
		stride = view.strides[0]
	if width == 0:
		width = view.shape[0]
	if height == 0:
		height = view.shape[1]
	if channels == 0:
		channels = view.shape[2]
	if bits_per_channel == 0:
		bits_per_channel = view.itemsize * 8
	return fpnge.binding.encode_view(view, width, height, channels, bits_per_channel, stride)

