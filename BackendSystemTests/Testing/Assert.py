class TestFailException(Exception):
    pass

def EXPECT_EQUAL(a, b, description = ""):
    if (a != b):
        raise TestFailException("Values are not the same!\n> Received:\n{}\n> Expected:\n{}\n> Description: {}".format(a, b, description))

def EXPECT_TRUE(condition, description = ""):
    if (condition != True):
        raise TestFailException("Received: '{}'\nExpected: 'True'\nDescription: {}".format(condition, description))

def EXPECT_PHRASE_IN_STRING(phrase : str, string : str, description = ""):
    if not (phrase in string):
        raise TestFailException("Received: '{}'\nExpected: 'True'\nDescription: {}".format(string, phrase, description))
    # TODO Write more Expectów: false, that, equal struct, equal list, etc ...
