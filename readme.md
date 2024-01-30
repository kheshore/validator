This is a Flask application that allows users to upload files (specifically images of mark sheets) and form data, processes the images to extract marks using OCR (Optical Character Recognition), compares the extracted marks with the ones provided in the form, and stores the form data along with the comparison result in a MongoDB database.

Key components:

1. **Flask Setup**: Flask is a web framework for Python. An instance of Flask is created and configured with an upload folder, a secret key, and a MongoDB URI.

2. **MongoDB Setup**: PyMongo is a Python driver for MongoDB. A PyMongo instance is created with the Flask app instance.

3. **Routes**: There are three routes defined:
   - `'/'`: This route handles both GET and POST requests. For POST requests, it processes the uploaded files and form data, compares the marks, and stores the data in MongoDB. For GET requests, it simply renders a template.
   - `'/success'`: This route handles GET requests and renders a success template.
   - `'/validate_file'`: This route handles POST requests, processes an uploaded file and form data, compares the marks, and returns a JSON response.

4. **Image Processing**: OpenCV is used to read the images and crop them to a region of interest (ROI). PyTesseract is used to perform OCR on the cropped images and extract the marks.

5. **Data Storage**: The form data along with the comparison result is stored in a MongoDB database.

6. **Running the App**: The Flask app is run with debug mode enabled.

-----------------------------------------------------------------------------------------------

TO INSTALL & RUN:

1. Ensure you have Python installed on your system. If not, you can download it from the [official Python website](https://www.python.org/downloads/).

2. Clone the repository or download the project files to your local system.

3. Navigate to the project directory in your terminal.

4. Install the required Python packages using pip (Python's package installer). The required packages are listed in the [`requirements.txt`](command:_github.copilot.openRelativePath?%5B%22requirements.txt%22%5D "requirements.txt") file. Run the following command:

```sh
pip install -r requirements.txt
```

5. Run the Flask application using the following command:

```sh
python app.py
```

6. Open a web browser and navigate to `http://localhost:5000` to access the application.

