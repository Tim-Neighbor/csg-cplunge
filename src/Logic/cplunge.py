import math
# import msvcrt

import Collections.CPLUNGE_Wrapper as CPLUNGE_Wrapper

Wrapper = CPLUNGE_Wrapper.Wrapper
sin = math.sin
cos = math.cos
tan = math.tan
pow = math.pow
atn = math.atan
pi = math.pi
fl = float


def deg_to_rad(deg):
    return deg * (pi / 180)


def rad_to_deg(rad):
    return (rad * 180) / pi


def uv_coord(position):
    if position > 360:
        return position - 360
    elif position < 0:
        return position + 360
    else:
        return position


def arcsine(num):
    return num + (pow(num, 3) / 6) + (3 * pow(num, 5) / 20) + (15 * pow(num, 7) / 336) + (105 * pow(num, 9) / 3456)


def arcosine(num):
    return (pi / 2) - num - (pow(num, 3) / 6) - (3 * pow(num, 5) / 20) - (15 * pow(num, 7) / 336) - (105 * pow(num, 9) / 3456)


def ToRad(vars):
    vars.rp1 = deg_to_rad(vars.p1F)
    vars.rp2 = deg_to_rad(vars.p2F)
    vars.rb1 = deg_to_rad(vars.b1)
    vars.rb2 = deg_to_rad(vars.b2)


def Eqn1(vars):
    ToRad(vars)
    vars.dF = atn(math.tan(vars.rp2) / (cos(vars.rb2) *
                  cos(vars.rb1) + sin(vars.rb2) * sin(vars.rb1)))
    vars.dF = rad_to_deg(vars.dF)


def Eqn2(vars):
    ToRad(vars)
    neg_one_one = cos(vars.rb2)
    neg_one_two = cos(vars.rb1)
    neg_one = neg_one_one * neg_one_two
    zero = sin(vars.rb2) * sin(vars.rb1)
    one = (neg_one + zero)
    two = pow((cos(vars.rp2) * one), 2)
    three = pow(sin(vars.rp2), 2)
    vars.co = .80783074 - two - three


def Eqn3(vars):
    ToRad(vars)
    e1 = cos(vars.rp2) * cos(vars.rb2)
    e2 = cos(vars.rp2) * sin(vars.rb2)
    e3 = sin(vars.rp2)
    c1 = cos(vars.rp1) * cos(vars.rb1)
    c2 = cos(vars.rp1) * sin(vars.rb1)
    c3 = sin(vars.rp1)
    one = (e1 * c1 + e2 * c2 + e3 * c3)
    two = (e1 ** 2 + e2 ** 2 + e3 ** 2) ** 0.5
    three = (c1 ** 2 + c2 ** 2 + c3 ** 2) ** 0.5
    four = arcosine(float(one) / (two * three))
    five = rad_to_deg(float(four))
    vars.a = abs(float(five) - 26)
    return


def Eqn4(vars):
    ToRad(vars)
    six = cos(vars.rb2) * cos(vars.rb1) + sin(vars.rb1) * sin(vars.rb2)
    seven = 1 - sin(vars.rp2) * sin(vars.rp1) - \
        cos(vars.rp2) * cos(vars.rp1) * six
    eight = fl(seven) / 2
    nine = abs(eight) ** 0.5
    ten = arcsine(nine)
    ten = rad_to_deg(ten)
    vars.e = abs(ten) - 13
    return


def Adjust(vars):
    vars.z1 = 1
    vars.p1F = float(vars.dF)

    Eqn3(vars)

    if vars.z8 == 0:
        vars.z8 = 1

    if vars.l == 1:
        vars.b = (fl(vars.b1) + 90)
        vars.b = uv_coord(fl(vars.b))
    else:
        vars.b = (fl(vars.b1) - 90)
        vars.b = uv_coord(fl(vars.b))

    if vars.l == 0:
        vars.p = '<'
    else:
        vars.p = '>'

    if vars.b1 <= vars.b2:
        vars.b1 = fl(vars.b1 + 1)
        vars.b1 = uv_coord(fl(vars.b1))

    if vars.b1 > vars.b2:
        vars.b1 = fl(vars.b1 - 1)
        vars.b1 = uv_coord(fl(vars.b1))

    if vars.b2 < 90 and vars.b1 > 270:
        vars.b1 = fl(vars.b1 + 2)
        vars.b1 = uv_coord(fl(vars.b1))

    if vars.b1 < 90 and vars.b2 > 270:
        vars.b1 = fl(vars.b1 - 2)
        vars.b1 = uv_coord(fl(vars.b1))

    if vars.l == 1:
        vars.b = fl(vars.b1 + 90)
        vars.b = uv_coord(fl(vars.b))
    else:
        vars.b = fl(vars.b1 - 90)
        vars.b = uv_coord(fl(vars.b))
    return


def Solution(vars):
    result = []
    if (vars.z != 1) or (vars.z1 != 1):
        result.extend([vars.p9, vars.p2S, vars.p8, vars.p1S])
        needed_adjustment = False
    else:
        result.extend([vars.b, vars.p9, vars.p2S, vars.p8, vars.p1S])
        needed_adjustment = True

    return [needed_adjustment, result]


def one_twin_set(b1, b2, p2F, dS):
    vars = Wrapper()

    vars.b1 = b1
    vars.b2 = b2
    vars.p2F = p2F
    vars.dS = dS
    vars.z9 = vars.b1
    vars.c = 1
    vars.n = 10

    vars.l = 0
    if vars.dS == '-':
        vars.b2 = (vars.b2 + 180)
        vars.b2 = uv_coord(vars.b2)
    vars.b1 = (vars.b1 + 90)
    vars.b1 = uv_coord(vars.b1)

    if abs(vars.b1 - vars.b2) >= 90 and vars.b1 - vars.b2 + 360 >= 90 and abs(vars.b1 - vars.b2 - 360) >= 90:
        vars.b1 = vars.b1 + 180
        vars.b1 = uv_coord(vars.b1)
        vars.l = 1

    # Lable1

    while True:
        while True:
            while True:
                Eqn1(vars)
                Eqn2(vars)

                if vars.co >= 0 and vars.z == 2:
                    # GOSUB Adjust
                    Adjust(vars)
                    # GOTO Lable1
                else:
                    break

            if vars.co >= 0:
                vars.z = 1
                Adjust(vars)
                # GOTO Lable1
            else:
                break

        vars.dF = round(vars.dF)

        for vars.r in range(2):
            if vars.r == 0:
                vars.x = fl(vars.dF + 28)
            else:
                vars.x = fl(vars.dF - 28)

            if vars.r == 0:
                vars.s = 1
            else:
                vars.s = -1

            if vars.r == 0:
                vars.w = fl(vars.dF)
            else:
                vars.w = fl(2 * vars.dF - vars.p1F + 2)

            vars.f = fl(0)

            vars.p1F = fl(vars.w)
            while True:
                Eqn4(vars)

                if vars.e * vars.f < 0:
                    break
                else:
                    vars.f = vars.e
                    # loop increment
                    vars.p1F = vars.p1F + vars.s

                    if (vars.p1F > vars.x and vars.s > 0) or (vars.p1F < vars.x and vars.s < 0):
                        # make adjustments after exceeding count
                        if vars.z == 2:
                            Adjust(vars)
                        else:
                            vars.z = 1
                            Adjust(vars)
                        vars.gotoLable1 = True
                        break

            # tims code
            if vars.gotoLable1:
                break

            if abs(vars.e) > abs(vars.f):
                vars.p1F = vars.p1F - vars.s

            vars.p = '>'
            if vars.l == 0 and vars.p1F > 0:
                vars.p = '<'
            if vars.l == 1 and vars.p1F < 0:
                vars.p = '<'

            if vars.r == 0:
                vars.p8 = vars.p1F
            else:
                vars.p9 = vars.p1F

            if vars.r == 0:
                vars.p1S = vars.p
            else:
                vars.p2S = vars.p

        # tims code
        if vars.gotoLable1:
            vars.gotoLable1 = False
            continue

        if vars.l == 1:
            vars.b = vars.b1 + 90
            vars.b = uv_coord(vars.b)
        else:
            vars.b = vars.b1 - 90
            vars.b = uv_coord(vars.b)
        break

    return Solution(vars)


def angle(b1: float, b2: float, p2F: float, dS: str, p1F: float):
    vars = Wrapper()

    vars.z = 0

    vars.b1 = fl(b1)
    vars.b2 = fl(b2)
    vars.p2F = fl(p2F)
    vars.dS = dS

    if vars.dS == '-':
        vars.b2 = vars.b2 + 180
        vars.b2 = uv_coord(vars.b2)

    vars.b1 = vars.b1 + 90
    vars.b1 = uv_coord(vars.b1)

    if (abs(vars.b1 - vars.b2) >= 90) and (vars.b1 - vars.b2 + 360 >= 90) and (abs(vars.b1 - vars.b2 - 360) >= 90):
        vars.b1 = vars.b1 + 180
        vars.b1 = uv_coord(vars.b1)

    vars.p1F = p1F

    Eqn3(vars)

    return vars.a
