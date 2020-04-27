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
    compress_value[..., 0] = compressed_r
    compress_value[..., 1] = compressed_g
    compress_value[..., 2] = compressed_b
    #print(compress_value.shape)
    compress_thing = Image.fromarray(compress_value)
    compress_thing = compress_thing.rotate(-90)
    compress_thing = compress_thing.transpose(Image.FLIP_LEFT_RIGHT)
    #compress_thing.save('well.jpg')
    return (coeffs_r, coeffs_g, coeffs_b), compress_thing


def img_from_dwt_coeff(coeff_dwt):
    """
    Returns Image recreated from dwt coefficients
    Parameters
    ----------
    (coeffs_r, coeffs_g, coeffs_b):
        RGB coefficients with Discrete Wavelet Transform Applied
    Returns
    -------
    Image from dwt coefficients
    """
    # Channel Red
    (coeffs_r, coeffs_g, coeffs_b) = coeff_dwt

    cc = np.array((coeffs_r, coeffs_g, coeffs_b))

    (width, height) = (len(coeffs_r[0]), len(coeffs_r[0][0]))

    cARed = np.array(coeffs_r[0])
    cHRed = np.array(coeffs_r[1][0])
    cVRed = np.array(coeffs_r[1][1])
    cDRed = np.array(coeffs_r[1][2])
    # Channel Green
    cAGreen = np.array(coeffs_g[0])
    cHGreen = np.array(coeffs_g[1][0])
    cVGreen = np.array(coeffs_g[1][1])
    cDGreen = np.array(coeffs_g[1][2])
    # Channel Blue
    cABlue = np.array(coeffs_b[0])
    cHBlue = np.array(coeffs_b[1][0])
    cVBlue = np.array(coeffs_b[1][1])
    cDBlue = np.array(coeffs_b[1][2])

    # maxValue per channel per matrix
    cAMaxRed = util.max_ndarray(cARed)
    cAMaxGreen = util.max_ndarray(cAGreen)
    cAMaxBlue = util.max_ndarray(cABlue)

    cHMaxRed = util.max_ndarray(cHRed)
    cHMaxGreen = util.max_ndarray(cHGreen)
    cHMaxBlue = util.max_ndarray(cHBlue)

    cVMaxRed = util.max_ndarray(cVRed)
    cVMaxGreen = util.max_ndarray(cVGreen)
    cVMaxBlue = util.max_ndarray(cVBlue)

    cDMaxRed = util.max_ndarray(cDRed)
    cDMaxGreen = util.max_ndarray(cDGreen)
    cDMaxBlue = util.max_ndarray(cDBlue)

    # Image object init
    dwt_img = Image.new('RGB', (width, height), (0, 0, 20))
    # cA reconstruction

    '''
    The image formed from the low frequency of the images which contains the main content of the image
    '''
    for i in range(width):
        for j in range(height):
            R = cARed[i][j]
            R = (R/cAMaxRed)*100.0
            G = cAGreen[i][j]
            G = (G/cAMaxGreen)*100.0
            B = cABlue[i][j]
            B = (B/cAMaxBlue)*100.0
            new_value = (int(R), int(G), int(B))
            dwt_img.putpixel((i, j), new_value)
   
    return dwt_img