from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template
from werkzeug.utils import secure_filename
from app import core
from collections import namedtuple

app = Flask(
    __name__
)

PathLink = namedtuple('PathLink', ['num', 'name', 'link'])

cor = core.Core()

@app.route("/", defaults={'path': ''},methods=['GET'])
@app.route("/<path:path>",methods=['GET'])
def index(path):
    if cor.ChangeDir(path):
        return render_template("index.html", files=cor.ScanDir(), paths=GetPathParts(), lenpaths=len(GetPathParts()), path=path)
    else:
        return render_template("404.html")

def GetPathParts():
    partpaths = [PathLink(1, 'root', url_for('index'))]
    req = request.path.split('/')
    i = 2
    curpath = ''
    for path in req[1:]:
        curpath += '/' + path
        partpaths.append(PathLink(i, path, url_for('index', path=curpath)))
        i += 1
    return partpaths



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
