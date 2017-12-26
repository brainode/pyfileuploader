class File:
    def __init__(self,filename,filesize,filetype,datemodifided):
        self.filename = filename
        self.filesize = filesize
        self.filetype = filetype
        self.filedatemod = datemodifided
    def __lt__(self, other):
        return len(str(self.filetype))<len(str(other.filetype))