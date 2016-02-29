import subprocess
import sys
import socket


class shell_command(object):
    def __init__(self, as_root=False, command=None, simulate=False, verbose=False):
        self.__as_root = as_root
        self.__command = command
        self.__simulate = simulate
        self.__verbose = verbose

    def __call__(self, fn):
        def __decorated(*args, **kwargs):
            ret = fn(*args, **kwargs)
            if ret is not None:
                return ret

            cmd = []

            if self.__as_root:
                cmd.append('sudo')

            cmd.append(
                self.__command if self.__command else fn.__name__
            )

            cmd.extend(self.__generate_arg_string(args, kwargs))

            if self.__verbose:
                print('Executing shell command: "' + ' '.join(cmd) + '"')

            if self.__simulate:
                return ' '.join(cmd)

            stdout = subprocess.DEVNULL
            stderr = subprocess.DEVNULL

            if self.__verbose:
                stdout = sys.stdout
                stderr = sys.stderr

            return subprocess.check_call(
                cmd,
                stdout=stdout,
                stderr=stderr
            )

        return __decorated

    @staticmethod
    def __generate_arg_string(args, kwargs):
        arguments = []

        for key, value in kwargs.items():
            if len(key) == 1:
                arguments.append('-' + str(key))
                if value is not None:
                    arguments.append(str(value))
            else:
                arg = '--' + str(key)
                if value is not None:
                    arg += '=' + str(value)
                arguments.append(arg)

        for value in args:
            arguments.append(str(value))

        return arguments


@shell_command(verbose=True)
def ssh(*args, **kwargs):
    connection_string = args[0]
    user, host = connection_string.split('@')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, 22))
    except socket.error:
        print('Port 22 on host "%s" is not accessible.' % host)
        return 1
    finally:
        s.close()
    return

ssh('root@machine')
