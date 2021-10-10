#!/usr/bin/python3
import glob, os
import struct
import zlib
import git
    

cwd  = os.path.join(os.getcwd(), "../micropython")
dwd  = os.path.abspath('micropython')
fw   = os.path.abspath('meteoink.fw')
mpc  = os.path.abspath('./mpy-cross -v -march=xtensawin')
repo = git.Repo(search_parent_directories = True)
sha  = repo.head.object.hexsha.encode()
    

def command(  cmd):
    print(    cmd)
    os.system(cmd)


def find(p, w = "*.py", d = cwd):
    s = os.path.join(d, p)
    os.chdir(s)
    
    l = []
    
    for f in glob.glob(w):
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
        src = os.path.relpath(os.path.join(cwd, *f))
        dst = os.path.abspath(os.path.join(dwd, f[0], f[1][:-2] + 'mpy'))
        command('{} {} -o {}'.format(mpc, src, dst))


def packfw(l):
    f = open(fw, 'wb')
    f.write(struct.pack('<IHH', 0x31415926, 1, len(sha)))
    f.write(sha)
    
    for d in l:
        fl = find(*d, dwd)
        for pf in fl:
            pf = os.path.relpath(os.path.join(dwd, *pf))
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


f = open(os.path.join(cwd, 'main.py'), 'w')
f.write('from app import run\n')
f.write('run({})\n'.format(sha))
f.close()

command('rm -Rf {}'.format(dwd))
command('mkdir  {}'.format(dwd))

copy('boot.py')
copy('config')
copy('main.py')

convert(find(''))
convert(find('bitmap'))
convert(find('config'))
convert(find('display'))
convert(find('lang'))
convert(find('ui'))
convert(find('var'))
convert(find('web'))

command('rm {}'.format(os.path.join(dwd, 'boot.mpy')))
command('rm {}'.format(os.path.join(dwd, 'main.mpy')))
command('rm {}'.format(os.path.join(dwd, 'config/__init__.py')))
command('rm {}'.format(os.path.join(dwd, 'config/alert.mpy')))
command('rm {}'.format(os.path.join(dwd, 'config/alert.py')))
command('rm {}'.format(os.path.join(dwd, 'config/connection.mpy')))
command('rm {}'.format(os.path.join(dwd, 'config/connection.py')))
command('rm {}'.format(os.path.join(dwd, 'config/display.mpy')))
command('rm {}'.format(os.path.join(dwd, 'config/display.py')))
command('rm {}'.format(os.path.join(dwd, 'config/led.mpy')))
command('rm {}'.format(os.path.join(dwd, 'config/location.mpy')))
command('rm {}'.format(os.path.join(dwd, 'config/location.py')))
command('rm {}'.format(os.path.join(dwd, 'config/pins.mpy')))
command('rm {}'.format(os.path.join(dwd, 'config/spot.mpy')))
command('rm {}'.format(os.path.join(dwd, 'config/spot.py')))
command('rm {}'.format(os.path.join(dwd, 'config/sys.mpy')))
command('rm {}'.format(os.path.join(dwd, 'config/temp.mpy')))
command('rm {}'.format(os.path.join(dwd, 'config/temp.py')))
command('rm {}'.format(os.path.join(dwd, 'config/ui.mpy')))
command('rm {}'.format(os.path.join(dwd, 'config/ui.py')))
command('rm {}'.format(os.path.join(dwd, 'config/vbat.mpy')))
command('rm {}'.format(os.path.join(dwd, 'config/vbat.py')))
command('rm {}'.format(os.path.join(dwd, 'var/alert.py')))
command('rm {}'.format(os.path.join(dwd, 'var/alert.mpy')))
command('rm {}'.format(os.path.join(dwd, 'var/display.py')))
command('rm {}'.format(os.path.join(dwd, 'var/display.mpy')))

packfw((('', '*.py'), ('', '*.mpy'), ('config', '*.mpy'), ('ui', '*.mpy'), ('web', '*.mpy'), ('lang', '*.mpy')))
