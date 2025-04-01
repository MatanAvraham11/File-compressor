# File Compressor

A simple web application for compressing files with a clean and intuitive user interface.

## Features

- Drag and drop file upload
- File compression with ZIP format
- Compression ratio display
- Download compressed files
- Compression history sidebar
- Modern and clean UI

## Setup

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Navigate to the project directory:
   ```bash
   cd file_compressor
   ```

2. Run the Flask application:
   ```bash
   python app.py
   ```

3. Open your web browser and go to:
   ```
   http://localhost:5000
   ```

## Usage

1. Drag and drop a file into the upload area or click to select a file
2. Wait for the compression to complete
3. View the compression results and download the compressed file
4. Access previously compressed files from the history sidebar

## Notes

- Maximum file size is limited to 16MB
- Compressed files are stored in the `uploads` directory
- Compression history is stored in `compression_history.json` 