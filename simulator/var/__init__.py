from machine import reset
from log     import log


def _check_alert(args, assign):
    import var.alert
    return assign and (not (alert.ALREADY_TRIGGERED == args[0]))


def _write_alert(args):
    log('Rebuild variables', 'alert')
    with open('var/{}.py'.format('alert'), 'w') as f:
        f.write('ALREADY_TRIGGERED = {}'.format(args[0]))


def _check_display(args, assign):
    import var.display
    return assign and (not (display.DISPLAY_STATE == args[0]))


def _write_display(args):
    log('Rebuild variables', 'display')
    with open('var/{}.py'.format('display'), 'w') as f:
        f.write('DISPLAY_STATE = {}'.format(args[0]))


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
