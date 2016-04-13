#!/usr/bin/env python3

import glob
import os.path
import argparse
import subprocess
import tempfile
import shutil
import xml.etree.ElementTree as ET

def unpack(apkfile):
    if not os.path.isfile(apkfile):
        raise ValueError("apkfile {} does not exist".format(apkfile))
    directory = tempfile.mkdtemp()
    subprocess.call(["apktool", "d", "-f", "-o", directory, apkfile])
    return directory


def rename(srcdir, old_name, new_name):
    if old_name == new_name:
        return
    tree = ET.parse('{}/AndroidManifest.xml'.format(srcdir))
    root = tree.getroot()
    manifest_element = next(root.iter("manifest"), None)
    assert manifest_element != None
    assert manifest_element.tag == "manifest"
    assert "package" in manifest_element.attrib.keys()
    assert manifest_element.attrib["package"] == old_name
    manifest_element.attrib["package"] = new_name
    tree.write("{}/AndroidManifest.xml".format(srcdir))


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
