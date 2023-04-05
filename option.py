import argparse

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

daemon_group = parser.add_argument_group('Daemon options')
daemon_group.add_argument('--daemon', action='store_true', help="run as an mrsync daemon")
# daemon_group.add_argument('--address', help='bind to the specified address')
daemon_group.add_argument('--no-detach', action='store_true', help="do not detach from the parent")
# daemon_group.add_argument('--port', type=int, help='listen on alternate port number')


parser.add_argument("files", nargs='+', help='Source ans destination file(s) or directory')

args = parser.parse_args()

if len(args.files) == 1 :
    src = args.files[:]
    dest = None

else :
    src = args.files[:-1]
    dest = args.files[-1]

connexion = 'local'

def split(file) :
    '''
    Determines the eventual name of the host and the user if specified (if not their value is None) and the destination
    Returns : (user, host, dest) where user and host may be None
    '''
    global connexion, mode
    user, host = None, None

    if '@' in file : # User name specified
        user, file = file.split('@')

    if '::' in file : # daemon connexion
        host, file = file.split('::')
        if connexion != 'local' : raise SyntaxError('mrsync cannon copy files between two remote hosts')
        connexion = 'daemon'

    elif ':' in file : # ssh connexion
        host, file = file.split(':')
        if connexion != 'local' : raise SyntaxError('mrsync cannon copy files between two remote hosts')
        connexion = 'ssh'

    return user, host, file


if len(src) == 1 :
    src_user, src_host, src = split(src[0])

if dest is not None :
    dest_user, dest_host, dest = split(dest)

if src_host is not None :
    mode = 'PULL'
elif dest_host is not None :
    mode = 'PUSH'
else :
    mode = 'LOCAL'

print('Source:', src_user, src_host, src)
print('Destination:', dest_user, dest_host, dest)
print('Connexion type :', connexion)
print('Mode :', mode)