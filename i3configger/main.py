import logging
import sys

from i3configger import (
    base, build, cli, config, exc, ipc, message, partials,  watch)

log = logging.getLogger(__name__)


def main():
    """Wrap main to show own exceptions wo traceback in normal use."""
    args = cli.process_command_line()
    try:
        _main(args)
    except exc.I3configgerException as e:
        if args.v > 2:
            raise
        sys.exit(e)


def _main(args):
    config.ensure_i3_configger_sanity()
    cnf = config.I3configgerConfig(load=False)
    ipc.configure(args)
    if args.version:
        print(f"i3configger {base.get_version()}")
        return 0
    if args.kill:
        watch.exorcise()
        return 0
    if args.message:
        prts = partials.create(cnf.partialsPath)
        message.process(cnf.messagesPath, prts, args.message)
    if watch.get_daemon_process():
        if not args.message:
            sys.exit("Already running - did you mean to send a message?")
        log.info("let the daemon do the work")
        return 0
    if args.daemon:
        watch.daemonized(args.v, args.log)
    elif args.watch:
        try:
            watch.watch_guarded()
        except KeyboardInterrupt:
            sys.exit("interrupted by user")
    else:
        build.build_all()
        ipc.communicate(refresh=True)
