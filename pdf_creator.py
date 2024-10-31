import os
from psd_to_png import convert_psd_to_png
from picture_to_pdf import picture_to_pdf  # Updated import to match the renamed file
from pdf_merger import merge_pdfs
from tqdm import tqdm
import shutil


def create_pdf(input_path, output_pdf, verso_image=None, split=False):
    # Create temporary directories
    os.makedirs("temp_png", exist_ok=True)
    os.makedirs("temp_pdf", exist_ok=True)

    # Check if input_path is a file or a directory
    if os.path.isfile(input_path):
        file_ext = os.path.splitext(input_path)[1].lower()
        # If it's a PSD file, convert it to PNG
        if file_ext == '.psd':
            png_file = convert_psd_to_png(input_path)
            picture_to_pdf(
                png_file,
                os.path.join(
                    "temp_pdf",
                    f"{os.path.splitext(os.path.basename(png_file))[0]}.pdf"),
                verso_image, split)
        # If it's an image file (PNG, JPG, JPEG), convert directly to PDF
        elif file_ext in ['.png', '.jpg', '.jpeg']:
            picture_to_pdf(
                input_path,
                os.path.join(
                    "temp_pdf",
                    f"{os.path.splitext(os.path.basename(input_path))[0]}.pdf"
                ), verso_image, split)
        # If it's a PDF file, copy it to the temp_pdf folder
        elif file_ext == '.pdf':
            shutil.copy(input_path,
                        os.path.join("temp_pdf", os.path.basename(input_path)))
        else:
            print(
                "Unsupported file format. Please provide a PNG, JPG, JPEG, PSD, or PDF file."
            )
            return
    else:
        # Process as a directory
        for psd_file in tqdm(
            [f for f in os.listdir(input_path) if f.endswith('.psd')],
                desc="Converting PSD to PNG"):
            convert_psd_to_png(os.path.join(input_path, psd_file))

        image_files = [
            f for f in os.listdir(input_path)
            if f.endswith(('.png', '.jpg', '.jpeg'))
        ]
        for image_file in tqdm(image_files, desc="Converting images to PDF"):
            picture_to_pdf(
                os.path.join(input_path, image_file),
                os.path.join("temp_pdf",
                             f"{os.path.splitext(image_file)[0]}.pdf"),
                verso_image, split)

        pdf_files = [f for f in os.listdir(input_path) if f.endswith('.pdf')]
        for pdf_file in tqdm(pdf_files, desc="Copying existing PDFs"):
            shutil.copy(os.path.join(input_path, pdf_file),
                        os.path.join("temp_pdf", pdf_file))

    # Merge PDFs
    merge_pdfs("temp_pdf", output_pdf)

    # Clean up temporary files
    for file in os.listdir("temp_png"):
        os.remove(os.path.join("temp_png", file))
    for file in os.listdir("temp_pdf"):
        os.remove(os.path.join("temp_pdf", file))
    os.rmdir("temp_png")
    os.rmdir("temp_pdf")
