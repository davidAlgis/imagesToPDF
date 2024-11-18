from psd_tools import PSDImage


def psd_to_tiff(psd_file, tif_file):
    """
    Convert a PSD file to a TIFF file preserving the CMYK color profile.
    """
    # Open the PSD file
    psd = PSDImage.open(psd_file)

    # Save the composite image as a CMYK TIFF
    psd.composite().save(tif_file, format='TIFF')
