from traceback import StackSummary, extract_stack


def errorAssert(condition: bool, msg: str) -> None:
    if (not condition):
        raise Exception(msg)


def throwException(msg: str) -> None:
    raise Exception(msg)


def warningAssert(condition: bool, msg: str) -> None:
    if (not condition):
        print()
        print("Warning: " + msg)
        print("Traceback stack:")

        warningStack: StackSummary = extract_stack()
        printStack(warningStack)
        print()


def throwWarning(msg: str) -> None:
    print()
    print("Warning: " + msg)
    print("Traceback stack:")

    warningStack: StackSummary = extract_stack()
    printStack(warningStack)
    print()


def printStack(errorStack: StackSummary, limit: int = -2, length: int = 2) -> None:
    errorStackLen = len(errorStack)

    if (length is None or length < 0):
        length = 0

    elif (length > errorStackLen):
        length = errorStackLen

    if (limit is None or limit >= 0):
        if (limit is None):
            limit = errorStackLen

        elif (limit > errorStackLen):
            limit = errorStackLen

        for i in range(limit - length, limit):
            print(
                "-----------------------------------------------------------------------")
            print("File: " + str(errorStack[i][0]))
            print("Line: " + str(errorStack[i][1]))
            print("Call: " + str(errorStack[i][3]))

    else:
        for i in range(errorStackLen + limit - length, errorStackLen + limit):
            print(
                "-----------------------------------------------------------------------")
            print("File: " + str(errorStack[i][0]))
            print("Line: " + str(errorStack[i][1]))
            print("Call: " + str(errorStack[i][3]))
