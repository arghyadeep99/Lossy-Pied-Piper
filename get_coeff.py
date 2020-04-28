# pylint: disable=C0103,E0401,W0631
'Compression methods'
import pywt
import numpy as np
from PIL import Image
import utils as util


def extract_rgb_coeff(img):
    """
    Returns RGB dwt applied coefficients tuple
    Parameters
    ----------
    img: PIL Image
    Returns
    -------
    (coeffs_r, coeffs_g, coeffs_b):
        RGB coefficients with Discrete Wavelet Transform Applied
    """
    (width, height) = img.size
    img = img.copy()

    mat_r = np.empty((width, height))
    mat_g = np.empty((width, height))
    mat_b = np.empty((width, height))

    for i in range(width):
        for j in range(height):
            (r, g, b) = img.getpixel((i, j))
            mat_r[i, j] = r
            mat_g[i, j] = g
            mat_b[i, j] = b

    coeffs_r = pywt.dwt2(mat_r, 'haar')
    compressed_r = coeffs_r[0]
    coeffs_g = pywt.dwt2(mat_g, 'haar')
    compressed_g = coeffs_g[0]
    coeffs_b = pywt.dwt2(mat_b, 'haar')
    compressed_b = coeffs_b[0]

    compress_value = np.zeros((compressed_r.shape[0],compressed_r.shape[1],3),'uint8')
    compress_value[..., 0], compress_value[..., 1], compress_value[..., 2] = compressed_r, compressed_g, compressed_b
    compress_thing = Image.fromarray(compress_value)
    compress_thing = compress_thing.rotate(-90)
    compress_thing = compress_thing.transpose(Image.FLIP_LEFT_RIGHT)

    return (coeffs_r, coeffs_g, coeffs_b), compress_thing


def img_from_dwt_coeff(coeff_dwt):

    (coeffs_r, coeffs_g, coeffs_b) = coeff_dwt

    cc = np.array((coeffs_r, coeffs_g, coeffs_b))

    (width, height) = (len(coeffs_r[0]), len(coeffs_r[0][0]))

    #Channel Red
    cARed,cHRed,cVRed,cDRed=np.array(coeffs_r[0]),np.array(coeffs_r[1][0]),np.array(coeffs_r[1][1]),np.array(coeffs_r[1][2])
    # Channel Green
    cAGreen,cHGreen,cVGreen,cDGreen=np.array(coeffs_g[0]),np.array(coeffs_g[1][0]),np.array(coeffs_g[1][1]),np.array(coeffs_g[1][2])
    # Channel Blue
    cABlue, cHBlue, cVBlue, cDBlue=np.array(coeffs_b[0]),np.array(coeffs_b[1][0]),np.array(coeffs_b[1][1]),np.array(coeffs_b[1][2])

    # maxValue per channel per matrix
    cAMaxRed, cAMaxGreen, cAMaxBlue = util.max_ndarray(cARed), util.max_ndarray(cAGreen), util.max_ndarray(cABlue)
    cHMaxRed, cHMaxGreen, cHMaxBlue = util.max_ndarray(cHRed), util.max_ndarray(cHGreen), util.max_ndarray(cHBlue)
    cVMaxRed, cVMaxGreen, cVMaxBlue = util.max_ndarray(cVRed), util.max_ndarray(cVGreen), util.max_ndarray(cVBlue)
    cDMaxRed, cDMaxGreen, cDMaxBlue = util.max_ndarray(cDRed), util.max_ndarray(cDGreen), util.max_ndarray(cDBlue)

    # Image object init
    dwt_img = Image.new('RGB', (width, height), (0, 0, 20))
    # Image reconstruction from cA

    #The image formed from the low frequency of the images which contains the main content of the image

    for i in range(width):
        for j in range(height):
            R, G, B= cARed[i][j], cAGreen[i][j], cABlue[i][j]
            R, G, B = (R/cAMaxRed)*100.0, (G/cAMaxGreen)*100.0, (B/cAMaxBlue)*100.0
            new_value = (int(R), int(G), int(B))
            dwt_img.putpixel((i, j), new_value)
   
    return dwt_img