#pip install flask opencv-python reportlab
from flask import Flask, render_template, request, flash, redirect
from werkzeug.utils import secure_filename
import cv2
import os
from reportlab.pdfgen import canvas

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp',}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, operation):
    print(f"The operation is {operation} and filename is {filename}")
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename
        case "cwebp":
            newFilename = f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cjpg":
            newFilename = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cjpeg":
            newFilename = f"static/{filename.split('.')[0]}.jpeg"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cpng":
            newFilename = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cpdf":
            newFilename = f"static/{filename.split('.')[0]}.pdf"
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            h, w, _ = img.shape
            c = canvas.Canvas(newFilename, pagesize=(w, h))
            c.drawImage(f"uploads/{filename}", 0, 0, w, h)
            c.save()
            return newFilename
    pass

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/edit", methods=["Get", "POST"])
def edit():
    if request.method == "POST":
        operation = request.form.get("operation")
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return "error no file selected"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            new = processImage(filename, operation)
            flash(f"Your image has been Processed and is avaliable <a href='/{new}' target='_blank'>here</a>")
            return render_template("index.html")

    return render_template("index.html")

            # return redirect(url_for('download_file', name=filename))


    return render_template("index.html")

app.run(debug=True, port=5001)