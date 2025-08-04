import os
from PyPDF2 import PdfMerger
import img2pdf

def convert_image_to_pdf(img_path, output_path):
    with open(output_path, "wb") as f:
        f.write(img2pdf.convert(img_path))

def merge_files(input_files, output_pdf):
    merger = PdfMerger()
    temp_pdfs = []

    for file in input_files:
        ext = os.path.splitext(file)[1].lower()
        if ext in ['.jpg', '.jpeg', '.png']:
            temp_pdf = f"{file}.pdf"
            convert_image_to_pdf(file, temp_pdf)
            merger.append(temp_pdf)
            temp_pdfs.append(temp_pdf)
        elif ext == '.pdf':
            merger.append(file)
        else:
            print(f"Formato não suportado: {file}")

    merger.write(output_pdf)
    merger.close()

    for temp in temp_pdfs:
        os.remove(temp)

if __name__ == "__main__":
    arquivos = ['eme-12.pdf', 'eme-13.pdf']  # troque pelos seus arquivos reais
    merge_files(arquivos, 'resultado_final.pdf')
    print("✅ PDF final criado com sucesso: resultado_final.pdf")
