import os
from os import listdir
from os.path import isfile, join, dirname, abspath, getmtime, getsize, isdir
import mimetypes
from datetime import datetime

from collections import namedtuple

from operator import itemgetter, attrgetter


Node = namedtuple('Node', ['name', 'type', 'size', 'datemodified', 'weight'])


class Core:
    def __init__(self):
        self.rootPath = '/fileuploader/rootdir'
        self.currientPath = self.rootPath
    def ScanDir(self):
        files = []
        with os.scandir(self.currientPath) as it:
            for entry in it:
                if entry.is_dir():
                    files.append(Node(
                        entry.name,
                        'folder',
                        0,
                        datetime.fromtimestamp(entry.stat().st_mtime),
                        0)
                    )
                else:
                    files.append(Node(
                        entry.name,
                        str(mimetypes.guess_type(entry.path)[0]),
                        entry.stat().st_size,
                        datetime.fromtimestamp(entry.stat().st_mtime),
                        len(str(mimetypes.guess_type(entry.path)[0]))
                    ))
        files.sort(key=attrgetter('weight'))
        return files
    def CreateFolder(self, path, name):
        try:
            os.mkdir(join(join(self.rootPath,path),name))
        except FileExistsError:
            pass
    def SaveFile(self, path, file, name):
        pass
    def ChangeDir(self, path):
        path = join(self.rootPath, path)
        if os.path.exists(path):
            self.currientPath = path
            return True
        else:
            return False
