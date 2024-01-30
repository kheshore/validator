from flask import Flask, request, render_template, redirect, url_for, flash, session, jsonify
from flask_pymongo import PyMongo
import os
import cv2
import numpy as np
import pytesseract

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['SECRET_KEY'] = 'secret-key'
app.config['MONGO_URI'] = 'mongodb+srv://kheshore:qo5tKxMEJn3jK3dX@validator.vpl6fz1.mongodb.net/validator?retryWrites=true&w=majority'
mongo = PyMongo(app)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    messages = []
    comparison_result = False
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        mobile = request.form['mobile']
        tenth_marks = request.form['10th_marks']
        twelfth_marks = request.form['12th_marks']
        tenth_marksheet = request.files['10th_marksheet']
        twelfth_marksheet = request.files['12th_marksheet']

        # Save the uploaded files
        tenth_filename = os.path.join(app.config['UPLOAD_FOLDER'], tenth_marksheet.filename)
        twelfth_filename = os.path.join(app.config['UPLOAD_FOLDER'], twelfth_marksheet.filename)
        tenth_marksheet.save(tenth_filename)
        twelfth_marksheet.save(twelfth_filename)

        # Process the images and compare the marks
        tenth_img = cv2.imread(tenth_filename)
        twelfth_img = cv2.imread(twelfth_filename)
        if tenth_img is None or twelfth_img is None:
            flash('Failed to load the images', 'error')
            return redirect(request.url)

        # Extract marks from the images
        roi = [(710, 1146), (810, 1204)]  # example ROI coordinates
        tenth_img_crop = tenth_img[roi[0][1]:roi[1][1], roi[0][0]:roi[1][0]]
        twelfth_img_crop = twelfth_img[roi[0][1]:roi[1][1], roi[0][0]:roi[1][0]]
        extracted_tenth_marks = pytesseract.image_to_string(tenth_img_crop)
        extracted_twelfth_marks = pytesseract.image_to_string(twelfth_img_crop)

        # Compare marks and matches here
        if int(tenth_marks) == int(extracted_tenth_marks):
            messages.append(('10th marks are correct!', 'success'))
            comparison_result = True
        else:
            messages.append(('10th marks are incorrect!', 'error'))

        if int(twelfth_marks) == int(extracted_twelfth_marks):
            messages.append(('12th marks are correct!', 'success'))
            comparison_result = comparison_result and True
        else:
            messages.append(('12th marks are incorrect!', 'error'))
            comparison_result = False

        # Insert the form data into MongoDB
        mongo.db.applications.insert_one({
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'mobile': mobile,
            '10th_marks': tenth_marks,
            '12th_marks': twelfth_marks,
            'comparison_result': comparison_result
        })
    if (request.method == 'POST'):
        return redirect(url_for('success'))

    return render_template('index.html', messages=messages, comparison_result=comparison_result)

@app.route('/success', methods=['GET'])
def success():
    return render_template('success.html')

@app.route('/validate_file', methods=['POST'])
def validate_file():
    file = request.files['file']
    marks = request.form['marks']
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)
    img = cv2.imread(filename)
    if img is None:
        return jsonify({'message': 'Failed to load the image', 'success': False})
    roi = [(710, 1146), (810, 1204)]
    img_crop = img[roi[0][1]:roi[1][1], roi[0][0]:roi[1][0]]
    extracted_marks = pytesseract.image_to_string(img_crop)
    if int(marks) == int(extracted_marks):
        return jsonify({'message': 'Marks are correct!', 'success': True})
    else:
        return jsonify({'message': 'Marks are incorrect!', 'success': False})

if __name__ == '__main__':
    app.run(debug=True)