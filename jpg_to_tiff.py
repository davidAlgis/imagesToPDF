from PIL import Image


def jpeg_to_tiff(jpeg_file, tiff_file):
    """
    Convert a JPEG file to a TIFF file preserving the color profile.
    """
    # Open the JPEG file
    with Image.open(jpeg_file) as img:
        # Ensure the image is loaded properly
        img.load()

        # Save the image as TIFF
        img.save(tiff_file, format='TIFF')
