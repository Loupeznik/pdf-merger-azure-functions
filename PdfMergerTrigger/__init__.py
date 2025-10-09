import azure.functions as func

from PyPDF2 import PdfMerger, PdfReader
import zipfile

def main(req: func.HttpRequest) -> func.HttpResponse:
    pdf = PdfMerger()
    files = []
    temp_path = '/tmp/'
    output_filename = "output.pdf"

    if (len(req.files) > 1):
        return func.HttpResponse(
             "Too many files",
             status_code=400
        )

    for input_file in req.files.values():
        filename = input_file.filename
        contents = input_file.stream.read()

        with open(temp_path + filename, 'wb') as temp:
            temp.write(contents)
        try:
            with zipfile.ZipFile(temp_path + filename, 'r') as zip:
                zip.extractall(temp_path)
                files = zip.namelist()
        except:
            return func.HttpResponse(
                "Uploaded file is not a .zip",
                status_code=400
        )

    for filename in files:
        pdf.append(PdfReader(temp_path + filename))

    pdf.write(temp_path + output_filename)   

    if len(pdf.pages) > 0:
        with open(temp_path + output_filename, 'rb') as output:
            return func.HttpResponse(output.read(), mimetype="application/pdf")
    else:
        return func.HttpResponse(
             "Merging failed",
             status_code=400
        )
