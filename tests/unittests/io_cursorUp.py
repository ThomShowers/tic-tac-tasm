import platform
from proxys import Io
import sys

if len(sys.argv) != 1:
    print("usage: io_cursorUp")
    exit(1)

system = platform.system()

if (system == "Windows"):

    from ctypes import Structure
    from ctypes import c_short
    from ctypes import windll
    from ctypes import byref
 
    class COORD(Structure):
        pass
 
    COORD._fields_ = [("X", c_short), ("Y", c_short)]

    class SMALL_RECT(Structure):
        pass

    SMALL_RECT._fields_ = [ ("Left", c_short), ("Top", c_short), ("Right", c_short), 
        ("Bottom", c_short) ]

    class CONSOLE_SCREEN_BUFFER_INFO(Structure):
        pass

    CONSOLE_SCREEN_BUFFER_INFO._fields_ = [ ("Size", COORD), ("CursorPosition", COORD),
        ("Attributes", c_short  ), ("Window", SMALL_RECT), ("MaximumWindowSize", COORD) ]

    STD_OUTPUT_HANDLE = -11
    h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    
    csbInfoBefore = CONSOLE_SCREEN_BUFFER_INFO()
    windll.kernel32.GetConsoleScreenBufferInfo(h, byref(csbInfoBefore))

    offset = 5

    newPos = COORD()
    newPos.X = csbInfoBefore.CursorPosition.X
    newPos.Y = csbInfoBefore.CursorPosition.Y + offset
    windll.kernel32.SetConsoleCursorPosition(h, newPos)

    Io().cursorUp(offset)

    csbInfoAfter = CONSOLE_SCREEN_BUFFER_INFO()
    windll.kernel32.GetConsoleScreenBufferInfo(h, byref(csbInfoAfter))

    exit(0 if csbInfoBefore.CursorPosition.Y == csbInfoAfter.CursorPosition.Y else 1)


else:
    sys.stderr.write(f"test not implemented on {system}")
    exit(1)