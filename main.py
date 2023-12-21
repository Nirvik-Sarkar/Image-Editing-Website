import os
from flask import Flask,render_template,request,flash,url_for
from werkzeug.utils import secure_filename
import cv2

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'webp', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key="super secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ProcessImage(filename,operation):
    print(f"the operation name is {operation} and filename is {filename}")
    img=cv2.imread(f"uploads/{filename}")
    if operation=="cgray":
        imgprocessed=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        newFilename=f"static/{filename}"
        cv2.imwrite(newFilename,imgprocessed)
        return newFilename
    elif operation=="cwebp":
        newFilename=f"static/{filename.split('.',1)[0]}.webp"
        cv2.imwrite(newFilename,img)
        return newFilename
    elif operation=="cjpg":
        newFilename=f"static/{filename.split('.',1)[0]}.jpg"
        cv2.imwrite(newFilename,img)
        return newFilename
    elif operation=="cpng":
        newFilename=f"static/{filename.split('.',1)[0]}.png"
        cv2.imwrite(newFilename,img)
        return newFilename
    pass
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def About():
    return render_template("about.html")

@app.route("/edit" , methods=["GET","POST"])
def Edit():
    if request.method == "POST":
        operation=request.form.get("operation")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "error no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new=ProcessImage(filename, operation)
            flash(f"Your image has been processed and is available <a href='/{new}' target='_blank'>here</a>")#target attribute is used here 
            #in anchor tag so that the editted image is opened in a new tab
            return render_template("index.html")

    return render_template("index.html")

app.run(debug=True,port=8000)