import math


def num_to_str(num, max_num_dec=0, mandatory=False):
    s = '{:0.' + str(max_num_dec) + 'f}'
    result = s.format(num)

    if not mandatory:
        result = result.rstrip('0').rstrip('.')

    if is_neg_zero(result):
        result = result.lstrip('-')

    return result


def is_neg_zero(s: str):
    if s.rstrip('0') == '-0.':
        return True
    else:
        return False


def FNACOS(x):
    # python doesnt allow division by 0 in any context
    try:
        if x == 1:
            return 1.570796 - 1.5707963267949
        else:
            return 1.570796 - math.atan(x / math.sqrt(1 - (x * x)))
    except:
        return math.nan


def FNASIN(x):
    if x == 1:
        return 1.5707963267949
    else:
        return math.atan(x / math.sqrt(1 - (x * x)))


def ABS(x):
    return abs(x)


def COS(x):
    return math.cos(x)


def SIN(x):
    return math.sin(x)


def ATN(x):
    return math.atan(x)


def SQR(x):
    return math.sqrt(x)


def POW(base, exponent):
    return math.pow(base, exponent)


def convert_point(d):
    return (d + 1) * 1000
