import os
from os import listdir
from os.path import isfile, join, dirname, abspath, getmtime, getsize
from app.file import File
import mimetypes
from datetime import datetime


class PyFileUploader:
    rootdir = '/fileuploader/rootdir'
    def __init__(self):
        self.curpath = self.rootdir
        self.scan_dir()
        pass
    def scan_dir(self,path=rootdir):
        path = join(self.rootdir,path) if len(path)>0 else self.rootdir
        files = [File(f,getsize(join(path,f))//1000000,mimetypes.guess_type(join(path,f))[0],datetime.fromtimestamp(getmtime(join(path,f)))) for f in listdir(path)]
        files.sort()
        return files
        # for f in files:
        #      print(f.filename)
        #      print(f.filetype[0])
        #      print(f.filesize)
        #      print(f.filedatemod)
    def upload_file(self,file):
        pass