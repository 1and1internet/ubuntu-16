#!/usr/bin/env python

import sys
import os
import signal


def write_stdout(s):
    sys.stdout.write(s)
    sys.stdout.flush()


def write_stderr(s):
    sys.stderr.write(s)
    sys.stderr.flush()


def main():
    while 1:
        write_stdout('READY\n')  # transition from ACKNOWLEDGED to READY
        line = sys.stdin.readline()  # read header line from stdin
        write_stderr(line)  # print it out to stderr
        headers = dict([x.split(':') for x in line.split()])
        data = sys.stdin.read(int(headers['len']))  # read the event payload
        write_stderr(data)  # print the event payload to stderr
        write_stdout('RESULT 2\nOK')  # transition from READY to ACKNOWLEDGED
        if os.environ.get('SUPERVISORD_EXIT_ON_FATAL') == '1':
            with open('/var/run/supervisord.pid', 'r') as f:
                os.kill(int(f.read()), signal.SIGTERM)

if __name__ == '__main__':
    main()
    import sys
