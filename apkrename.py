#!/usr/bin/env python3

import glob
import os.path
import argparse
import subprocess
import tempfile
import shutil


def unpack(apkfile):
    if not os.path.isfile(apkfile):
        raise ValueError("apkfile {} does not exist".format(apkfile))
    directory = tempfile.mkdtemp()
    subprocess.call(["apktool", "d", "-f", "-o", directory, apkfile])
    return directory


def rename(srcdir, old_name, new_name):
    if old_name == new_name:
        return
    with open("{}/AndroidManifest.xml".format(srcdir), 'r+') as manifest:
        data = manifest.read()
        manifest.seek(0)
        manifest.truncate()
        manifest.write(data.replace(old_name, new_name))
    files = glob.glob("{}/smali/**/*.smali".format(srcdir), recursive=True)
    old_name_smali_syntax = "L{}".format(old_name.replace('.', '/'))
    new_name_smali_syntax = "L{}".format(new_name.replace('.', '/'))
    for smalifile in files:
        with open(smalifile, 'r+') as sf:
            data = sf.read()
            sf.seek(0)
            sf.truncate()
            sf.write(data.replace(old_name_smali_syntax, new_name_smali_syntax))


def pack(srcdir, name):
    subprocess.call(["apktool", "b", "-o", "modified_{}.apk".format(name), srcdir])


def main():
    parser = argparse.ArgumentParser(description='Rename android package names')
    parser.add_argument("apk", help="apkfile to modify")
    parser.add_argument("current_name", help="current package name")
    parser.add_argument("new_name", help="new package name")
    args = parser.parse_args()
    directory = unpack(args.apk)
    rename(directory, args.current_name, args.new_name)
    pack(directory, args.new_name)
    shutil.rmtree(directory)


if __name__ == '__main__':
    main()
