mrsync(1)                                                              mrsync(1)



NAME
       mrsync - minimalistic version of rsync

SYNOPSIS
       mrsync [OPTION]... SRC [SRC]... DEST

       mrsync [OPTION]... SRC [SRC]... [USER@]HOST:DEST

       mrsync [OPTION]... SRC [SRC]... [USER@]HOST::DEST

       mrsync [OPTION]... SRC

       mrsync [OPTION]... [USER@]HOST:SRC [DEST]

       mrsync [OPTION]... [USER@]HOST::SRC [DEST]

DESCRIPTION
       This project was realized in the context of the second year system programming course from Université Côte d'Azur, teached by professor Sid Touati.
       mrsync is a program that behaves in much the same way that rsync does, but
       has less options.

GENERAL
       mrsync copies files either to or from a remote host, or locally  on  the
       current  host  (it  does  not  support copying files between two remote
       hosts).

       There are two different ways for mrsync  to  contact  a  remote  system:
       using  ssh or contacting an mrsync daemon directly via TCP.  The  
       remote-shell  transport is used whenever the source or destination path 
       contains a single colon (:) separator after a host specification.
       Contacting  an  mrsync daemon directly happens when the source or 
       destination path contains a double colon (::) separator after a host 
       specification.
       
       As a special case, if a single source arg is specified without a desti-
       nation, the files are listed in an output format similar to "ls -l".

       As expected, if neither the source or destination path specify a remote
       host, the copy occurs locally (see also the --list-only option).


       When using a remote system (ssh or daemon), the path on the distant host must be specified from the personal directory or be an absolute path.


SETUP
       See the file README for installation instructions.

       Once  installed,  you  can use mrsync to any machine that you can access
       via a remote shell (as well as some that you can access using the mrsync
       daemon-mode  protocol).   

       Note  that  mrsync  must be installed on both the source and destination
       machines.


USAGE
       You use mrsync in the same way you use rcp. You must  specify  a  source
       and a destination, one of which may be remote.

       Perhaps the best way to explain the syntax is with some examples:

              mrsync -t *.c foo:src/


       This would transfer all files matching the pattern *.c from the current
       directory to the directory src on the machine foo. If any of the  files
       already  exist on the remote system then the mrsync remote-update proto-
       col is used to update the file by sending only the differences. See the
       tech report for details.

              mrsync -av foo:src/bar /data/tmp


       This would recursively transfer all files from the directory src/bar on
       the machine foo into the /data/tmp/bar directory on the local  machine.
       The  files  are  transferred in "archive" mode, which ensures that
       permissions are preserved  in  the transfer.  

              mrsync -av foo:src/bar/ /data/tmp


       A trailing slash on the source changes this behavior to avoid  creating
       an  additional  directory level at the destination.  You can think of a
       trailing / on a source as meaning "copy the contents of this directory"
       as  opposed  to  "copy  the  directory  by name", but in both cases the
       attributes of the containing directory are transferred to the  contain-
       ing  directory on the destination.  In other words, each of the follow-
       ing commands copies the files in the same way, including their  setting
       of the attributes of /dest/foo:

              mrsync -av /src/foo /dest
              mrsync -av /src/foo/ /dest/foo


       You  can  also  use mrsync in local-only mode, where both the source and
       destination don't have a ':' in the name. In this case it behaves  like
       an improved copy command.

CONNECTING TO AN MRSYNC DAEMON
       It  is  also possible to use mrsync without a remote shell as the trans-
       port.  In this case you will directly connect to a remote mrsync daemon,
       typically  using  TCP port 10873.  (This obviously requires the daemon to
       be running on the remote system, so refer to the STARTING AN MRSYNC DAE-
       MON TO ACCEPT CONNECTIONS section below for information on that.)

       Using  mrsync  in  this  way is the same as using it with a remote shell
       except that:


       o      you either use a double colon :: instead of a  single  colon  to
              separate the hostname from the path.

       o      if you specify no local destination then a listing of the speci-
              fied files on the remote daemon is provided.

       An example that copies all the files in a remote directory named "src":

           mrsync -av host::src /dest


STARTING AN MRSYNC DAEMON TO ACCEPT CONNECTIONS
       In order to connect to an mrsync daemon, the remote system needs to have
       a daemon already running (or it needs to have configured something like
       inetd to spawn an mrsync daemon for incoming connections on a particular
       port).

       If  you're  using  ssh tunneling for the transfer,
       there is no need to manually start an mrsync daemon.

OPTIONS SUMMARY
       Here is a short summary of the options available in mrsync. Please refer
       to the detailed description below for a complete description.

        -v, --verbose               increase verbosity
        -q, --quiet                 suppress non-error messages
        -a, --archive               archive mode; same as -rpt (no -H)
        -r, --recursive             recurse into directories
        -u, --update                skip files that are newer on the receiver
        -d, --dirs                  transfer directories without recursing
        -H, --hard-links            preserve hard links
        -p, --perms                 preserve permissions
        -t, --times                 preserve times
            --existing              skip creating new files on receiver
            --ignore-existing       skip updating files that exist on receiver
            --delete                delete extraneous files from dest dirs
            --force                 force deletion of dirs even if not empty
            --timeout=TIME          set I/O timeout in seconds
            --blocking-io           use blocking I/O for the remote shell
        -I, --ignore-times          don't skip files that match size and time
            --size-only             skip files that match in size
            --address=ADDRESS       bind address for outgoing socket to daemon
            --port=PORT             specify double-colon alternate port number
            --list-only             list the files instead of copying them
       -h   --help                  show this help


       mrsync  can also be run as a daemon, in which case the following options
       are accepted:

            --daemon                run as an mrsync daemon
            --address=ADDRESS       bind to the specified address
            --no-detach             do not detach from the parent
            --port=PORT             listen on alternate port number
        -h, --help                  show this help (if used after --daemon)



OPTIONS
       Many  of  the  command  line options  have  two  variants,  one short and 
       one long.  These are shown below, separated by commas. Some options only 
       have a long variant.  The '='  for  options  that take a parameter is 
       optional; whitespace can be used instead.


       --help Print a short help page  describing  the  options  available  in
              mrsync  and exit.  For backward-compatibility with older versions
              of mrsync, the help will also be output if you use the -h  option
              without any other args.

       -v, --verbose
              This  option  increases  the amount of information you are given
              during the transfer.  By default, mrsync works silently. A single
              -v  will  give you information about what files are being trans-
              ferred and a brief summary at the end. Two -v  flags  will  give
              you  information  on  what  files are being skipped and slightly
              more information at the end. More than two -v flags should  only
              be used if you are debugging mrsync.

              Note that the names of the transferred files that are output are
              just  the  name of the file. At the single -v level of verbosity, 
              this does not mention when a file gets its attributes changed.             

       -q, --quiet
              This  option  decreases  the amount of information you are given
              during the transfer, notably  suppressing  information  messages
              from  the remote server. This flag is useful when invoking mrsync
              from cron.


       -I, --ignore-times
              Normally  mrsync  will  skip  any files that are already the same
              size and have the same  modification  time-stamp.   This  option
              turns  off  this "quick check" behavior, causing all files to be
              updated.


       --size-only
              Normally mrsync will not transfer any files that are already  the
              same  size  and  have the same modification time-stamp. With the
              --size-only option, files will not be transferred if  they  have
              the  same  size,  regardless  of  timestamp. This is useful when
              starting to use mrsync after using another mirroring system which
              may not preserve timestamps exactly.

       -a, --archive
              This is equivalent to -rpt. It is a quick way of saying  you
              want  recursion  and want to preserve almost everything (with -H
              being a notable omission).  

              Note that -a does not preserve hardlinks, because finding multi-
              ply-linked  files is expensive.  You must separately specify -H.


       -r, --recursive
              This  tells  mrsync  to  copy  directories recursively.  See also
              --dirs (-d).

       -u, --update
              This  forces mrsync to skip any files which exist on the destina-
              tion and have a modified time that  is  newer  than  the  source
              file.   (If an existing destination file has a modify time equal
              to the source file's, it will be updated if the sizes  are  dif-
              ferent.)


       -d, --dirs
              Tell the sending  side  to  include  any  directories  that  are
              encountered.  Unlike --recursive, a directory's contents are not
              copied unless the directory name specified is "." or ends with a
              trailing  slash (e.g. ".", "dir/.", "dir/", etc.).  Without this
              option or the --recursive option, mrsync will skip  all  directo-
              ries it encounters (and output a message to that effect for each
              one).  If you specify both --dirs and  --recursive,  --recursive
              takes precedence.


       --existing
              This  tells mrsync to skip creating files (including directories)
              that do not exist yet on the destination.   If  this  option  is
              combined  with  the  --ignore-existing  option, no files will be
              updated (which can be useful if all you want to do is to  delete
              extraneous files).


       --ignore-existing
              This  tells  mrsync  to skip updating files that already exist on
              the destination (this does not ignore  existing  directores,  or
              nothing would get done).  See also --existing.


       --delete
              This  tells  mrsync to delete extraneous files from the receiving
              side (ones that aren't on the sending side), but  only  for  the
              directories  that  are  being synchronized.  You must have asked
              mrsync to send the whole directory (e.g. "dir" or "dir/") without
              using  a  wildcard  for  the directory's contents (e.g. "dir/*")
              since the wildcard is expanded by the shell and mrsync thus  gets
              a  request  to  transfer individual files, not the files' parent
              directory.  

              This option has no effect unless either --recursive or --dirs 
              (-d) is set, but only for  directories whose contents are being copied.

       --force
              This  option tells mrsync to delete a non-empty directory when it
              is to be replaced by a non-directory.  This is only relevant  if
              deletions are not active (see --delete for details).


       --timeout=TIMEOUT
              This option allows you to set a maximum I/O timeout in  seconds.
              If no data is transferred for the specified time then mrsync will
              exit. The default is 0, which means no timeout.


       --address
              By default mrsync will bind to the wildcard address when connect-
              ing  to  an  mrsync  daemon.   The --address option allows you to
              specify a specific IP address (or hostname)  to  bind  to.   See
              also this option in the --daemon mode section.


       --port=PORT
              This  specifies  an alternate TCP port number to use rather than
              the default of 873.  This is only needed if you  are  using  the
              double-colon  (::) syntax to connect with an mrsync daemon (since
              the URL syntax has a way to specify the port as a  part  of  the
              URL).  See also this option in the --daemon mode section.


       --list-only
              This  option will cause the source files to be listed instead of
              transferred.  This option is  inferred  if  there  is  a  single
              source  arg  and no destination specified, so its main uses are:
              (1) to turn a copy command that includes a destination arg  into
              a  file-listing command, (2) to be able to specify more than one
              local source arg (note: be sure to include the destination).
              Caution: keep in mind that a source arg with a wild-card is 
              expanded by the shell into multiple args, so it is never safe to 
              try to list such an arg without using this option.  For example:

                  mrsync -av --list-only foo* dest/


DAEMON OPTIONS
       The options allowed when starting an mrsync daemon are as follows:


       --daemon
              This  tells mrsync that it is to run as a daemon.  The daemon you
              start running may be accessed using an mrsync  client  using  the
              host::dir or mrsync://host/dir/ syntax.

              If  standard input is a socket then mrsync will assume that it is
              being run via inetd, otherwise it will detach from  the  current
              terminal  and  become a background daemon.  The daemon will read
              the config file (mrsyncd.conf) on each connect made by  a  client
              and respond to requests accordingly.  See the mrsyncd.conf(5) man
              page for more details.


       --address
              By default mrsync will bind to the wildcard address when run as a
              daemon  with  the  --daemon option.  The --address option allows
              you to specify a specific IP address (or hostname) to  bind  to.
              This  makes  virtual  hosting  possible  in conjunction with the
              --config option.  See also the "address" global  option  in  the
              mrsyncd.conf manpage.

       --no-detach
              When running as a daemon, this option  instructs  mrsync  to  not
              detach  itself  and become a background process.  This option is
              required when running as a service on Cygwin, and  may  also  be
              useful when mrsync is supervised by a program such as daemontools
              or AIX's System Resource Controller.  --no-detach is also recom-
              mended  when  mrsync is run under a debugger.  This option has no
              effect if mrsync is run from inetd or sshd.


       --port=PORT
              This specifies an alternate TCP port number for  the  daemon  to
              listen  on  rather than the default of 873.  See also the "port"
              global option in the mrsyncd.conf manpage.

       -h, --help
              When  specified after --daemon, print a short help page describ-
              ing the options available for starting an mrsync daemon.





SYMBOLIC LINKS
       Symbolic links are  not  transferred  at  all.   A  message
       "skipping non-regular" file is emitted for any symlinks that exist.

DIAGNOSTICS
       mrsync occasionally produces error messages that may seem a little cryp-
       tic. The one that seems to cause the most confusion is  "protocol  ver-
       sion mismatch -- is your shell clean?".

       This  message is usually caused by your startup scripts or remote shell
       facility producing unwanted garbage on the stream that mrsync  is  using
       for  its  transport.  The  way  to diagnose this problem is to run your
       remote shell like this:

              ssh remotehost /bin/true > out.dat


       then look at out.dat. If everything is working correctly  then  out.dat
       should  be  a zero length file. If you are getting the above error from
       mrsync then you will probably find that out.dat contains  some  text  or
       data.  Look  at  the contents and try to work out what is producing it.
       The most common cause is incorrectly configured shell  startup  scripts
       (such  as  .cshrc  or .profile) that contain output statements for non-
       interactive logins.


EXIT VALUES
       0      Success

       1      Syntax or usage error

       3      Errors selecting input/output files, dirs

       5      Error starting client-server protocol

       10     Error in socket I/O

       11     Error in file I/O

       12     Error in mrsync protocol data stream

       20     Received SIGUSR1 or SIGINT

       21     Some error returned by waitpid()

       23     Partial transfer due to error

       24     Partial transfer due to vanished source files

       30     Timeout in data send/receive


SEE ALSO
       rsync(1)


BUGS
       The options --blocking-io, -H, -t, -p and --no-OPTION are not supported.


INTERNAL OPTIONS
       The option --server is used  internally  by  mrsync,  and
       should  never  be  typed  by  a  user under normal circumstances.


CREDITS
       A  WEB site is available at http://rsync.samba.org/.  The site includes
       an FAQ-O-Matic which may cover  questions  unanswered  by  this  manual
       page.

AUTHORS
       This mrsync has been written by ALINOT Killian and SOLODOVNIKOV Boris.

                                  L2 info math-info 2022/2023              mrsync(1)
