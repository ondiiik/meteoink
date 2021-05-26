from machine import deepsleep


def _check_mode(args, assign):
    import var.mode
    return assign and (not (mode.MODE == args[0]))


def _write_mode(args):
    print('Rebuild variables', 'mode')
    with open('var/{}.py'.format('mode'), 'w') as f:
        f.write('MODE = {}'.format(args[0]))


def _check_alert(args, assign):
    import var.alert
    return assign and (not (alert.ALREADY_TRIGGERED == args[0]))


def _write_alert(args):
    print('Rebuild variables', 'alert')
    with open('var/{}.py'.format('alert'), 'w') as f:
        f.write('ALREADY_TRIGGERED = {}'.format(args[0]))


_modules = { 'mode' : (_check_mode,  _write_mode),
             'alert': (_check_alert, _write_alert) }


def write(m, args, assign = True, force = False):
    m = _modules[m]
    try:
        change = m[0](args, assign)
    except:
        change = True
    
    if force or change:
        m[1](args)
    
    return change


reset = False
reset = write('mode',  (0,),     False) or reset
reset = write('alert', (False,), False) or reset

if reset:
    print('Variables rebuilt - rebooting')
    deepsleep(1)

import var.mode
import var.alert
