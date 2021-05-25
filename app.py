from flask import Flask, request,  render_template
from cv2 import imread, cvtColor, COLOR_BGR2RGB
import pytesseract

app = Flask(__name__)

pytesseract.pytesseract.tesseract_cmd = r"./vendor/tesseract-ocr/share/tessdata"

@app.route("/predict/", methods=['POST', 'GET'])
def prediction():
    if request.method == "GET":
        img = imread('sample.png')
        img = cvtColor(img, COLOR_BGR2RGB)
        text = pytesseract.image_to_string(img)
        return 'succcess'

@app.route('/')
def hello_world():
   return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)
