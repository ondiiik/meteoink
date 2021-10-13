from machine import reset
from log     import log


def _check_alert(args, assign):
    import var.alert
    return assign and (not (alert.ALREADY_TRIGGERED == args[0]))


def _write_alert(args):
    try:
        from var.alert import _cnt as cnt
    except:
        cnt = 0
    
    cnt += 1
    log('Rebuild variables', f'alert ({cnt} times)')
    with open(f'var/alert.py', 'w') as f:
        f.write(f'ALREADY_TRIGGERED = {args[0]}\n_cnt = {cnt}\n')


def _check_display(args, assign):
    import var.display
    return assign and (not (display.DISPLAY_STATE == args[0]))


def _write_display(args):
    try:
        from var.display import _cnt as cnt
    except:
        cnt = 0
    
    cnt += 1
    log('Rebuild variables', f'display ({cnt} times)')
    with open('var/display.py', 'w') as f:
        f.write(f'DISPLAY_STATE = {args[0]}\n_cnt = {cnt}\n')


_modules = { 'alert'   : (_check_alert,   _write_alert),
             'display' : (_check_display, _write_display) }


def write(m, args, assign = True, force = False):
    m = _modules[m]
    try:
        change = m[0](args, assign)
    except:
        change = True
    
    if force or change:
        m[1](args)
    
    return change


reboot = False
reboot = write('alert',   (False,), False) or reboot
reboot = write('display', (0,),     False) or reboot

if reboot:
    log('Variables rebuilt - rebooting')
    reset()

import var.alert
