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
    def hasPrev(self, page):
        return page > 0
    def hasNext(self, page):
        return page < self.getPagesCount() - 1
    def getPagesCount(self):
        return int(ceil(self.maxItems/self.itemOnPage))
    def appendDots(self):
        self.appendPageLink('#', '...', 'uk-disabled')
    def appendPageLink(self, linkPage, text, cssClass):
        self.ul.append(
            liItem(
                url_for('index', path=request.path, page=linkPage),
                text,
                cssClass
            )
        )
    def isEdgePage(self, page):
        return page == 0 or page == self.getPagesCount() - 1
    def initPaginator(self, page, itemsCount):
        self.page = int(page)
        self.maxItems = int(itemsCount)
        self.ul = []

        self.itemFrom = self.page * self.itemOnPage
        self.itemTo = self.itemFrom + self.itemOnPage

        prevPage = self.page - 1 if self.hasPrev(self.page) else 0
        nextPage = self.page + 1 if self.hasNext(self.page) else self.page

        pages = self.getPagesCount()
        #Append Prev item.Always exist
        self.appendPageLink(prevPage, 'html_PagPrev', 'uk-disabled' if not self.hasPrev(self.page) else '')
        isPlacedLeftDots = False
        isPlacedRightDots = False
        for pageIndex in range(pages):
            if self.page + 2 <= pageIndex and not isPlacedRightDots:
                self.appendDots()
                isPlacedRightDots = True
            if self.isEdgePage(pageIndex):
                self.appendPageLink(pageIndex, str(pageIndex + 1), 'uk-active' if self.page == pageIndex else '')
            if self.page - 2 >= pageIndex and not isPlacedLeftDots:
                self.appendDots()
                isPlacedLeftDots = True
            elif self.page - 2 < pageIndex and self.page + 2 > pageIndex and not self.isEdgePage(pageIndex):
                self.appendPageLink(pageIndex, str(pageIndex + 1), 'uk-active' if self.page == pageIndex else '')
            else:
                continue
        # Append Next item.Always exist
        self.appendPageLink(nextPage, 'html_PagNext', 'uk-disabled' if not self.hasNext(self.page) else '')
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
