import sys
import Testing.SystemTest as SystemTest
import Testing.SystemTestContext as context
import sys
from Server.Backend import utils

if __name__ == "__main__": 
    args = utils.ArgvDeserializer(sys.argv)
    stContext : context.SystemTestContext = context.SystemTestContext()

    testcaseSimpleRegex = args.GetArg("testcase")
    testLogLevel = utils.convertLogLevel(args.GetArg("loglevel"))
    enforceSystem = args.GetArg("os")

    if testLogLevel:
        stContext.setLogLevel(testLogLevel)
        stContext.initLogging()

    if enforceSystem == "linux":
        stContext.setSystem(context.System.linux)
    elif enforceSystem == "ci-linux":
        stContext.setSystem(context.System.ci_linux)

    if args.GetArg("emailconfig"):
        stContext.setEmailConfig()

    if args.GetArg("emailaddress"):
        stContext.setEmailAddress(args.GetArg("emailaddress"))

    if args.GetArg("emailpassword"):
        stContext.setEmailPassword(args.GetArg("emailpassword"))

    SystemTest.systemTestContext = stContext

    ##### IMPORT TESTS FILES #####
    import TestsSystemConnectionTestService
    import TestsAdmissionControlService
    import TestsSpaceReservationService
    ##############################


    if testcaseSimpleRegex:
        SystemTest.execute_test(testcaseSimpleRegex)
    else:
        SystemTest.execute_tests()
