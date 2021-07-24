# PDF Merger For Azure Functions
An Azure Function for merging multiple PDF files. After deploying to Azure Functions, the sole trigger in this function can be used via a POST request with a .zip file as a form-data *files* variable. The PDF files inside this .zip file will be extracted, merged together and returned as one PDF.

This is an Azure Functions implementation of my original [PDF Merger](https://github.com/Loupeznik/utils/blob/master/www_utils/pdfmerger.py) script.