#!/usr/bin/python3
import glob, os

cwd = os.path.join(os.getcwd(), "../micropython")
dwd = os.path.abspath('micropython')
mpc = os.path.abspath('./mpy-cross')

def command(cmd):
    print(    cmd)
    os.system(cmd)


def find(p):
    s = os.path.join(cwd, p)
    os.chdir(s)
    
    l = []
    
    for f in glob.glob("*.py"):
        l.append((p, f))
    
    return l


def copy(p):
    src = os.path.join(cwd, p)
    dst = os.path.join(dwd, p)
    cmd = ('rm -Rf {}'.format(dst), 'cp -LR {} {}'.format(src, dst))
    
    for c in cmd:
        command(c)


def convert(l):
    try:
        os.mkdir(os.path.join(dwd, l[0][0]))
    except FileExistsError:
        pass
    
    os.chdir(cwd)
    
    for f in l:
        src = os.path.relpath(os.path.join(cwd, f[0], f[1]))
        dst = os.path.abspath(os.path.join(dwd, f[0], f[1][:-2] + 'mpy'))
        command('{} {} -o {}'.format(mpc, src, dst))


command('rm -Rf {}'.format(dwd))
command('mkdir  {}'.format(dwd))

copy('config')
copy('bitmap')
copy('boot.py')
copy('main.py')

convert(find(''))
convert(find('display'))
convert(find('ui'))
convert(find('web'))
convert(find('config'))

command('rm {}'.format(os.path.join(dwd, 'main.mpy')))
command('rm {}'.format(os.path.join(dwd, 'boot.mpy')))
command('rm {}'.format(os.path.join(dwd, 'config/__init__.py')))
command('rm {}'.format(os.path.join(dwd, 'config/connection.mpy')))
command('rm {}'.format(os.path.join(dwd, 'config/spot.mpy')))
command('rm {}'.format(os.path.join(dwd, 'config/ui.mpy')))
command('rm {}'.format(os.path.join(dwd, 'config/pins.mpy')))
