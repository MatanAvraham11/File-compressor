from flask import Flask, render_template, request, jsonify, send_file
import os
import zipfile
from datetime import datetime
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Store compression history
HISTORY_FILE = 'compression_history.json'

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Save original file
    original_filename = file.filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    original_path = os.path.join(app.config['UPLOAD_FOLDER'], f'original_{timestamp}_{original_filename}')
    file.save(original_path)

    # Create compressed file
    compressed_filename = f'compressed_{timestamp}_{original_filename}.zip'
    compressed_path = os.path.join(app.config['UPLOAD_FOLDER'], compressed_filename)

    # Compress file
    with zipfile.ZipFile(compressed_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(original_path, original_filename)

    # Calculate compression ratio
    original_size = os.path.getsize(original_path)
    compressed_size = os.path.getsize(compressed_path)
    compression_ratio = ((original_size - compressed_size) / original_size) * 100

    # Update history
    history = load_history()
    history.append({
        'original_name': original_filename,
        'compressed_name': compressed_filename,
        'original_size': original_size,
        'compressed_size': compressed_size,
        'compression_ratio': round(compression_ratio, 2),
        'timestamp': timestamp
    })
    save_history(history)

    # Clean up original file
    os.remove(original_path)

    return jsonify({
        'success': True,
        'compressed_filename': compressed_filename,
        'original_size': original_size,
        'compressed_size': compressed_size,
        'compression_ratio': round(compression_ratio, 2)
    })

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(
        os.path.join(app.config['UPLOAD_FOLDER'], filename),
        as_attachment=True
    )

@app.route('/history')
def get_history():
    return jsonify(load_history())

if __name__ == '__main__':
    app.run(debug=True) 