from proxys import Io
import sys

if len(sys.argv) != 2:
    print("usage: io_println <println-arg>")
    exit(1)

exit(0 if Io().println(sys.argv[1]) else 1)
