import framework
import os
from proxys import Io
import subprocess

scriptdir = os.path.dirname(__file__)

class Println_Prints(framework.Test):

    def __init__(self): super().__init__()

    def test(self):

        expected = "line to print"

        result = subprocess.run(
            [ "python", f"{scriptdir}/io_println.py", expected ],
            stdout=subprocess.PIPE)
        
        framework.expect(result.returncode == 0, f"io_scanln.py exited with {result.returncode}")
        
        actual = result.stdout.decode("utf-8")

        if not actual.endswith(os.linesep):
            framework.inconclusive(f"io_println.py stdout missing expected '{os.linesep}'")

        actual = actual[:-len(os.linesep)]

        framework.expectsame(expected, actual, "value printed to stdout")


class Scanln_Test():

    def __init__(self): super().__init__()

    def test(self):

        result = subprocess.run(
            [ "python", f"{scriptdir}/io_scanln.py", str(self.count()) ],
            stdout=subprocess.PIPE,
            input=self.input().encode("utf-8"))

        actual = result.stdout.decode("utf-8")

        if not actual.endswith(os.linesep):
            framework.inconclusive(f"io_println.py stdout missing expected '{os.linesep}'")

        actual = actual[:-len(os.linesep)]

        framework.expectsame(self.expected(), actual, "value scanned from stdin")

    def input(self): 
        raise Exception(f"{type(self).__name__} does not define an input() method")

    def count(self):
        raise Exception(f"{type(self).__name__} does not define an count() method")

    def expected(self): 
        raise Exception(f"{type(self).__name__} does not define an expected() method")


class Scanln_ScansExpectedLine(Scanln_Test, framework.Test):

    def __init__(self): super().__init__()
        
    def input(self): return "expected string"

    def count(self): return len(self.input())

    def expected(self): return self.input()


class Scanln_BufferTooShort_LineTruncated(Scanln_Test, framework.Test):

    def __init__(self): super().__init__()

    def input(self): return f"{self.expected()} plus some extra"

    def count(self): return len(self.expected())

    def expected(self): return "expected string"


class Scanln_BufferHasExtraSpace_LineEndingsAreTrimmed(Scanln_Test, framework.Test):

    def __init__(self): super().__init__()
        
    def input(self): return "expected string"

    def count(self): return len(self.input()) + 5

    def expected(self): return self.input()


class Scanln_InputEndsWithLineSeps_LineSepsAreTrimmed(Scanln_Test, framework.Test):

    def __init__(self): super().__init__()

    def input(self): return f"{self.expected()}{os.linesep}{os.linesep}"

    def count(self): return len(self.input()) + 5

    def expected(self): return "expected line"


if __name__ == "__main__":
    exit(0 if framework.run(__name__) else 1)