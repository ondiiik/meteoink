from ulogging import getLogger
logger = getLogger(__name__)

from machine import reset


def _check_alert(args, assign):
    import var.alert
    return assign and (not (alert.ALREADY_TRIGGERED == args[0]))


def _write_alert(args):
    try:
        from var.alert import _cnt as cnt
    except:
        cnt = 0

    cnt += 1
    logger.info('Rebuild variables', f'alert ({cnt} times)')
    with open(f'var/alert.py', 'w') as f:
        f.write(f'ALREADY_TRIGGERED = {args[0]}\n_cnt = {cnt}\n')


_modules = {'alert': (_check_alert,   _write_alert)}


def write(m, args, assign=True, force=False):
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

if reboot:
    logger.info('Variables rebuilt - rebooting')
    reset()

import var.alert
