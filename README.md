# PDF Merger For Azure Functions

An Azure Function for merging multiple PDF files. After deploying to Azure Functions, the sole trigger in this function can be used via a POST request with a .zip file as a form-data *files* variable. The PDF files inside this .zip file will be extracted, merged together and returned as one PDF.

This is an Azure Functions implementation of my original [PDF Merger](https://github.com/Loupeznik/utils/blob/master/www_utils/pdfmerger.py) script.

## Development Setup

### Prerequisites

- Python 3.11
- Azure Functions Core Tools v4

### Initial Setup

1. Run the setup script to create a virtual environment and install dependencies:

```bash
./setup-venv.sh
```

2. Activate the virtual environment:

```bash
source .venv/bin/activate
```

3. When done, deactivate the virtual environment:

```bash
deactivate
```

### Code Quality

This project uses [ruff](https://docs.astral.sh/ruff/) for linting and code formatting.

Run linting:

```bash
ruff check .
```

Run formatting:

```bash
ruff format .
```

## API Response Headers

The function returns the merged PDF as the response body and includes processing metadata in response headers:

- `X-PDF-Total`: Total number of PDF files found in the zip
- `X-PDF-Success-Count`: Number of successfully processed PDFs
- `X-PDF-Failed-Count`: Number of failed PDFs
- `X-PDF-Failed`: JSON array of failed filenames (only included when 10 or fewer failures)

## Testing

See [tests/TESTING.md](tests/TESTING.md) for detailed testing instructions, including:
- How to start the function locally
- Using the provided HTTP test file
- Generating test data
- Understanding response headers
