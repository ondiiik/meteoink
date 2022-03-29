#!/usr/bin/python3
import glob
import os
import struct
import zlib
import git
from pathlib import Path


cwd = Path(os.getcwd(), "../micropython")
dwd = os.path.abspath('micropython')
fw = os.path.abspath('meteoink.fw')
mpc = os.path.abspath('./mpy-cross -v -march=xtensawin')
repo = git.Repo(search_parent_directories=True)
sha = repo.head.object.hexsha.encode()


def command(cmd):
    print(cmd)
    os.system(cmd)


def find(p, w="*.py", d=cwd):
    s = Path(d, p)
    os.chdir(s)

    l = []

    for f in glob.glob(w):
        l.append((p, f))

    return l


def copy(p):
    src = Path(cwd, p)
    dst = Path(dwd, p)
    cmd = (f'rm -Rf {dst}', f'mkdir -p {dst} && rsync -avL --exclude="__pycache__" "{src}/." "{dst}/."' if src.is_dir() else f'cp "{src}" "{dst}"')

    for c in cmd:
        command(c)


def convert(l):
    try:
        Path(dwd, l[0][0]).mkdir()
    except FileExistsError:
        pass

    os.chdir(cwd)

    for f in l:
        src = os.path.relpath(Path(cwd, *f))
        dst = os.path.abspath(Path(dwd, f[0], f[1][:-2] + 'mpy'))
        command('{} {} -o {}'.format(mpc, src, dst))


def packfw(l):
    f = open(fw, 'wb')
    f.write(struct.pack('<IHH', 0x31415926, 1, len(sha)))
    f.write(sha)

    for d in l:
        fl = find(*d, dwd)
        for pf in fl:
            pf = os.path.relpath(Path(dwd, *pf))
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


with open(Path(cwd, 'main.py'), 'w') as f:
    f.write(f'''from log import dump_exception

try:
    print('Starting the application ...')
    from app import run
    run({sha})
    
except KeyboardInterrupt as e:
    dump_exception('Interrupted by keyboard ...', e)
except BaseException as e:
    dump_exception('!!! APPLICATION ERROR - REBOOTING !!!', e)
    import machine
    machine.reset()
''')

command('rm -Rf {}'.format(dwd))
command('mkdir  {}'.format(dwd))

copy('boot.py')
copy('config')
copy('main.py')
copy('web/www')

convert(find(''))
convert(find('bitmap'))
convert(find('config'))
convert(find('display'))
convert(find('lang'))
convert(find('ui'))
convert(find('var'))
convert(find('web'))
convert(find('web/microweb'))

command('rm {}'.format(Path(dwd, 'boot.mpy')))
command('rm {}'.format(Path(dwd, 'main.mpy')))
command('rm {}'.format(Path(dwd, 'config/__init__.py')))
command('rm {}'.format(Path(dwd, 'config/alert.mpy')))
command('rm {}'.format(Path(dwd, 'config/alert.py')))
command('rm {}'.format(Path(dwd, 'config/connection.mpy')))
command('rm {}'.format(Path(dwd, 'config/connection.py')))
command('rm {}'.format(Path(dwd, 'config/display.mpy')))
command('rm {}'.format(Path(dwd, 'config/display.py')))
command('rm {}'.format(Path(dwd, 'config/led.mpy')))
command('rm {}'.format(Path(dwd, 'config/location.mpy')))
command('rm {}'.format(Path(dwd, 'config/location.py')))
command('rm {}'.format(Path(dwd, 'config/pins.mpy')))
command('rm {}'.format(Path(dwd, 'config/spot.mpy')))
command('rm {}'.format(Path(dwd, 'config/spot.py')))
command('rm {}'.format(Path(dwd, 'config/sys.mpy')))
command('rm {}'.format(Path(dwd, 'config/temp.mpy')))
command('rm {}'.format(Path(dwd, 'config/temp.py')))
command('rm {}'.format(Path(dwd, 'config/ui.mpy')))
command('rm {}'.format(Path(dwd, 'config/ui.py')))
command('rm {}'.format(Path(dwd, 'config/vbat.mpy')))
command('rm {}'.format(Path(dwd, 'config/vbat.py')))
command('rm {}'.format(Path(dwd, 'var/alert.py')))
command('rm {}'.format(Path(dwd, 'var/alert.mpy')))
command('rm {}'.format(Path(dwd, 'var/display.py')))
command('rm {}'.format(Path(dwd, 'var/display.mpy')))

packfw((('', '*.py'), ('', '*.mpy'), ('config', '*.mpy'), ('ui', '*.mpy'), ('web', '*.mpy'), ('lang', '*.mpy')))
