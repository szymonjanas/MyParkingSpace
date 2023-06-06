from Testing.SystemTest import TestCase, TestCaseContext
from Testing import Assert
import requests

@TestCase(__name__)
def test_whenServerIsRunningPathHelloWorld_thenShouldReturnHelloWorldString(context : TestCaseContext):

    Assert.EXPECT_EQUAL(
        "Hello World!",
        requests.get(context.URL + "helloworld").text,
        "For connection validation string value must be the same!"
    )

@TestCase(__name__)
def test_whenServerIsRunningPathHelloWorld_thenShouldReturnHelloWorldStringOnSecondInstance(context : TestCaseContext):

    Assert.EXPECT_EQUAL(
        "Hello World!",
        requests.get(context.URL + "helloworld").text,
        "For connection validation string value must be the same!"
    )
