from ctypes import c_int
from ctypes import cdll
from ctypes import create_string_buffer
import os

sodir = f"{os.path.dirname(__file__)}/native"

class Io:

    def __init__(self):
        self.lib = cdll.LoadLibrary(f"{sodir}/io.so")

    def println(self, line):
        encoded = line.encode("ascii")
        return self.lib.println(encoded, len(encoded)) != 0

    def scanln(self, len):
        buffer = create_string_buffer(len)
        scanned = self.lib.scanln(buffer, len)
        if scanned > 0:
            return buffer.value.decode("ascii")
        return None

    def cursorUp(self, count):
        return self.lib.cursorUp(count) != 0
        