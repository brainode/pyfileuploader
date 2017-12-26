from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template
from werkzeug.utils import secure_filename
from app import core


app = Flask(
    __name__
)

#Mock
cor = core.PyFileUploader()
files = cor.scan_dir()
#

#@app.route("/")
@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")
def index(path):
    return render_template("index.html", title='Py File Uploader', files=cor.scan_dir(path))

@app.route("/",methods=['POST'])
def upload():
    print(request.files)
    return render_template("index.html", title='Py File Uploader', files=cor.scan_dir(request.path))