from proxys import Io
import sys

if len(sys.argv) != 2:
    print("usage: io_scanln <scanln-arg>")
    exit(1)

if not sys.argv[1].isdigit():
    print("<scanln-arg> must be a positive integer")
    exit(1)

expectedLength = int(sys.argv[1])
print(Io().scanln(expectedLength))