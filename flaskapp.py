import os
from flask import Flask, render_template, request, url_for, send_from_directory
from stat import *
import time, sys, platform, datetime
from werkzeug.utils import secure_filename
from PIL import Image

APP_ROOT = os.path.dirname('/home/ubuntu/images')
APP_ROOT_DELETE = os.path.dirname('/home/ubuntu/images/')
ALLOWED_EXTENSIONS = set (['pdf','png', 'jpg','jpeg'])

app = Flask(__name__)
app.config['APP_ROOT'] = APP_ROOT
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 *1024
app.debug = True

def allowed_file(filename):
        return '.' in filename and \
                           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def autodelete():
    for filename in os.listdir('/home/ubuntu/images'):
        fullPath = os.path.join(APP_ROOT_DELETE, filename)
        stat = os.stat(fullPath)
        mtime = stat.st_mtime
        current_time= time.time()
        if (mtime<= current_time -300):
            os.remove(fullPath)
    return render_template("upload.html")
       
@app.route("/")
def index():
    autodelete()
    return render_template("upload.html")


@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    print(target)
    
    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        if file and allowed_file(filename):
            destination = "/".join([target, filename])
            print(destination)
            file.save(destination)
            return render_template("upload.html", upload_files=os.listdir("/home/ubuntu/images"))
        else:
            return render_template("upload.html", upload_files=os.listdir("/home/ubuntu/images"))

@app.route("/upload/<path:filename>")
def send_file(filename):
    return send_from_directory("/home/ubuntu/images/",filename)

@app.route("/delete/<path:filename>")
def delete_file(filename):
    print("hello")
    fullPath = os.path.join(APP_ROOT_DELETE, filename)
    if os.path.exists(fullPath):
      os.remove(fullPath)
    return render_template('upload.html', upload_files=os.listdir("/home/ubuntu/images"))

@app.route("/properties/<path:filename>")
def checkfiletype(filename):
    if '.jpg' in filename or '.png' in filename or '.jpeg' in filename:
        fullPath = os.path.join(APP_ROOT_DELETE, filename)
        stat = os.stat(fullPath)
        image = Image.open(fullPath,'r')
        resolution = image.size
        pixel= image.load()
        pixels=(pixel[0,1])

        return render_template('upload.html', upload_files= os.listdir("/home/ubuntu/images"),
        mtime=time.ctime(stat.st_mtime), img_resolution=resolution, ctime=time.ctime(stat.st_mtime),size=stat.st_size,pix=pixels)
    else:
        fullPath = os.path.join(APP_ROOT_DELETE, filename)
        stat = os.stat(fullPath)
        return render_template('upload.html', upload_files= os.listdir("/home/ubuntu/images"),
        mtime=time.ctime(stat.st_mtime),ctime=time.ctime(stat.st_mtime),size=stat.st_size)

@app.errorhandler(413)
def page_not_found(e):
    return "You are trying to upload a file with filesize greater than 2mb, Please go back and try some other file", 413

if __name__ == "__main__":
    app.run()
