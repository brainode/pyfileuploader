from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template
from werkzeug.utils import secure_filename
from app import core
from collections import namedtuple

app = Flask(
    __name__
)

PathLink = namedtuple('PathLink', ['num', 'name', 'link'])

#Mock
cor = core.Core()
#files = cor.scan_dir()
#

@app.route("/", defaults={'path': ''},methods=['GET'])
@app.route("/<path:path>",methods=['GET'])
def index(path):
    cor.ChangeDir(path)
    return render_template("index.html", files=cor.ScanDir(), paths=GetPathParts(), lenpaths=len(GetPathParts()))

def GetPathParts():
    partpaths = [PathLink(1, 'root', url_for('index'))]
    req = request.path.split('/')
    i = 2
    for path in req[1:]:
        partpaths.append(PathLink(i, path, url_for('index', path=path)))
        i += 1
    return  partpaths


if __name__ == '__main__':
    app.run(host='0.0.0.0')


# @app.route("/<path:path>",methods=['POST'])
# def upload(path):
#     f = request.files['file']
#     cor.upload_file(request.files['file'],secure_filename(f.filename))
#     print("Path is: " + path)
#     return index(path)
#     #return index(request.path)
#     #return render_template("index.html", title='Py File Uploader', files=cor.scan_dir(''))
#     #return render_template("index.html", title='Py File Uploader', files=cor.scan_dir(request.path))
#
