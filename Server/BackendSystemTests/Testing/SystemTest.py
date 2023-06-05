from Testing import Assert
import logging
import sys
import subprocess
import time
import requests
import psutil
import Testing.SystemTestConsts as consts
import Testing.SystemTestContext as context

systemTestContext : context.SystemTestContext = None

def convertLogLevel(loglevel):
    if loglevel == logging.DEBUG:
        return "DEBUG"
    if loglevel == logging.INFO:
        return "INFO"
    if loglevel == logging.WARN:
        return "WARN"
    if loglevel == logging.ERROR:
        return "ERROR"

class TestOutcome:
    testStatus = True
    testMessage = ""

    def __init__(self, testStatus, testMessage):
        self.testStatus = testStatus
        self.testMessage = testMessage

class TestCaseContext:
    LOG = None
    testOutcome : TestOutcome
    ipAddress = None
    portAddress = None
    SUT = None
    URL = ""
    logFilePath = ""
    serverConnectionRetries = 0

    def __init__(self, ipAddress, port, logFilePath):
        global systemTestContext
        self.LOG = systemTestContext.LOG
        self.ipAddress = ipAddress
        self.portAddress = port
        self.logFilePath = logFilePath
        self.testOutcome = TestOutcome(True, "")
        self.URL = "http://{}:{}/".format(ipAddress, port)
        self.serverConnectionRetries = 0

    def getTestOutcome(self):
        return self.testOutcome

    def isServerOnline(self):
        try:
            return "Hello World!" == requests.get(self.URL + "helloworld").text
        except ConnectionError:
            return False
        except requests.exceptions.ConnectionError:
            return False

    def __turn_off_requests_logging__(self):
        logging.getLogger("urllib3").propagate = False

    def __turn_on_requests__logging__(self):
        logging.getLogger("urllib3").propagate = True

    def connectToBackend(self):
        self.__turn_off_requests_logging__()
        while not self.isServerOnline():
            time.sleep(consts.SLEEP_TIME_BETWEEN_RETRIES_IN_SEC)
            self.serverConnectionRetries += 1
            if self.serverConnectionRetries >= consts.RETRIES_ON_TEST_INIT:
                raise ConnectionError("SystemTest could not connect to server after {} retries!"
                                        .format(self.serverConnectionRetries))
        self.__turn_on_requests__logging__()

    def __kill_process__(self, proc_pid):
        process = psutil.Process(proc_pid)
        for proc in process.children(recursive=True):
            proc.kill()
        process.kill()

    def InitTest(self):
        global systemTestContext
        cmd = [systemTestContext.getPythonRunCommand(), "Backend", 
             "--ipaddress", self.ipAddress,
             "--logfilepath", self.logFilePath,
             "--databasepath", systemTestContext.databasePath,
             "--newdatabase",
             "--loglevel", convertLogLevel(systemTestContext.loglevel) 
             ]
        if systemTestContext.IsDebug():
            self.SUT = subprocess.Popen(
                cmd,
                shell=False)
        else:
            self.SUT = subprocess.Popen(
                cmd,
                shell=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
        self.LOG.debug("Test run with command: {}".format(" ".join(cmd)))
        self.connectToBackend()
        self.LOG.debug("SystemTest connected to Backend Server successfully!")

    def FinishTest(self):
        if self.SUT:
            try:
                self.SUT.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.__kill_process__(self.SUT.pid)

class TestCaseContextGenerator:
    __ip_address_default__ = "127.0.0.0"
    __last_ip_address__ = "127.0.0.0"

    def setDefaultIpAddress(self, ipAddress : str):
        self.__ip_address_default__ = ipAddress
        self.__last_ip_address__ = ipAddress

    def IsOver250(self, value):
        return int(value) > 250

    def nextIpAddress(self):
        ipAddr = self.__last_ip_address__.split('.')
        if self.IsOver250(ipAddr[3]):
            if self.IsOver250(ipAddr[2]):
                if self.IsOver250(ipAddr[1]):
                    raise Exception("IpAddress range is overloaded!")
                else:
                    ipAddr[1] = str(int(ipAddr[3])+1)
                    ipAddr[2] = "0"    
                    ipAddr[3] = "0"    
            else:
                ipAddr[2] = str(int(ipAddr[3])+1)
                ipAddr[3] = "0"    
        else:
            ipAddr[3] = str(int(ipAddr[3])+1)
        self.__last_ip_address__ = '{}.{}.{}.{}'.format(*ipAddr)

        return self.__last_ip_address__
        # FIXME provide mechanizm for overloading 1.256, and checking if IP is taken
        # assigning only a new IP Addr will be a problem for huge amount of test

__TestCaseContextGenerator__ = TestCaseContextGenerator()

def next_ip_address():
    global __TestCaseContextGenerator__, __IP_Addr_taken__
    return __TestCaseContextGenerator__.nextIpAddress()

class TestExecutionContext:
    componentName : str
    testName : str
    testExec = None 
    testNumber : int
    testOutcome : TestOutcome
    author = None

    def __init__(self,
                 componentName,
                 testName,
                 testExec,
                 author = None):
        self.componentName = componentName
        self.testName = testName
        self.testExec = testExec
        self.author = author
        self.testOutcome = TestOutcome(True, None) 
    

    def setNumber(self, number):
        self.testNumber = number

    def setOutcome(self, outcome):
        self.testOutcome = outcome

    def execute(self, context, LOG):
        self.__log_test_run__(LOG)
        return self.testExec(context)
    
    def __log_test_run__(self, LOG):
        LOG.info("##################################################################")
        LOG.info("##################################################################")
        LOG.info("TEST RUN: [ {} ] {}::{}{}".format(
            self.testNumber, self.componentName, self.testName,
            "\n                          Author: {}".format(self.author) if (self.author) else ""))
        
    def testFail(self, message, LOG):
        self.testOutcome = TestOutcome(False, message)
        LOG.error("> FAILED: [ {} ] {}::{} \nFailure reason:\n{}".format(
            self.testNumber, self.componentName, self.testName, message))

    def testPass(self, LOG):
        LOG.info("> PASSED: [ {} ] {}::{}".format(
            self.testNumber, self.componentName, self.testName))

class TestCasesContainer:
    __test_cases__ = []
    LOG = None

    def append(self, textExecutionContext : TestExecutionContext):
        testNum = len(self.__test_cases__)
        textExecutionContext.setNumber(testNum)
        self.__test_cases__.append(textExecutionContext)
    
    def filter(self, condition):
        output = []
        for test in self.__test_cases__:
            if condition(test.testOutcome.testStatus):
                output.append(test)
        return output

    def map(self, func):
        newContainer = []
        for test in self.__test_cases__:
            if func(test):
                newContainer.append(test)
        return newContainer

    def summary(self, LOG):
        failed = self.filter(lambda status : status == False)
        if len(failed):
            LOG.error("\n\n{}\n{}\n{}\n\n".format(
                      "##############################################################",
                      "#################### Failed test summary: ####################",
                      "##############################################################"))
            for test in failed:
                LOG.error("FAIL {}.{}--{}\n{}".format(
                    test.componentName,
                    test.testName,
                    test.testNumber,
                    test.testOutcome.testMessage
                ))
        lenTotal = len(self.__test_cases__)
        lenPassed = len(self.filter(lambda status : status == True))
        lenFailed = len(failed)
        percentPassed = 0
        percentFailed = 0
        if lenTotal:
            percentPassed = int((lenPassed/lenTotal)*100)
            percentFailed = int((lenFailed/lenTotal)*100)

        LOG.info("\n\nTEST SUMMARY! TOTAL: {}, PASS: {} ({}%), FAIL: {} ({}%)".format(
            lenTotal,
            lenPassed,
            percentPassed,
            lenFailed,
            percentFailed
        ))

        if lenFailed > 0:
            sys.exit('At least one of System Test failed!')

    def execute(self, selected = None):
        global systemTestContext
        if selected != None:
            self.__test_cases__ = selected
        LOG = systemTestContext.LOG
        for test in self.__test_cases__:
            context = TestCaseContext(
                ipAddress = next_ip_address(),
                port = consts.PORT,
                logFilePath = "{}{}.{}--{}.log".format(systemTestContext.logDirectoryPath,
                                                        test.componentName,
                                                        test.testName,
                                                        test.testNumber))
            try:
                test.execute(context, LOG)
                test.testPass(LOG)
            except Assert.TestFailException as fail:
                test.testFail(fail, LOG)
            except ConnectionError as connectionError:
                test.testFail(connectionError, LOG)
            except Exception as exception:
                test.testFail(exception, LOG)
            finally:
                context.FinishTest()
        self.summary(LOG)

__TestCases__ = TestCasesContainer()

def TestCase(component_name, author=None, wip=False):
    def decorator(func):
        if (not wip): # wip = work in progress
            __TestCases__.append(
                TestExecutionContext(
                    component_name, func.__name__, func, author))        
    return decorator

def execute_tests():
    global __TestCases__, systemTestContext
    systemTestContext.clearTestsLogsDirectory()
    __TestCases__.execute()

def execute_test(testcaseSimpleRegex):
    global systemTestContext
    systemTestContext.clearTestsLogsDirectory()
    selectedTestcases = __TestCases__.map(
        lambda test : 
        (
            ("{}.{}".format(test.componentName, test.testName))
            .find(testcaseSimpleRegex) != -1
        )
    )
    __TestCases__.execute(selectedTestcases)
