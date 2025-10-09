# Testing Guide

This guide explains how to test the PDF Merger Azure Function locally.

## Prerequisites

- Azure Functions Core Tools v4
- Python 3.11 virtual environment set up (see README.md)

## Starting the Function Locally

1. Activate the virtual environment:

```bash
source .venv/bin/activate
```

2. Start the Azure Functions runtime:

```bash
func start
```

The function will be available at `http://localhost:7071/api/PdfMergerTrigger`

## Generating Test Data

Generate test PDF files and zip archives from the project root:

```bash
python3 tests/create-test-data.py
```

This creates:
- `test-data/valid-pdfs.zip` - Contains 3 valid PDF files
- `test-data/mixed-pdfs.zip` - Contains 2 valid PDFs and 1 invalid PDF

## Testing Methods

### Method 1: Using HTTP File (VS Code REST Client)

If you have the [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) installed in VS Code:

1. Open `tests/tests.http`
2. Click "Send Request" above any test case
3. View the response in the output panel

### Method 2: Using curl

#### Test with valid PDFs:

```bash
curl -X POST \
  http://localhost:7071/api/PdfMergerTrigger \
  -F "file=@test-data/valid-pdfs.zip" \
  -o output-valid.pdf \
  -i
```

#### Test with mixed valid/invalid PDFs:

```bash
curl -X POST \
  http://localhost:7071/api/PdfMergerTrigger \
  -F "file=@test-data/mixed-pdfs.zip" \
  -o output-mixed.pdf \
  -i
```

The `-i` flag includes response headers in the output, and `-o` saves the merged PDF.

### Method 3: Using Postman/Insomnia

1. Create a new POST request to `http://localhost:7071/api/PdfMergerTrigger`
2. Set body type to `form-data`
3. Add a file field named `file`
4. Upload one of the test zip files
5. Send the request

## Understanding Response Headers

The function returns processing metadata in custom HTTP headers:

| Header | Description |
|--------|-------------|
| `X-PDF-Total` | Total number of PDF files found in the zip archive |
| `X-PDF-Success-Count` | Number of PDFs successfully processed and merged |
| `X-PDF-Failed-Count` | Number of PDFs that failed to process |
| `X-PDF-Failed` | JSON array of failed filenames (only included when ≤10 failures) |

### Example Response Headers

**All valid PDFs:**
```
X-PDF-Total: 3
X-PDF-Success-Count: 3
X-PDF-Failed-Count: 0
```

**Mixed valid/invalid PDFs:**
```
X-PDF-Total: 3
X-PDF-Success-Count: 2
X-PDF-Failed-Count: 1
X-PDF-Failed: ["invalid.pdf"]
```

## Expected Behaviors

### Successful Cases

1. **All valid PDFs** - Returns merged PDF with status 200
   - All PDFs are merged in the order they appear in the zip
   - Success count equals total count

2. **Mixed valid/invalid PDFs** - Returns merged PDF with status 200
   - Valid PDFs are merged successfully
   - Invalid PDFs are skipped (not included in output)
   - Headers show which files failed

### Error Cases

1. **No PDF files in zip** - Returns 400 with message "No valid PDF files found in the zip archive"

2. **Invalid zip file** - Returns 400 with message "Uploaded file is not a .zip"

3. **Multiple files uploaded** - Returns 400 with message "Too many files"

4. **Missing filename** - Returns 400 with message "Uploaded file is missing a filename."

5. **All PDFs invalid** - Returns 400 with message "Merging failed"

## Verifying Merged PDFs

After downloading the merged PDF, verify it by opening it:

```bash
# macOS
open output-valid.pdf

# Linux
xdg-open output-valid.pdf
```

## Filtering and File Selection

The function automatically filters out:
- Hidden files (starting with `.`)
- macOS metadata files (`__MACOSX/`)
- Directory entries in the zip
- Non-PDF files

Only valid `.pdf` files are processed.

## Troubleshooting

### Function not starting

Check that:
- Virtual environment is activated
- All dependencies are installed (`pip install -r requirements.txt`)
- Port 7071 is not already in use

### Test data not found

Run the test data generation script from the project root:
```bash
python3 tests/create-test-data.py
```

### Invalid PDFs not being rejected

This is expected behavior - invalid PDFs are skipped, and the function continues processing valid PDFs. Check the `X-PDF-Failed` header to see which files were skipped.
