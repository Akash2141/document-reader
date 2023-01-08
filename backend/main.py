import os
from flask import Flask, request
from flask_cors import CORS
from doc_crop import extract_doc

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "./upload/"


@app.route('/read', methods=['POST'])
def welcome():
    file = request.files['file']
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    return extract_doc(filepath)


if __name__ == '__main__':
    app.run(port=8000)
