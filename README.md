##Documentation
    def shell_command(self, as_root=False, command=None, simulate=False, verbose=False)
    
- as_root - if True command will be prefixed with "sudo"
- command - string that overrides command to execute, can be used for commands that contain characters not valid for python function names
- simulate - prevents execution, command string will be returned
- verbose - if True command output will be displayed + additional output

##Examples
###Simple Execution
    >>> @shell_command(verbose=True)
    ... def whoami():
    ...      return
    ... 
    >>> whoami()
    Executing shell command: "whoami"
    user
    
### Automatically format command parameters
    >>> @shell_command(verbose=True)
    ... def ping(*args, **kwargs):
    ...     return
    ...
    >>> ping('github.com', c=1)
    Executing shell command: "ping -c 1 github.com"
    PING github.com (192.30.252.129) 56(84) bytes of data.
    64 bytes from github.com (192.30.252.129): icmp_seq=1 ttl=52 time=111 ms
    
    --- github.com ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 111.829/111.829/111.829/0.000 ms
<!-- split -->
    >>> @shell_command(verbose=True)
    ... def wget(*args, **kwargs):
    ...     return
    ...
    >>> wget('https://github.com', O='index.html', q=None, progress='bar')
    Executing shell command: "wget -q -O index.html --progress=bar https://github.com"

###Execute as super user
    >>> @shell_command(verbose=True, as_root=True)
    ... def whoami():
    ...      return
    ... 
    >>> whoami()
    Executing shell command: "sudo whoami"
    root
    
###Validate parameters
    >>> @shell_command(verbose=True)
    ... def ssh(*args, **kwargs): 
    ... connection_string = args[0]
    ... user, host = connection_string.split('@')
    ... 
    ... s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ... try:
    ...     s.connect((host, 22))
    ... except socket.error:
    ...     print('Port 22 on host "%s" is not accessible.' % host)
    ...     return 1
    ... finally:
    ...     s.close()
    ... return None
    ...
    >>> ssh('root@machine')
    Port 22 on host "machine" is not accessible.
    1
    
##Known Issues
- doesn't support parameters containing characters not allowed in python keywords (e.g. -)