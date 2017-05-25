import logging
import subprocess
import tempfile
from pathlib import Path

log = logging.getLogger(__name__)
LOG_PATH = Path(tempfile.gettempdir()) / 'i3configger.log'


def configure_logging(verbosity, writeLog=False, isDaemon=False):
    level = logging.getLevelName(
        {0: 'ERROR', 1: 'WARNING', 2: 'INFO'}.get(verbosity, 'DEBUG'))
    fmt = '%(asctime)s %(name)s %(levelname)s: %(message)s'
    if isDaemon:
        if not writeLog:
            return
        logging.basicConfig(filename=str(LOG_PATH), format=fmt, level=level)
    else:
        logging.basicConfig(format=fmt, level=level)
        if not writeLog:
            return
        fileHandler = logging.FileHandler(str(LOG_PATH))
        fileHandler.setFormatter(logging.Formatter(fmt))
        fileHandler.setLevel(level)
        log.addHandler(fileHandler)


class IpcControl:
    @classmethod
    def reload_i3(cls):
        if cls._send_i3_msg('reload'):
            cls.notify_send("reloaded i3")

    @classmethod
    def restart_i3(cls):
        if cls._send_i3_msg('restart'):
            cls.notify_send("restarted i3")

    refresh = restart_i3

    @classmethod
    def _send_i3_msg(cls, msg):
        # todo use Adaephons i3 library
        cmd = ['i3-msg', msg]
        try:
            output = subprocess.check_output(cmd).decode()
            if '"success":true' in output:
                return True
            cls.notify_send("%s: %s" % (cmd, output), urgency='critical')
            return False
        except subprocess.CalledProcessError as e:
            if msg == 'restart' and e.returncode == 1:
                log.debug("[IGNORE] exit 1 is ok for restart")
                return True

    @classmethod
    def notify_send(cls, msg, urgency='low'):
        subprocess.check_call([
            'notify-send', '-a', 'i3configger', '-t', '1', '-u', urgency, msg])
