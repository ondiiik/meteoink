#!/usr/bin/python3
import glob
import os
import struct
import zlib
import git
from pathlib import Path


root = Path(os.getcwd()).resolve()


class Builder:
    def __init__(self, dst, variant):
        self.cwd = root.joinpath('..', 'micropython').resolve()
        self.dwd = root.joinpath(dst, variant).resolve()
        self.fw = root.joinpath('meteoink.fw')
        self.mpc = str(root.joinpath('mpy-cross')) + ' -v -march=xtensawin'
        self.repo = git.Repo(search_parent_directories=True)
        self.sha = self.repo.head.object.hexsha.encode()
        self.variant = variant

    def __call__(self, cleanup=False):
        try:
            with open(Path(self.cwd, 'main.py'), 'w') as f:
                f.write(f'''from ulogging import getLogger, dump_exception
logger = getLogger('main')

try:
    logger.info('Starting the application ...')
    from app import run
    run({self.sha})
    
except KeyboardInterrupt as e:
    dump_exception('Interrupted by keyboard ...', e)
except BaseException as e:
    dump_exception('!!! APPLICATION ERROR - REBOOTING !!!', e)
    import machine
    machine.reset()
''')

            with open(Path(self.cwd, 'setup', 'display.py'), 'w') as f:
                f.write(f'''from .epd_{self.variant} import *
# from .epd_bwy import *
# from .epd_acep import *
''')

            if cleanup:
                self.command(f'rm -Rf {self.dwd}')

            self.command(f'mkdir {self.dwd}')

            self.copy('boot.py')
            self.copy('main.py')
            self.copy('setup')
            self.copy('web/www')

            self.convert(self.find(''))
            self.convert(self.find('bitmap'))
            self.convert(self.find('bitmap/acep_rotated'), 'acep')
            self.convert(self.find('bitmap/bwy'), 'bwy')
            self.convert(self.find('db'))
            self.convert(self.find('display'))
            self.convert(self.find('lang'))
            self.convert(self.find('setup'))
            self.convert(self.find('ui'))
            self.convert(self.find('ui/acep'), 'acep')
            self.convert(self.find('ui/bwy'), 'bwy')
            self.convert(self.find('web'))
            self.convert(self.find('web/microweb'))
            self.convert(self.find('web/page'))

            self.command(f'rm {Path(self.dwd, "boot.mpy")}')
            self.command(f'rm {Path(self.dwd, "main.mpy")}')
            self.command(f'rm {Path(self.dwd, "display/epd_acep.mpy")}', 'bwy')
            self.command(f'rm {Path(self.dwd, "display/epd_bwy.mpy")}', 'acep')
            self.command(f'rm {Path(self.dwd, "setup/__init__.py")}')
            self.command(f'rm {Path(self.dwd, "setup/display.mpy")}')
            self.command(f'rm {Path(self.dwd, "setup/epd_acep.py")}')
            self.command(f'rm {Path(self.dwd, "setup/epd_bwy.py")}')
            self.command(f'rm {Path(self.dwd, "setup/pins.mpy")}')
            self.command(f'rm {Path(self.dwd, "setup/epd_acep.mpy")}', 'bwy')
            self.command(f'rm {Path(self.dwd, "setup/epd_bwy.mpy")}', 'acep')
            self.command(f'rm {Path(self.dwd, "db/_alert.mpy")}')
            self.command(f'rm {Path(self.dwd, "db/_beep.mpy")}')
            self.command(f'rm {Path(self.dwd, "db/_connection.mpy")}')
            self.command(f'rm {Path(self.dwd, "db/_display.mpy")}')
            self.command(f'rm {Path(self.dwd, "db/_led.mpy")}')
            self.command(f'rm {Path(self.dwd, "db/_location.mpy")}')
            self.command(f'rm {Path(self.dwd, "db/_spot.mpy")}')
            self.command(f'rm {Path(self.dwd, "db/_sys.mpy")}')
            self.command(f'rm {Path(self.dwd, "db/_temp.mpy")}')
            self.command(f'rm {Path(self.dwd, "db/_time.mpy")}')
            self.command(f'rm {Path(self.dwd, "db/_ui.mpy")}')
            self.command(f'rm {Path(self.dwd, "db/_vbat.mpy")}')

            #packfw((('', '*.py'), ('', '*.mpy'), ('db', '*.mpy'), ('ui', '*.mpy'), ('web', '*.mpy'), ('lang', '*.mpy')))
        finally:
            self.command(f'cd {root}')

    def command(self, cmd, variant=None):
        if variant is not None and variant != self.variant:
            return

        print(cmd)
        os.system(cmd)

    def find(self, p, w="*.py", d=None):
        if d is None:
            d = self.cwd
        s = Path(d, p)
        os.chdir(s)

        l = []

        for f in glob.glob(w):
            l.append((p, f))

        return l

    def copy(self, p):
        src = Path(self.cwd, p)
        dst = Path(self.dwd, p)
        cmd = (f'rm -Rf {dst}', f'mkdir -p {dst} && rsync -avL --exclude="__pycache__" "{src}/." "{dst}/."' if src.is_dir() else f'cp "{src}" "{dst}"')

        for c in cmd:
            self.command(c)

    def convert(self, l, variant=None):
        if variant is not None and variant != self.variant:
            return

        try:
            Path(self.dwd, l[0][0]).mkdir()
        except FileExistsError:
            pass

        os.chdir(self.cwd)

        for f in l:
            src = os.path.relpath(Path(self.cwd, *f))
            dst = os.path.abspath(Path(self.dwd, f[0], f[1][:-2] + 'mpy'))
            self.command('{} {} -o {}'.format(self.mpc, src, dst))

    def packfw(self, l):
        f = open(self.fw, 'wb')
        f.write(struct.pack('<IHH', 0x31415926, 1, len(self.sha)))
        f.write(self.sha)

        for d in l:
            fl = find(*d, self.dwd)
            for pf in fl:
                pf = os.path.relpath(Path(self.dwd, *pf))
                print('Compress "{}"'.format(pf))
                wf = open(pf, 'rb')
                pf = pf.encode()
                f.write(struct.pack('<H', len(pf)))
                f.write(pf)
                d = zlib.compress(wf.read())
                f.write(struct.pack('<I', len(d)))
                f.write(d)
                wf.close()
        f.close()


builder_bwy = Builder('micropython', 'bwy')
builder_bwy()

builder_acep = Builder('micropython', 'acep')
builder_acep(cleanup=True)
