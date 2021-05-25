from flask import Flask, request,  render_template
import cv2
import pytesseract

app = Flask(__name__)

pytesseract.pytesseract.tesseract_cmd = r"/app/.apt/usr/bin/tesseract"

@app.route("/predict/", methods=['POST', 'GET'])
def prediction():
    if request.method == "GET":
        img = cv2.imread('sample.png')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(img)
        return 'succcess'

@app.route('/')
def hello_world():
   return render_template('index.html')

if __name__ == '__main__':
    app.run()
