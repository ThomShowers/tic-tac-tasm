from framework import Test
from framework import run
from framework import ExpectationNotMet
from framework import Inconclusive
from framework import expect
from framework import expectsame
from framework import inconclusive
from framework import TestResult


class ExpectationNotMet_HasExpectedStr(Test):

    def __init__(self): super().__init__()

    def test(self):
        expected = "expected message"
        if expected != str(ExpectationNotMet(expected)):
            raise Exception("ExpectationNotMet has wrong str()")


class Inconclusive_HasExpectedStr(Test):

    def __init__(self): super().__init__()

    def test(self):
        expected = "expected message"
        if expected != str(Inconclusive(expected)):
            raise Exception("Inconclusive has wrong str()")


class Expect_False_RaisesExpectationNotMet(Test):

    def __init__(self): super().__init__()

    def test(self):
        expected = "expected message"
        try:
            expect(False, expected)
            raise Exception("expect(False) did not raise ExpectationNotMet")
        except ExpectationNotMet as err:
            if expected != str(err):
                raise Exception("raised ExpectationNotMet has wrong str()")


class Expect_True_DoesNotRaise(Test):

    def __init__(self): super().__init__()

    def test(self):
        try:
            expect(True, "should not raise")
        except Exception as err:
            raise Exception(f"expect(True) raised error '{str(err)}'")


class ExpectSame_NotSame_Raises(Test):

    def __init__(self): super().__init__()

    def test(self):
        expected = "expectation prefix"
        try:
            expectsame(1, 2, expected)
            raise Exception("expectsame(1, 2) did not raise ExpectationNotMet")
        except ExpectationNotMet as err:
            if not str(err).startswith(expected):
                raise Exception("raised ExpectationNotMet does not have expected prefix")


class ExpectSame_Same_DoesNotRaise(Test):

    def __init__(self): super().__init__()

    def test(self):
        try:
            expectsame(1, 1, "should not raise")
        except Exception as err:
            raise Exception(f"expectsame(1, 1) raised error '{str(err)}'")


class InconclusiveMethod_RaisesInconclusive(Test):

    def __init__(self): super().__init__()

    def test(self):
        expected = "inconclusive message"
        try:
            inconclusive(expected)
            raise Exception("inconclusive() did not raise Inconclusive")
        except Inconclusive as err:
            if expected != str(err):
                raise Exception("raised Inconclusive has wrong str()")


class TestResult_NoMessage_Passed(Test):

    def __init__(self): super().__init__()

    def test(self):
        if not TestResult().passed:
            raise Exception("TestResult().passed is false")
        

class TestResult_Message_FailedWithMessage(Test):

    def __init__(self): super().__init__()

    def test(self):
        expected = "expected message"
        result = TestResult(expected)
        if result.passed:
            raise Exception("TestResult(message).passed is true")
        if expected != result.message:
            raise Exception("TestResult(message) has wrong message")
            

if __name__ == "__main__":
    exit(0 if run(__name__) else 1)
