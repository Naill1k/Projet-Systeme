import argparse

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()

group.add_argument("-v", "--verbose", action="count", default=0, help="increase verbosity")
group.add_argument("-q", "--quiet", action="store_true", help="suppress non-error messages")

parser.add_argument("-a", "--archive", action="store_true", help="archive mode; same as -rpt (no -H)")
parser.add_argument("-r", "--recursive", action="store_true", help="recurse into directories")
parser.add_argument("-u", "--update", action="store_true", help="skip files that are newer on the receiver")
parser.add_argument("-d", "--dirs", action="store_true", help="transfer directories without recursing")
parser.add_argument("-H", "--hard-links", action="store_true", help="preserve hard links")
parser.add_argument("-p", "--perms", action="store_true", help="preserve hard links")
parser.add_argument("-t", "--times", action="store_true", help="preserve times")
parser.add_argument("--existing", action="store_true", help="skip creating new files on receiver")
parser.add_argument("--ignore-existing", action="store_true", help="skip updating files that exist on receiver")
parser.add_argument("--delete", action="store_true", help="delete extraneous files from dest dirs")
parser.add_argument("--force", action="store_true", help="force deletion of dirs even if not empty")
parser.add_argument("--timeout", type=int, help="set I/O timeout in seconds")

parser.add_argument("SRC", type=str, help="The SOURCE directory")
parser.add_argument("DEST", type=str, help="The DESTINATION directory")

args = parser.parse_args()
