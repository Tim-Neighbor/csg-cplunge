class TwinSet:
    def __init__(self, cviv=0.0, cvp=0.0, kodec=0.0,
                 twiniv=0.0, twinp=0.0, kodee=0.0, totalm=0.0,
                 thickm=0.0, totalt=0.0, thicko=0.0, thicki=0.0,
                 widthn=0.0, widthp=0.0, is_complete=True):

        self.cviv = cviv
        self.cvp = cvp
        self.kodec = kodec
        self.twiniv = twiniv
        self.twinp = twinp
        self.kodee = kodee
        self.totalm = totalm
        self.thickm = thickm
        self.totalt = totalt
        self.thicko = thicko
        self.thicki = thicki
        self.widthn = widthn
        self.widthp = widthp
        self.is_complete = is_complete
        self.d_a = 0.0

    # Does not include widthp, because it is never editable, modifiable,
    # or reported in the original program.
    def __str__(self):
        string = ''

        string = string + '{}'.format(min_num(self.cviv)) + '\t'
        string = string + '{}'.format(min_num(self.cvp)) + '\t'
        string = string + '{}'.format(min_num(self.kodec)) + '\t'
        string = string + '{}'.format(min_num(self.twiniv)) + '\t'
        string = string + '{}'.format(min_num(self.twinp)) + '\t'
        string = string + '{}'.format(min_num(self.kodee)) + '\t'
        if self.is_complete:
            string = string + '{}'.format(min_num(self.totalm)) + '\t'
            string = string + '{}'.format(min_num(self.thickm)) + '\t'
            # this was changed from thicki, because that seems like what it should be doing
            string = string + '{}'.format(min_num(self.totalt)) + '\t'
            string = string + '{}'.format(min_num(self.thicko)) + '\t'
            string = string + '{}'.format(min_num(self.thicki)) + '\t'
            string = string + '{}'.format(min_num(self.widthn))

        return string

    def to_string(self, position):
        s = ''

        s = s + '{}'.format(min_num(position)) + '\t'
        s = s + '{}'.format(min_num(self.cviv)) + '\t'
        s = s + '{}'.format(min_num(self.cvp)) + '\t'
        s = s + '{}'.format(min_num(self.kodec)) + '\t'
        s = s + '{}'.format(min_num(self.twiniv)) + '\t'
        s = s + '{}'.format(min_num(self.twinp)) + '\t'
        s = s + '{}'.format(min_num(self.kodee)) + '\t'
        if self.is_complete:
            s = s + '{}'.format(min_num(self.totalm)) + '\t'
            s = s + '{}'.format(min_num(self.thickm)) + '\t'
            s = s + '{}'.format(min_num(self.totalt)) + '\t'
            s = s + '{}'.format(min_num(self.thicko)) + '\t'
            s = s + '{}'.format(min_num(self.thicki)) + '\t'
            s = s + '{}'.format(min_num(self.widthn))

        return s


def min_num(num):
    num = float(num)
    if num.is_integer():
        return int(num)
    else:
        return num


def format_num_to_string(num, max_num_dec=0, mandatory=False):
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
