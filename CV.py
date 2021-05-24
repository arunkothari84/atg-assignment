from flask import Flask, request
import cv2
import pytesseract

app = Flask(__name__)

pytesseract.pytesseract.tesseract_cmd = r"/app/.apt/usr/bin/tesseract"

@app.route("/predict/", methods=['POST', 'GET'])
def prediction(file):
    if request.method == "GET":
        img = cv2.imread('sample.png')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(img)
        print(text)


if __name__ == '__main__':
    app.run()
