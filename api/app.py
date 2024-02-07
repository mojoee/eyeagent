from flask import Flask, request, flash, redirect, url_for, jsonify
from src.image_utils import process_image_to_info
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
from src.call_API import getImageLabels
from src.utils import uploadImage

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


@app.route('/storeImage', methods=['POST'])
def storeImage():
    file = request.form['file']
    supabasePath = request.form['supabasePath']
    content = file.read()
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join('images', filename)
        print(filepath)
        uploadImage(content, bucket="images", path_on_supastorage=supabasePath, content_type="image/jpeg")
        return {"message": "Image uploaded successfully!"}
    else:
        return None


@app.route('/readISBN', methods=['POST'])
def readISBN():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join('/tmp', filename)
        file.save(filepath)
        # Use your script's functionality
        isbn = process_image_to_info(filepath)
        return jsonify(isbn)


@app.route('/readImage', methods=['POST'])
def readImage():
    uri = request.text['uri']
    if uri:
        labels = getImageLabels(uri)
        # use labels to make a suggestion


if __name__ == '__main__':
    app.run(debug=True)