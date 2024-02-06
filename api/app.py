from flask import Flask, request, flash, redirect, url_for, jsonify
from src.image_utils import process_image_to_info
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes and origins
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit
app.secret_key = os.environ.get('SECRET_KEY', 'optional_default_secret_key')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

@app.route('/')
def home():
    return "Welcome to the eyeagent API!"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/read_ISBN', methods=['POST'])
def read_ISBN():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join('/tmp', filename)
        file.save(filepath)
        # Use your script's functionality
        isbn = process_image_to_info(filepath)
        return jsonify(isbn)


if __name__ == '__main__':
    app.run(debug=True)