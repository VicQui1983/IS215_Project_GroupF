import os
import boto3
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)
s3_client = boto3.client('s3', region_name='us-east-1')

BUCKET_NAME = 's215-news-image-buckets'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', title=None, article=None, image_url=None)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('index.html', title="Error", article="No file part", image_url=None)

    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', title="Error", article="No selected file", image_url=None)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        image_key = f'uploads/{filename}'

        try:
            s3_client.upload_fileobj(file, BUCKET_NAME, image_key)
            temp_image_url = f"https://{BUCKET_NAME}.s3.us-east-1.amazonaws.com/{image_key}"
            return render_template('index.html', title="Upload Successful", article="Image uploaded. Article generation pending.", image_url=temp_image_url)

        except Exception as e:
             print(f"Error during upload: {str(e)}")
             return render_template('index.html', title="Error", article=f"An upload error occurred: {str(e)}", image_url=None)

    return render_template('index.html', title="Error", article="Invalid file type", image_url=None)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
