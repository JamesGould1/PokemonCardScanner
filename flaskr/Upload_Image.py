import os

import cv2
from flask import flash, request, redirect, Blueprint, current_app
from werkzeug.utils import secure_filename
from flaskr.BasicImageRead import *
from flaskr.Preprocess_image import *
from .Process_Text import *

UPLOAD_FOLDER = os.path.join(os.getcwd(), '/User_Files/')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

upload = Blueprint('upload', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            upload_folder = current_app.config['UPLOAD_FOLDER']
            file.save(os.path.join(upload_folder, filename))

            img_array = add_image_process(file.filename)

            # if not os.path.isdir('Processed_Files'):
            #     os.makedirs("Processed_Files")
            #
            # print("ATTEMPTING ON: ", type(img), img.dtype)
            # print(cv2.imwrite(f"Processed_Files/{filename}",img))
            # cv2.imwrite(f"Processed_Files/{filename}",img)
            set_name = request.form.get('set_name')
            shortened_set_name = set_name.split(" ")[0]
            for img in img_array:
                text = load_image(img)
                if not set_name:
                    match = extract_number_from_image(text)
                else:
                    match = extract_number_from_image_with_set(text)
                if match:
                    break

            print(f"{set_name} and {match}")
            final = find_card(shortened_set_name, match)
            if not match:
                return "Please take another photo"
            return final
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <br><br>
      <span>(Optional) <br> Enter set name to improve matches: </span>
      <input type=text name=set_name placeholder="Set Name">
      <input type=submit value=Upload>
    </form>
    '''

