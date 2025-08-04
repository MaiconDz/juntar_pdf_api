from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from PyPDF2 import PdfMerger
import img2pdf
import os
import shutil
import uuid

app = FastAPI()

def convert_image_to_pdf(img_bytes, output_path):
    with open(output_path, "wb") as f:
        f.write(img2pdf.convert(img_bytes))

@app.post("/juntar")
async def juntar_arquivos(files: list[UploadFile] = File(...)):
    merger = PdfMerger()
    temp_files = []

    output_pdf_name = f"resultado_{uuid.uuid4().hex}.pdf"

    for file in files:
        filename = file.filename
        ext = os.path.splitext(filename)[1].lower()
        content = await file.read()

        if ext in ['.pdf']:
            temp_path = f"temp_{uuid.uuid4().hex}.pdf"
            with open(temp_path, "wb") as f:
                f.write(content)
            merger.append(temp_path)
            temp_files.append(temp_path)

        elif ext in ['.jpg', '.jpeg', '.png']:
            temp_path = f"temp_{uuid.uuid4().hex}.pdf"
            convert_image_to_pdf(content, temp_path)
            merger.append(temp_path)
            temp_files.append(temp_path)

        else:
            return {"erro": f"Formato não suportado: {filename}"}

    merger.write(output_pdf_name)
    merger.close()

    for f in temp_files:
        os.remove(f)

    return FileResponse(output_pdf_name, media_type='application/pdf', filename=output_pdf_name)
