import os
import PyPDF2
from tqdm import tqdm


def merge_pdfs(input_folder, output_filename):
    pdf_files = sorted([
        os.path.join(input_folder, f) for f in os.listdir(input_folder)
        if f.endswith('.pdf')
    ])

    if not pdf_files:
        print("No PDF files found in the specified directory.")
        return

    merger = PyPDF2.PdfMerger()

    for pdf_file in tqdm(pdf_files, desc="Merging PDFs"):
        merger.append(pdf_file)

    with open(output_filename, 'wb') as fout:
        merger.write(fout)

    merger.close()
    print(f"PDFs merged successfully: {output_filename}")
