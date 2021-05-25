from flask import Flask, request,  render_template
from cv2 import imread, cvtColor, COLOR_BGR2RGB, threshold, THRESH_OTSU, THRESH_BINARY_INV, getStructuringElement, MORPH_RECT, dilate, findContours, RETR_EXTERNAL, CHAIN_APPROX_NONE,boundingRect, rectangle
import pytesseract

app = Flask(__name__)

pytesseract.pytesseract.tesseract_cmd = r"./vendor/tesseract-ocr/bin/tesseract"

@app.route("/predict/", methods=['POST', 'GET'])
def prediction():
    if request.method == "GET":
        img = imread('sample.png')
        img = cvtColor(img, COLOR_BGR2RGB)
        ret, thresh1 = threshold(gray, 0, 255, THRESH_OTSU | THRESH_BINARY_INV)
        rect_kernel = getStructuringElement(MORPH_RECT, (18, 18))
        dilation = dilate(thresh1, rect_kernel, iterations = 1)
        contours, hierarchy = findContours(dilation, RETR_EXTERNAL, 
                                                 CHAIN_APPROX_NONE)
        for cnt in contours:
            x, y, w, h = boundingRect(cnt)
            rect = rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cropped = im2[y:y + h, x:x + w]
            file = open("recognized.txt", "a")
            text = pytesseract.image_to_string(cropped) + "\n"
        im2 = img.copy()
        return text

@app.route('/')
def hello_world():
   return render_template('./index.html')

if __name__ == '__main__':
    app.run(debug=False)
