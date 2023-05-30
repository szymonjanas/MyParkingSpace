from Testing.SystemTest import TestCase, TestCaseContext
from Testing import Assert
import requests

@TestCase(__name__)
def test_whenServerIsRunningPathHelloWorldShouldReturnHelloWorldString(context : TestCaseContext):
    context.InitTest()

    Assert.EXPECT_EQUAL(
        "Hello World!",
        requests.get(context.URL + "helloworld").text,
        "For connection validation string value must be the same!"
    )

    context.FinishTest()

@TestCase(__name__)
def test_whenServerIsRunningPathHelloWorldShouldReturnHelloWorldStringOnSecondInstance(context : TestCaseContext):
    context.InitTest()

    Assert.EXPECT_EQUAL(
        "Hello World!",
        requests.get(context.URL + "helloworld").text,
        "For connection validation string value must be the same!"
    )

    context.FinishTest()
