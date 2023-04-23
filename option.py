import argparse, message

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()

group.add_argument("-v", "--verbose", action="count", default=0, help="increase verbosity")
group.add_argument("-q", "--quiet", action="store_true", help="suppress non-error messages")

parser.add_argument('-a', '--archive', action='store_true', help='archive mode; same as -rpt (no -H)')
parser.add_argument('-r', '--recursive', action='store_true', help='recurse into directories')
parser.add_argument('-u', '--update', action='store_true', help='skip files that are newer on the receiver')
parser.add_argument('-d', '--dirs', action='store_true', help='transfer directories without recursing')
parser.add_argument('-H', '--hard-links', action='store_true', help='preserve hard links')
parser.add_argument('-p', '--perms', action='store_true', help='preserve permissions')
parser.add_argument('-t', '--times', action='store_true', help='preserve times')
parser.add_argument('--existing', action='store_true', help='skip creating new files on receiver')
parser.add_argument('--ignore-existing', action='store_true', help='skip updating files that exist on receiver')
parser.add_argument('--delete', action='store_true', help='delete extraneous files from dest dirs')
parser.add_argument('--force', action='store_true', help='force deletion of dirs even if not empty')
parser.add_argument('--timeout', type=int, help='set I/O timeout in seconds')
parser.add_argument('--blocking-io', action='store_true', help='use blocking I/O for the remote shell')
parser.add_argument('-I', '--ignore-times', action='store_true', help="don't skip files that match size and time")
parser.add_argument('--size-only', action='store_true', help='skip files that match in size')
parser.add_argument('--address', help='bind address for outgoing socket to daemon')
parser.add_argument('--port', type=int, help='specify double-colon alternate port number')
parser.add_argument('--list-only', action='store_true', help='list the files instead of copying them')
parser.add_argument('--server', action='store_true', help='Used in ssh communication to start server on remote host')

daemon_group = parser.add_argument_group('Daemon options')
daemon_group.add_argument('--daemon', action='store_true', help="run as an mrsync daemon")
# daemon_group.add_argument('--address', help='bind to the specified address')
daemon_group.add_argument('--no-detach', action='store_true', help="do not detach from the parent")
# daemon_group.add_argument('--port', type=int, help='listen on alternate port number')


parser.add_argument("files", nargs='+', help='Source ans destination file(s) or directory')

args = parser.parse_args()

if len(args.files) == 1 : # Mode --list-only
    src = args.files[:]
    dest = None
    args.list_only = True

else :
    src = args.files[:-1]
    dest = args.files[-1]

connection = 'local'


def split(file) :
    '''
    Determines the eventual name of the host and the user if specified (if not their value is None) and the destination
    Returns : (user, host, dest) where user and host may be None
    '''
    global connection, mode
    user, host = None, None

    if '@' in file : # User name specified
        user, file = file.split('@')

    if '::' in file : # daemon connection
        host, file = file.split('::')
        if connection != 'local' : raise SyntaxError('mrsync cannon copy files between two remote hosts')
        connection = 'daemon'

    elif ':' in file : # ssh connection
        host, file = file.split(':')
        if connection != 'local' : raise SyntaxError('mrsync cannon copy files between two remote hosts')
        connection = 'ssh'

    return user, host, file



if len(src) == 1 :
    src_user, src_host, src = split(src[0])
else :
    src_user, src_host = None, None


if dest is not None :
    dest_user, dest_host, dest = split(dest)
else :
    dest_user, dest_host = None, None


if src_host is not None :
    mode = 'PULL'
    host = src_host

elif dest_host is not None :
    mode = 'PUSH'
    host = dest_host

else :
    mode = 'LOCAL'
    host = None




# Construction of the dictionary containing the flags and options
state = {
    '-v': args.verbose,
    '-q': args.quiet,
    '-a': args.archive,
    '-r': args.recursive,
    '-u': args.update,
    '-d': args.dirs,
    '-H': args.hard_links,
    '-p': args.perms,
    '-t': args.times,
    '--existing': args.existing,
    '--ignore_existing': args.ignore_existing,
    '--delete': args.delete,
    '--force': args.force,
    '--timeout': args.timeout,
    '--blocking_io': args.blocking_io,
    '-I': args.ignore_times,
    '--size_only': args.size_only,
    '--address': args.address,
    '--port': args.port,
    '--list_only': args.list_only,
    '--server': args.server,
    '--daemon': args.daemon,
    '--no_detach': args.no_detach,

    'mode': mode,
    'connection': connection,
    'host': host,
    'src': src,
    'dest': dest
}


# Display active flags and options
for opt in state :
    val = state[opt]
    if type(val) == bool :
        if val :
            message.log(f"Flag : '{opt}'", state['-v'], 2)
    else :
        message.log(f"'{opt}' : {val}", state['-v'], 2)
        
message.log('='*64, state['-v'], 2)