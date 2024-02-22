from flask import Flask, request, render_template, redirect, url_for, flash, session, jsonify
from flask_pymongo import PyMongo
import os
import cv2
import numpy as np
import pytesseract

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['SECRET_KEY'] = 'secret-key'
app.config['MONGO_URI'] = 'mongodb+srv://swathi:qo5tKxMEJn3jK3dX@validator.vpl6fz1.mongodb.net/validator?retryWrites=true&w=majority'
mongo = PyMongo(app)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    mobile = request.form['mobile']
    tenth_marks = request.form['10th_marks']
    twelfth_marks = request.form['12th_marks']
    
    try:
        mongo.db.applications.insert_one({
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'mobile': mobile,
            '10th_marks': tenth_marks,
            '10th_sheet_marks': tenth_marks,
            '12th_marks': twelfth_marks,
            '12th_sheet_marks':twelfth_marks
        })
        print('Data uploaded successfully!')
    except Exception as e:
        print(f'Failed to upload data: {str(e)}')

    return redirect(url_for('success'))

@app.route('/success', methods=['GET'])
def success():
    return render_template('success.html')

@app.route('/validate_file', methods=['POST'])
def validate_file():
    file = request.files['file']
    marks = request.form['marks']
    mtype = request.form['type']
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)
    img = cv2.imread(filename)
    if img is None:
        return jsonify({'message': 'Failed to load the image', 'success': False})
    
    # Define different ROIs for 10th and 12th marks
    roi_10th = [(710, 1146), (810, 1204)]
    roi_12th = [(530, 1166), (686, 1214)]
    roi = roi_10th if mtype == '10th' else roi_12th

    img_crop = img[roi[0][1]:roi[1][1], roi[0][0]:roi[1][0]]
    extracted_marks = pytesseract.image_to_string(img_crop)
    
    if (mtype == '10th' and int(marks) < 350) or (mtype == '12th' and int(marks) < 420):
        return jsonify({'message': 'Marks are below expectation', 'success': False, 'extracted_marks': extracted_marks})
    else:
        if int(marks) == int(extracted_marks):
            return jsonify({'message': 'Marks are correct!', 'success': True, 'extracted_marks': extracted_marks})
        else:
            return jsonify({'message': 'Marks are incorrect!', 'success': False , 'extracted_marks': extracted_marks})

if __name__ == '__main__':
    app.run(debug=True)