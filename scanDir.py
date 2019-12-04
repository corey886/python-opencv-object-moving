import os
import sys
import time
import datetime


def checkFolder(isFolder):
    try:
        files = os.listdir(isFolder)
        subs = len(files)
        if subs < 1:
            print('empty folder >>' + isFolder)
            os.rmdir(isFolder)
    except:
        print('can not checkFolder >>' + isFolder)

    return''


def checkFile(isFile):
    # https://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python
    # https://www.runoob.com/python/os-stat.html

    try:
        (mode, ino, dev, nlink, uid, gid, size,
         atime, mtime, ctime) = os.stat(isFile)
        fDatetime = datetime.datetime.fromtimestamp(ctime)

        deleteTime = fDatetime+datetime.timedelta(days=21)

        now = datetime.datetime.now()

        if now > deleteTime:
            print('file datetime is out of bound >>' + isFile)
            os.remove(isFile)
    except:
        print('can not checkFile >>' + isFile)

    return ''


def scanDir(rootpath):
    for entry in os.scandir(rootpath):
        try:
            if entry.is_dir():
                scanDir(entry.path)
                checkFolder(entry.path)
            elif entry.is_file():
                checkFile(entry.path)
        except:
            print('can not read >>' + entry.path)

    return ''
