from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import sys
from PIL import Image
import pytesseract
import argparse
import cv2

__author__ = 'Rick Torzynski <ricktorzynski@gmail.com>'
__source__ = ''

app = Flask(__name__)
UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']

      filename = secure_filename(f.filename)

      filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
      f.save(filepath)
    
      image = cv2.imread(filepath)
      gray = cv2.cvtColor(image, cv2.COLOR_)
      
      gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

      gray = cv2.medianBlur(gray, 3)

      ofilename = os.path.join(app.config['UPLOAD_FOLDER'],"{}.png".format(os.getpid()))
      cv2.imwrite(ofilename, gray)
    
      text = pytesseract.image_to_string(Image.open(ofilename))
      
      os.remove(ofilename)

      return {'text': text}

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(debug=True, host='0.0.0.0', port=port)
