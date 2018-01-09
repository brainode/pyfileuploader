import os
from os.path import join
import mimetypes
from datetime import datetime
from werkzeug.utils import secure_filename
from collections import namedtuple
from operator import attrgetter
from transliterate import translit,get_available_language_codes

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
    def CreateFolder(self, name):
        try:
            os.mkdir(join(self.currientPath,name))
        except FileExistsError:
            pass
        except Exception:
            pass
    def SaveFile(self, file):
        filename = translit(file.filename, 'ru', reversed=True)
        filename = secure_filename(filename)
        file.save(join(self.currientPath, filename))
    def ChangeDir(self, path):
        path = join(self.rootPath, path)
        if os.path.exists(path):
            self.currientPath = path
            return True
        else:
            return False
