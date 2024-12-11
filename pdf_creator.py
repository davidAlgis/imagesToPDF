import os
import shutil
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
from tiff_to_pdf import tiff_to_pdf
from png_jpeg_to_pdf import image_to_pdf
from pdf_merger import merge_pdfs


def process_psd(psd_file, temp_dir, dpi):
    """Convert PSD to TIFF and then to PDF."""
    from psd_tools import PSDImage
    tif_file = os.path.join(
        temp_dir, f"{os.path.splitext(os.path.basename(psd_file))[0]}.tiff")
    pdf_file = tif_file.replace('.tiff', '.pdf')

    # Convert PSD to TIFF
    psd = PSDImage.open(psd_file)
    psd.composite().save(tif_file, format='TIFF')

    # Convert TIFF to PDF
    tiff_to_pdf(tif_file, pdf_file, dpi=dpi)
    os.remove(tif_file)  # Clean up intermediate TIFF
    return pdf_file


def process_image(image_file, temp_dir, verso_image, split, dpi):
    """Convert an image file (JPEG or PNG) to PDF."""
    pdf_file = os.path.join(
        temp_dir, f"{os.path.splitext(os.path.basename(image_file))[0]}.pdf")
    image_to_pdf(image_file, pdf_file, verso_image, split, dpi)
    return pdf_file


def copy_pdf(pdf_file, temp_dir):
    """Copy an existing PDF to the temp directory."""
    dest_file = os.path.join(temp_dir, os.path.basename(pdf_file))
    shutil.copy(pdf_file, dest_file)
    return dest_file


def create_pdf(input_paths,
               output_pdf,
               verso_image=None,
               split=False,
               dpi=300):
    """
    Create a PDF from input files or a folder.

    :param input_paths: List of input file paths or a folder path
    :param output_pdf: Path to the output PDF
    :param verso_image: Optional verso image
    :param split: Split PDF pages
    :param dpi: Resolution for PDF creation
    """
    temp_dir = os.path.abspath("temp_pdf")
    os.makedirs(temp_dir, exist_ok=True)

    if isinstance(input_paths, str) and os.path.isdir(input_paths):
        # Handle folder input
        input_paths = [
            os.path.join(input_paths, f) for f in os.listdir(input_paths)
        ]

    psd_files = [f for f in input_paths if f.endswith('.psd')]
    image_files = [
        f for f in input_paths if f.lower().endswith(('.jpg', '.jpeg', '.png'))
    ]
    pdf_files = [f for f in input_paths if f.endswith('.pdf')]

    # Check if there are any files to process
    if not psd_files and not image_files and not pdf_files:
        print("No valid files (PSD, JPEG, PNG, or PDF) found to process.")
        return

    tasks = []

    with ProcessPoolExecutor() as executor:
        # Submit tasks for PSD processing
        for psd_file in psd_files:
            tasks.append(executor.submit(process_psd, psd_file, temp_dir, dpi))

        # Submit tasks for image (JPEG/PNG) processing
        for image_file in image_files:
            tasks.append(
                executor.submit(process_image, image_file, temp_dir,
                                verso_image, split, dpi))

        # Submit tasks for copying PDFs
        for pdf_file in pdf_files:
            tasks.append(executor.submit(copy_pdf, pdf_file, temp_dir))

        # Use tqdm to track progress
        for future in tqdm(as_completed(tasks),
                           total=len(tasks),
                           desc="Processing files"):
            try:
                future.result()  # Ensure exceptions are raised if any
            except Exception as e:
                print(f"Error processing file: {e}")

    # Merge PDFs
    merge_pdfs(temp_dir, output_pdf)

    # Clean up temporary files
    shutil.rmtree(temp_dir)
