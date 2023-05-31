from Testing import Assert
import logging
import os
import subprocess
import time
import requests
import psutil

LOGS_FILE_PATH = "logs/SystemTestOutput.log"
PORT = "5566"
PYTHON_RUNNER = "py"

with open(LOGS_FILE_PATH, "w") as file:
    pass

logging.basicConfig(
    format='[%(asctime)s] %(message)s',
    handlers=[
        logging.FileHandler(LOGS_FILE_PATH),
        logging.StreamHandler()
    ],
    level=logging.DEBUG)
LOG = logging.getLogger()

def set_log_level(logLevel):
    LOG.setLevel(logLevel)

_linux_ = 1
_windows_ = 2
__system__ = _windows_
def set_os(system):
    global __system__, _linux_
    if system == _linux_:
        __system__ = _linux_
        LOG.debug("Running system tests on linux!")

def __get_python_run_command__():
    global __system__, _linux_, _windows_
    if __system__ == _linux_:
        return "python3"
    if __system__ == _windows_:
        return "py"


class TestOutcome:
    testStatus = True
    testMessage = ""

    def __init__(self, testStatus, testMessage):
        self.testStatus = testStatus
        self.testMessage = testMessage

class TestCaseContext:
    testOutcome : TestOutcome
    ipAddress = None
    portAddress = None
    SUT = None
    URL = ""
    logFilePath = ""
    serverConnectionRetries = 0

    def __init__(self, ipAddress, port, logFilePath):
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
            time.sleep(0.1)
            self.serverConnectionRetries += 1
            if self.serverConnectionRetries > 30:
                raise ConnectionError("SystemTest could not connect to server after {} retries!"
                                        .format(self.serverConnectionRetries))
        self.__turn_on_requests__logging__()

    def __kill_process__(self, proc_pid):
        process = psutil.Process(proc_pid)
        for proc in process.children(recursive=True):
            proc.kill()
        process.kill()

    def InitTest(self):
        cmd = [__get_python_run_command__(), "Backend", 
             "--ipaddress", self.ipAddress,
             "--logfilepath", self.logFilePath
             ]
        if LOG.level == LOG.debug:
            self.SUT = subprocess.Popen(
                cmd,
                shell=False)
        else:
            self.SUT = subprocess.Popen(
                cmd,
                shell=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
        LOG.debug("Test run with command: {}".format(" ".join(cmd)))
        self.connectToBackend()
        LOG.debug("SystemTest connected to Backend Server successfully!")

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

    def execute(self, context):
        self.__log_test_run__()
        return self.testExec(context)
    
    def __log_test_run__(self):
        LOG.info("________________________________________")
        LOG.info("TEST RUN: [ {} ] {}::{}{}".format(
            self.testNumber, self.componentName, self.testName,
            "\n                          Author: {}".format(self.author) if (self.author) else ""))
        
    def testFail(self, message):
        self.testOutcome = TestOutcome(False, message)
        LOG.error("> FAILED: [ {} ] {}::{} \nFailure reason:\n{}".format(
            self.testNumber, self.componentName, self.testName, message))

    def testPass(self):
        LOG.info("> PASSED: [ {} ] {}::{}".format(
            self.testNumber, self.componentName, self.testName))

class TestCasesContainer:
    __test_cases__ = []

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

    def summary(self):
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

    def execute(self, selected = None):
        global PORT
        if selected != None:
            self.__test_cases__ = selected
        for test in self.__test_cases__:
            context = TestCaseContext(
                ipAddress = next_ip_address(),
                port = PORT,
                logFilePath = "logs/systemtests/{}.{}--{}.log".format(
                                                                test.componentName,
                                                                test.testName,
                                                                test.testNumber))
            try:
                test.execute(context)
                test.testPass()
            except Assert.TestFailException as fail:
                test.testFail(fail)
            except ConnectionError as connectionError:
                test.testFail(connectionError)
            except Exception as exception:
                test.testFail(exception)
            finally:
                context.FinishTest()
        self.summary()

__TestCases__ = TestCasesContainer()

def TestCase(component_name, author=None):
    def decorator(func):
        __TestCases__.append(
            TestExecutionContext(
                component_name, func.__name__, func, author))        
    return decorator

def execute_tests():
    global __TestCases__
    __TestCases__.execute()

def execute_test(testcaseSimpleRegex):
    selectedTestcases = __TestCases__.map(
        lambda test : 
        (
            ("{}.{}".format(test.componentName, test.testName))
            .find(testcaseSimpleRegex) != -1
        )
    )
    __TestCases__.execute(selectedTestcases)
