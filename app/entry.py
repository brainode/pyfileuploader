from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template
from app import core
from collections import namedtuple
from math import ceil

app = Flask(
    __name__
)

app.config['MAX_CONTENT_LENGTH'] = 5120 * 1024 * 1024

PathLink = namedtuple('PathLink', ['num', 'name', 'link'])

#paginator block
liItem = namedtuple('liItem', ['link', 'showText', 'cssClass'])

class Paginator:
    def __init__(self):
        self.itemOnPage = 12
        self.page = 0
        self.itemFrom = 0
        self.itemTo = self.itemOnPage
        self.maxItems = 0
        self.ul = []
    def hasPrev(self):
        return self.page > 1
    def hasNext(self):
        return self.page < self.getPagesCount() - 1
    def getPagesCount(self):
        return int(ceil(self.maxItems/self.itemOnPage))
    def initPaginator(self, page, itemsCount):
        self.page = int(page)
        self.maxItems = int(itemsCount)
        self.ul = []

        self.itemFrom = self.page * self.itemOnPage
        self.itemTo = self.itemFrom + self.itemOnPage

        prevPage = self.page - 1 if self.hasPrev() else 0
        nextPage = self.page + 1 if self.hasNext() else 0

        pages = self.getPagesCount()
        #Append Prev item.Always exist
        self.ul.append(liItem(
                        url_for('index', path=request.path, page=prevPage),
                        'html_PagPrev',
                        'uk-disabled' if not self.hasPrev() else ''
                    )
        )
        # Append first item.Always exist
        self.ul.append(liItem(
                            url_for('index', path=request.path, page=0),
                            '1',
                            'uk-active' if self.page == 0 else ''
                        )
        )
        if self.getPagesCount() > 5:
            self.ul.append(liItem(
                            '#',
                            '...',
                            'uk-disabled'
                        )
            )
        for pageIndex in range(1, pages):
            self.ul.append(liItem(
                            url_for('index', path=request.path, page=pageIndex),
                            pageIndex+1,
                            'uk-active' if self.page == pageIndex else ''
                        )
            )
            if self.getPagesCount() > 5 and pageIndex == pages-2:
                self.ul.append(liItem(
                    '#',
                    '...',
                    'uk-disabled'
                )
            )
        # Append next item.Always exist
        self.ul.append(liItem(
                            url_for('index', path=request.path, page=nextPage),
                            'html_PagNext',
                            'uk-disabled' if not self.hasNext() else ''
                        )
        )
###end paginator block


cor = core.Core()
pag = Paginator()

@app.route("/", defaults={'path': ''},methods=['GET'])
@app.route("/<path:path>",methods=['GET'])
def index(path):
    files = cor.ScanDir()
    try:
        page = request.args['page']
    except Exception:
        page = 0
    pag.initPaginator(page, len(files))
    if cor.ChangeDir(path):
        return render_template("index.html", files=files, paths=GetPathParts(), lenpaths=len(GetPathParts()), path=path, paginator=pag)
    else:
        return render_template("404.html")

@app.route("/", defaults={'path': ''},methods=['POST'])
@app.route("/<path:path>",methods=['POST'])
def Action(path):
    try:
        action = request.args['action']
        if action == 'CreateFolder':
            CreateFolder(path)
        elif action == 'Upload':
            UploadFiles(path)
    except Exception:
        pass
    return index(path)


def CreateFolder(path):
    try:
        folderName = request.form['foldername']
        cor.CreateFolder(folderName)
    except:
        #Show error message
        pass
    return index(path)


def UploadFiles(path):
    try:
        file = request.files['file']
        cor.SaveFile(file)
    except:
        #Show error message
        pass
    return index(path)

#Bread crumbs generating
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
