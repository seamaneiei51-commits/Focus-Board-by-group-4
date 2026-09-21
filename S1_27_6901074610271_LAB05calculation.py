def function1(*args):
    result = 1
    for num in args:
        result *= num
    return result


def function2(*args):
    result = 0
    for num in args:
        result += num
    return result
 