from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import backbone

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "65ZEF4EDC121DF87EQ841S216QZD4Q5S"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Image successfully uploaded and displayed below')
        backbone.forgeryDetector.work('static/uploads/' + filename)
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, gif')
        return redirect(request.url)


@app.route('/display/<filename>_or')
def display_image_original(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/display/<filename>_ela')
def display_image_ela(filename):
    return redirect(url_for('static', filename='uploads/' + filename[:-4] + '_ela.png'), code=301)

@app.route('/display/<filename>_cm')
def display_image_copyMove(filename):
    return redirect(url_for('static', filename='uploads/' + filename[:-4] + '_copyMove.png'), code=301)



if __name__ == "__main__":
    app.run(debug=True)
