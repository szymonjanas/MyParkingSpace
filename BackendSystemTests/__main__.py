from Testing import SystemTest
import sys
import logging

def convertLogLevel(logLevelStr):
    if logLevelStr == "DEBUG":
        return logging.DEBUG
    if logLevelStr == "INFO":
        return logging.INFO
    if logLevelStr == "WARNING":
        return logging.WARNING
    if logLevelStr == "ERROR":
        return logging.ERROR

if __name__ == "__main__": 
    
    testcaseSimpleRegex = None
    testLogLevel = None
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "--testcase":
            testcaseSimpleRegex = sys.argv[i+1]
            i+=1
        if sys.argv[i] == "--loglevel":
            testLogLevel = sys.argv[i+1]
            testLogLevel = convertLogLevel(testLogLevel)
            i+=1
        if sys.argv[i] == "--linux":
            SystemTest.set_os(SystemTest._linux_)
        if sys.argv[i] == "--ci-linux":
            SystemTest.set_os(SystemTest._ci_linux_)

    if testLogLevel:
        SystemTest.set_log_level(testLogLevel)

    ##### IMPORT TESTS FILES
    import SystemConnectionTestServiceTests
    import AdmissionControlServiceTests
    #####

    if testcaseSimpleRegex:
        SystemTest.execute_test(testcaseSimpleRegex)
    else:
        SystemTest.execute_tests()
