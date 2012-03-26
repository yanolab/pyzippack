# -*- coding: utf-8 -*-

import argparse
import zipfile
import glob
import os

def _compile_and_write2zip(zio, filename):
    name, ext = os.path.splitext(filename)

    if ext == '.py':
        _compile(filename, '__main__.pyc', zio.debug)
        zio.write('__main__.pyc')
        if zio.debug > 0: print 'Adding', '__main__.pyc'
    elif ext in ['.pyc', '.pyo']:
        zio.write(filename, '__main__' + ext)

def _compile(pyfile, pycfile, debug=0):
    import py_compile
    if debug > 0: print 'Compiling', pyfile
    py_compile.compile(pyfile, pycfile, None, True)

def _write_main(zio, mainfile):
    import functools

    ftable = {
        "__main__.py": f.writepy,
        "__main__.pyc": f.write,
        "__main__.pyo": f.write,
        }

    deffunc = functools.partial(_compile_and_write2zip, zio)
    func = ftable.get(mainfile, deffunc)
    func(mainfile)

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
            _write_main(f, args.main)

    if args.clean:
        import glob
        for tmpfile in glob.glob("*.py[c|o]"):
            os.remove(tmpfile)
