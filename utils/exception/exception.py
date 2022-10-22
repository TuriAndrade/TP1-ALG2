from traceback import StackSummary, extract_stack
import sys


def errorAssert(condition: bool, msg: str) -> None:
    if(not condition):
        print("Error: " + msg)
        print("Traceback stack:")

        errorStack: StackSummary = extract_stack()
        printErrorStack(errorStack)
        sys.exit()


def throwException(msg: str) -> None:
    print("Error: " + msg)
    print("Traceback stack:")

    errorStack: StackSummary = extract_stack()
    printErrorStack(errorStack)
    sys.exit()


def printErrorStack(errorStack: StackSummary, limit: int = -2) -> None:
    errorStackLen = len(errorStack)

    if(limit is None or limit > errorStackLen):
        if(limit is None):
            limit = errorStackLen

        elif(limit > errorStackLen):
            limit = errorStackLen

        for i in range(limit):
            print(
                "-----------------------------------------------------------------------")
            print("File: " + str(errorStack[i][0]))
            print("Line: " + str(errorStack[i][1]))
            print("Call: " + str(errorStack[i][3]))

    else:
        for i in range(errorStackLen + limit):
            print(
                "-----------------------------------------------------------------------")
            print("File: " + str(errorStack[i][0]))
            print("Line: " + str(errorStack[i][1]))
            print("Call: " + str(errorStack[i][3]))
