import os
from psd_to_png import convert_psd_to_png
from png_to_pdf import png_to_pdf
from pdf_merger import merge_pdfs
from tqdm import tqdm

def create_pdf(input_folder, output_pdf, verso_image=None, split=False):
    os.makedirs("temp_png", exist_ok=True)
    os.makedirs("temp_pdf", exist_ok=True)

    # Convert PSD to PNG
    for psd_file in tqdm([f for f in os.listdir(input_folder) if f.endswith('.psd')], desc="Converting PSD to PNG"):
        convert_psd_to_png(os.path.join(input_folder, psd_file))

    # Convert PNG to PDF
    png_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]
    for png_file in tqdm(png_files, desc="Converting PNG to PDF"):
        png_to_pdf(os.path.join(input_folder, png_file), os.path.join("temp_pdf", f"{os.path.splitext(png_file)[0]}.pdf"), verso_image, split)

    # Merge PDFs
    merge_pdfs("temp_pdf", output_pdf)

    # Clean up temporary files
    for file in os.listdir("temp_png"):
        os.remove(os.path.join("temp_png", file))
    for file in os.listdir("temp_pdf"):
        os.remove(os.path.join("temp_pdf", file))
    os.rmdir("temp_png")
    os.rmdir("temp_pdf")
