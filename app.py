from flask import Flask, request, render_template, redirect, url_for, flash
import os
import cv2
import numpy as np
import pytesseract

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['SECRET_KEY'] = 'secret-key'  # replace 'your-secret-key' with your actual secret key

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['image']
        marks = request.form['marks']
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        # Process the image and compare the marks
        imgQ = cv2.imread(filename)  # Use the path of the uploaded file
        if imgQ is None:
            flash('Failed to load the image')
            return redirect(request.url)
        h,w,c = imgQ.shape
        orb = cv2.ORB_create(1000)
        kp1, des1 = orb.detectAndCompute(imgQ,None)
        img = cv2.imread(filename)
        if img is None:
            flash('Failed to load the uploaded image')
            return redirect(request.url)
        kp2, des2 = orb.detectAndCompute(img, None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        matches = bf.match(des2, des1)
        # Extract marks from the image
        roi = [(710, 1146), (810, 1204), ' text', 'Marks']
        imgCrop = img[roi[0][1]:roi[1][1], roi[0][0]:roi[1][0]]
        extracted_marks = pytesseract.image_to_string(imgCrop)
        # Compare marks and matches here
        # If they match, save to database and flash a success message
        if int(marks) == int(extracted_marks):
            flash('Marks and matches are correct!')
        else:
            flash('Marks and matches are incorrect!')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)