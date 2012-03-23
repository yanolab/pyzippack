# -*- coding: utf-8 -*-

import argparse
import zipfile
import glob
import os

def clean(target):
    if not os.path.exists(target):
        return None

    if os.path.isfile(target):
        os.remove(target)
    elif os.path.isdir(target):
        for root, dirs, files in os.walk(target):
            for file in files:
                name, ext = os.path.splitext(file)
                if ext in ['.pyc', '.pyo']:
                    os.remove(os.path.join(root, file))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="compile python files and zip packaging")
    parser.add_argument('target', nargs='*', default='./')
    parser.add_argument('-m', '--main')
    parser.add_argument('-o', '--output', default='target.pyz')
    parser.add_argument('-c', '--clean', nargs='?', default=True)

    args = parser.parse_args()

    with zipfile.PyZipFile(args.output, "w", zipfile.ZIP_DEFLATED) as f:
        f.debug = 2
        for _target in args.target:
            f.writepy(_target)

        if not args.main == None:
            f.writepy(args.main)

    if args.clean:
        for _target in args.target:
            clean(_target)

        if not args.main == None:
            for ext in ['c', 'o']:
                clean(args.main + ext)
