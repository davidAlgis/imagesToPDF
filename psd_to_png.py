import os
from tqdm import tqdm
from psd_tools import PSDImage


def convert_psd_to_png(psd_file):
    psd_image = PSDImage.open(psd_file)
    png_file = psd_file.replace('.psd', '.png')
    psd_image.composite().save(png_file)
    return png_file
