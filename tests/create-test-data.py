#!/usr/bin/env python3
import os
import zipfile

TEST_DATA_DIR = "test-data"
VALID_DIR = os.path.join(TEST_DATA_DIR, "valid")
INVALID_DIR = os.path.join(TEST_DATA_DIR, "invalid")


def create_simple_pdf(filename, content="Test PDF"):
    pdf_content = f"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/Resources <<
/Font <<
/F1 <<
/Type /Font
/Subtype /Type1
/BaseFont /Helvetica
>>
>>
>>
/MediaBox [0 0 612 792]
/Contents 4 0 R
>>
endobj
4 0 obj
<<
/Length 44
>>
stream
BT
/F1 12 Tf
100 700 Td
({content}) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000317 00000 n
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
409
%%EOF
"""
    with open(filename, "wb") as f:
        f.write(pdf_content.encode())


def create_invalid_pdf(filename):
    with open(filename, "w") as f:
        f.write("This is not a valid PDF file, just plain text.")


def main():
    os.makedirs(VALID_DIR, exist_ok=True)
    os.makedirs(INVALID_DIR, exist_ok=True)

    print("Creating valid PDF files...")
    for i in range(1, 4):
        pdf_path = os.path.join(VALID_DIR, f"test{i}.pdf")
        create_simple_pdf(pdf_path, f"Test PDF #{i}")
        print(f"  Created: {pdf_path}")

    print("\nCreating zip with valid PDFs...")
    with zipfile.ZipFile("test-data/valid-pdfs.zip", "w") as zipf:
        for i in range(1, 4):
            pdf_filename = f"test{i}.pdf"
            pdf_path = os.path.join(VALID_DIR, pdf_filename)
            zipf.write(pdf_path, pdf_filename)
    print("  Created: test-data/valid-pdfs.zip")

    print("\nCreating invalid PDF file...")
    invalid_pdf_path = os.path.join(INVALID_DIR, "invalid.pdf")
    create_invalid_pdf(invalid_pdf_path)
    print(f"  Created: {invalid_pdf_path}")

    print("\nCreating valid PDFs for mixed test...")
    valid_pdf1 = os.path.join(INVALID_DIR, "valid1.pdf")
    valid_pdf2 = os.path.join(INVALID_DIR, "valid2.pdf")
    create_simple_pdf(valid_pdf1, "Valid PDF #1")
    create_simple_pdf(valid_pdf2, "Valid PDF #2")
    print(f"  Created: {valid_pdf1}")
    print(f"  Created: {valid_pdf2}")

    print("\nCreating zip with one invalid PDF...")
    with zipfile.ZipFile("test-data/mixed-pdfs.zip", "w") as zipf:
        zipf.write(valid_pdf1, "valid1.pdf")
        zipf.write(invalid_pdf_path, "invalid.pdf")
        zipf.write(valid_pdf2, "valid2.pdf")
    print("  Created: test-data/mixed-pdfs.zip")

    print("\nTest data creation complete!")
    print("\nTest files created:")
    print("  - test-data/valid-pdfs.zip (3 valid PDFs)")
    print("  - test-data/mixed-pdfs.zip (2 valid PDFs + 1 invalid PDF)")


if __name__ == "__main__":
    main()
