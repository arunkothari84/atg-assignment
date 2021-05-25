from flask import Flask, request,  render_template, flash, send_from_directory
from cv2 import imread, cvtColor, COLOR_BGR2GRAY, threshold, THRESH_OTSU, THRESH_BINARY_INV, getStructuringElement, MORPH_RECT, dilate, findContours, RETR_EXTERNAL, CHAIN_APPROX_NONE,boundingRect, rectangle
import pytesseract
from werkzeug.utils import secure_filename

app = Flask(__name__)

pytesseract.pytesseract.tesseract_cmd = r"./vendor/tesseract-ocr/bin/tesseract"

UPLOAD_FOLDER = '/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def prediction(fname):
    img = imread(uploaded_file(fname))
    gray = cvtColor(img, COLOR_BGR2GRAY)
    ret, thresh1 = threshold(gray, 0, 255, THRESH_OTSU | THRESH_BINARY_INV)
    rect_kernel = getStructuringElement(MORPH_RECT, (18, 18))
    dilation = dilate(thresh1, rect_kernel, iterations = 1)
    contours, hierarchy = findContours(dilation, RETR_EXTERNAL, 
                                             CHAIN_APPROX_NONE)
    im2 = img.copy()
    text = ''
    for cnt in contours:
        x, y, w, h = boundingRect(cnt)
        rect = rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cropped = im2[y:y + h, x:x + w]
        file = open("recognized.txt", "a")
        text = text + pytesseract.image_to_string(cropped) + "<br>"

    return text

def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)    
    
@app.route('/', methods=['GET','POST'])
def hello_world():
   if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return prediction(filename)
   return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload href='/'>   
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=False)
