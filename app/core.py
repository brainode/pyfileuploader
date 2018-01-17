import os
from os.path import join
import mimetypes
from datetime import datetime
from werkzeug.utils import secure_filename
from collections import namedtuple
from operator import attrgetter
from transliterate import translit

Node = namedtuple('Node', ['name', 'type', 'size', 'datemodified', 'weight'])

DiskSpace = namedtuple('DiskSpace', ['free', 'used', 'total', 'style'])

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
                        round(entry.stat().st_size/1000000, 2),
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
    def DiskUsage(self):
        diskSt = os.statvfs(self.currientPath)
        free = round(diskSt.f_bavail * diskSt.f_frsize / (1024 ** 2), 2)
        total = round(diskSt.f_blocks * diskSt.f_frsize / (1024 ** 2), 2)
        used = ((diskSt.f_blocks - diskSt.f_bfree) * diskSt.f_frsize) / (1024 ** 2)
        if used/total*100 > 90:
            style = 'uk-progress-danger'
        elif used/total*100 > 70:
            style = 'uk-progress-warning'
        else:
            style = 'uk-progress-success'
        return DiskSpace(free, used, total, style)

# def disk_usage(path):
#
#     st = os.statvfs(path)
#     free = st.f_bavail * st.f_frsize
#     total = st.f_blocks * st.f_frsize
#     used = (st.f_blocks - st.f_bfree) * st.f_frsize
#     return _ntuple_diskusage(total, used, free)