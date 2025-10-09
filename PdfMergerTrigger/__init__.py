import json
import os
import zipfile

import azure.functions as func
from pypdf import PdfReader, PdfWriter


def main(req: func.HttpRequest) -> func.HttpResponse:
    pdf = PdfWriter()
    files = []
    temp_path = "/tmp/"
    output_filename = "output.pdf"
    success_list = []
    failed_list = []

    if len(req.files) > 1:
        return func.HttpResponse("Too many files", status_code=400)

    for input_file in req.files.values():
        filename = input_file.filename
        contents = input_file.stream.read()

        if not filename:
            return func.HttpResponse("Uploaded file is missing a filename.", status_code=400)

        zip_path = os.path.join(temp_path, filename)
        with open(zip_path, "wb") as temp:
            temp.write(contents)
        try:
            with zipfile.ZipFile(zip_path, "r") as zip_file:
                zip_file.extractall(temp_path)
                files = [
                    f
                    for f in zip_file.namelist()
                    if f.lower().endswith(".pdf")
                    and not f.endswith("/")
                    and not any(part.startswith(".") or part.startswith("__") for part in f.split("/"))
                ]
        except Exception:
            return func.HttpResponse("Uploaded file is not a .zip", status_code=400)

    if not files:
        return func.HttpResponse("No valid PDF files found in the zip archive", status_code=400)

    for filename in files:
        file_path = os.path.join(temp_path, filename)
        try:
            pdf.append(PdfReader(file_path))
            success_list.append(filename)
        except Exception:
            failed_list.append(filename)

    output_path = os.path.join(temp_path, output_filename)
    pdf.write(output_path)

    headers = {
        "X-PDF-Total": str(len(files)),
        "X-PDF-Success-Count": str(len(success_list)),
        "X-PDF-Failed-Count": str(len(failed_list)),
    }

    if len(failed_list) <= 10:
        headers["X-PDF-Failed"] = json.dumps(failed_list)

    if len(pdf.pages) > 0:
        with open(output_path, "rb") as output:
            return func.HttpResponse(output.read(), mimetype="application/pdf", headers=headers)
    else:
        return func.HttpResponse("Merging failed", status_code=400)
