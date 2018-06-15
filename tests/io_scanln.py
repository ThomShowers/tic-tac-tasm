from proxys import Io
import sys

if len(sys.argv) != 2 or not sys.argv[1].isdigit():
    print("usage: io_scanln <scan-length> (scan-length must be a positive integer)")
    exit(1)

expectedLength = int(sys.argv[1])
print(Io().scanln(expectedLength))