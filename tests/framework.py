import inspect
import os
import sys


class ExpectationNotMet(Exception):

    def __init__(self, message):
        super().__init__(message)


class Inconclusive(Exception):

    def __init__(self, message):
        super().__init__(message)


def expect(result, message):
     if not result:
         raise ExpectationNotMet(message)


def expectsame(expected, actual, description):
    expect(expected == actual, f"{description} expected '{expected}'; got '{actual}'")


def inconclusive(message):
    raise Inconclusive(message)


class TestResult:

    def __init__(self, message=None):
        self.passed = message == None
        self.message = message


class Test:

    def __init__(self): pass

    def run(self):
        try:
            self.test()
            return TestResult()
        except Inconclusive as err:
            return TestResult(str(err))
        except ExpectationNotMet as err:
            return TestResult(f"failed: {str(err)}")
        except Exception as err:
            return (TestResult(f"error: {str(err)}"))
            
    def name(self):
        return type(self).__name__

    def test(self):
        raise Exception(f"{self.name()} does not define a 'test' method")


def run(testsuite):
    
    if testsuite not in sys.modules:
        print(f"module {testsuite} not found")
        return 

    testmodule = sys.modules[testsuite]
    tests = [ testclass() for _, testclass in inspect.getmembers(testmodule, istest) ]

    suitename = getsuitename(testmodule)
    totaltests = len(tests)
    passedtests = 0

    print(f"running test suite '{suitename}'...")

    for test in tests:

        result = test.run()
        if result.passed:
            passedtests += 1
        else:
            print(f"{test.name()}: {result.message}")

    print(f"{passedtests}/{totaltests} '{suitename}' tests passed")

    return passedtests == totaltests


def istest(member):
    return inspect.isclass(member) and isderived(member, Test)


def isderived(derived, base):
    return issubclass(derived, base) and derived != base


def getsuitename(testmodule):
    return testmodule.name if hasattr(testmodule, "name") else basefilename(testmodule.__file__)


def basefilename(path):
    return os.path.splitext(os.path.basename(path))[0]
