import os
import PyPDF2
from tqdm import tqdm
from natsort import natsorted


def merge_pdfs(input_folder, output_filename):
    # Get all PDF files in the folder
    pdf_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.pdf')]

    # Sort files in natural order (1, 2, 3, ..., 10, 11, 12)
    pdf_files = natsorted(pdf_files)

    if not pdf_files:
        print("No PDF files found in the specified directory.")
        return

    merger = PyPDF2.PdfMerger()

    for pdf_file in tqdm(pdf_files, desc="Merging PDFs"):
        merger.append(pdf_file)

    # Write the merged PDF
    with open(output_filename, 'wb') as fout:
        merger.write(fout)

    merger.close()
    print(f"PDFs merged successfully: {output_filename}")
