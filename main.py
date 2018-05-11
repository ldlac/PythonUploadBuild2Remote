import os
import pysftp
import argparse

def getFilesFromDirectory(_dir, _sftp, path, first = 0, localBuildFolder = None):
    if path == "":
        path = _dir

    if (not _sftp.exists(_dir) and _dir != localBuildFolder):
        _sftp.mkdir(_dir, mode=755)
        _sftp.chdir(_dir)
        print("Created folder " + _dir)
    for root, dirs, files in os.walk(path):
        for file in files:
            if first == 0:
                print("Created file " + os.path.join(root, file))
                _sftp.put(os.path.join(root, file))
            else:
                print("Created file " + os.path.join(root, file))
                _sftp.put(os.path.join(root, file))
        for dir in dirs:
            getFilesFromDirectory(dir, _sftp, os.path.join(root, dir))
        _sftp.chdir("..")
        break;

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fullpath', required=True, help='Full Path on the remote')
    parser.add_argument('--localdir', required=True, help='Name of the local dir (build dir)')
    args = parser.parse_args()

    username = os.environ.get('MUSIC_DEPLOY_USER')
    password = os.environ.get('MUSIC_DEPLOY_PASS')
    ip = os.environ.get('DEPLOY_SERVER')

    if (username == None or password == None or ip == None):
        print("Environnement variables are not set, MUSIC_DEPLOY_USER, MUSIC_DEPLOY_PASS, DEPLOY_SERVER")
        return 0

    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    with pysftp.Connection(ip, username, password=password, cnopts=cnopts) as sftp:
        with sftp.cd(args.fullpath):
            sftp.execute('rm -rf *')
            try:
                getFilesFromDirectory(args.localdir, sftp, "", 1, args.localdir)
            except:
                print("Upload Unsuccessful")

            print("Upload Successful")
        return 0

import sys

if __name__ == "__main__": sys.exit(main())
