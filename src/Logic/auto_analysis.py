

from datetime import datetime
import os
import math
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox
from operations.num_ops import num_to_str, FNACOS, ABS, COS, SIN, POW, SQR, FNASIN, convert_point
from DataObjects.TwinSet import TwinSet
import svgwrite
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM


class AutoAnalysis():
    def __init__(self):
        # Variables from CL implementation.
        self.max_precision = 10
        self.BEAR = [0.0] * 4
        self.PLUNGE = [0.0] * 4
        self.B = [0.0] * 4
        self.P = [0.0] * 4
        self.DELGR = [0.0] * 51
        self.SLISTR = [0.0] * 7
        self.ALPHA1 = [0.0] * 4
        self.BETA1 = [0.0] * 4
        self.GAMMA1 = [0.0] * 4
        self.ALPHA2 = [0.0] * 4
        self.BETA2 = [0.0] * 4
        self.GAMMA2 = [0.0] * 4
        self.ALPHA3 = [0.0] * 4
        self.BETA3 = [0.0] * 4
        self.GAMMA3 = [0.0] * 4
        self.SLIDE = [0.0] * 4
        self.DEV = [0.0] * 151
        self.DFILE = [0.0] * 4
        self.BR = [0.0] * 4
        self.PLG = [0.0] * 4
        self.CVIV = [0.0] * 151
        self.CVP = [0.0] * 151
        self.KODEC = [0.0] * 151
        self.TWINIV = [0.0] * 151
        self.TWINP = [0.0] * 151
        self.KODEE = [0.0] * 151
        self.TOTALM = [0.0] * 151
        self.THICKM = [0.0] * 151
        self.TOTALT = [0.0] * 151
        self.THICKO = [0.0] * 151
        self.PC = [0.0] * 151
        self.QC = [0.0] * 151
        self.RC = [0.0] * 151
        self.ANGLE = [0.0] * 151
        self.ANGCVE = [0.0] * 151
        self.THICKI = [0.0] * 151
        self.DIRCG = [[0.0] * 4 for i in range(151)]
        self.DIRCE = [[0.0] * 4 for i in range(151)]
        self.TENSHR = [0.0] * 151
        self.COEFMX = [[0.0] * 6 for i in range(151)]
        self.ESLIDE = [0.0] * 7
        self.ERRR = [0.0] * 7
        self.TWINSET = [0.0] * 151
        self.CAXIS = [[0.0] * 4 for i in range(151)]
        self.TAXIS = [[0.0] * 4 for i in range(151)]
        self.WIDTHN = [0.0] * 151
        self.WIDTHP = [0.0] * 151
        self.NUMDAT = [0] * 5  # ints
        self.IROTAT = [0.0] * 151
        self.BEARC = [0.0] * 151
        self.PLUNC = [0.0] * 151
        self.BEARE = [0.0] * 151
        self.PLUNE = [0.0] * 151
        self.BEARG = [0.0] * 151
        self.PLUNG = [0.0] * 151
        self.BCOMP = [0.0] * 151
        self.PCOMP = [0.0] * 151
        self.BTENS = [0.0] * 151
        self.PTENS = [0.0] * 151
        self.ANGCE = [0.0] * 151
        self.SINDEX = [0.0] * 151
        self.AVWIDTH = [0.0] * 151
        self.EXPECT = [0.0] * 151

        self.total_num = 0
        self.file_num = 0

        self.store_SLISTR = [0.0] * 7
        self.store_BEAR = [0.0] * 4
        self.store_PLUNGE = [0.0] * 4
        self.store_BCOMP = [0.0] * 151
        self.store_PCOMP = [0.0] * 151
        self.store_BTENS = [0.0] * 151
        self.store_PTENS = [0.0] * 151
        self.store_SINDEX = [0.0] * 151
        self.store_AVWIDTH = [0.0] * 151
        self.store_EXPECT = [0.0] * 151
        self.store_BEARC = [0.0] * 151
        self.store_PLUNC = [0.0] * 151
        self.store_BEARE = [0.0] * 151
        self.store_PLUNE = [0.0] * 151
        self.store_BEARG = [0.0] * 151
        self.store_PLUNG = [0.0] * 151
        self.store_NUMDAT = [0] * 5  # ints

        # Holds the output for the report box.
        self.output = []  # strings

        # Holds the fudge type and ratio values
        self.set_ratio = 0.0
        self.set_fudge = 0

        # Holds the previous fudge type and ratio values
        self.old_set_ratio = 0.0
        self.old_set_fudge = 0

        # color objects??

        self.set_ratio = 1
        self.set_fudge = 2

        # drawings
        self.cur_drawing = None
        self.PNG_path = None

    def auto_analysis(self, i_data, i_egspi, i_con, i_dev, pr_stat, save_SVG, plot_picture,
                      data_set1: list[TwinSet], data_set2: list[TwinSet], data_set3: list[TwinSet],
                      ds1_is_rotate, ds2_is_rotate, ds3_is_rotate,
                      ds1_rotation: list, ds2_rotation: list, ds3_rotation: list, snet: bool,
                      is_snet_rotate, snet_plot_type, rot1, tilt, rot2, back_color, grid_color, point_color, icon_color):

        self.clear_data()

        self.output = []

        # todo handle fudge factors (did he?)
        i_fudge = self.set_fudge
        ratio = self.set_ratio

        self.file_num = self.load_sets(data_set1, data_set2, data_set3, ds1_is_rotate,
                                       ds2_is_rotate, ds3_is_rotate, ds1_rotation, ds2_rotation, ds3_rotation)

        if self.file_num == 0:
            self.cur_drawing = None
            return

        self.NUMDAT[1] = 0  # In the CL program, unsure why it is here.

        if i_data == 1:
            for n in range(1, self.file_num + 1):
                self.output.append('Thin Section: ' + num_to_str(n))
                self.output.append(
                    'Number of Twin Sets is: ' + num_to_str((self.NUMDAT[n + 1] - self.NUMDAT[n])))
                self.output.append('')
                self.output.append(
                    'GR\tOPTIC AX ORIEN\t\t\tTWIN SET ORIEN\t\t\tMICROTWINS\t\tTHICK TWINS\t\t\tGRN WDTH')
                self.output.append(
                    '\tINVRT\tPLUNG\t\tINVRT\tPLUNG\t\tNUM\tTHK\tNUM\tOUT\tINN\tNORTO')

                for i in range(self.NUMDAT[n] + 1, self.NUMDAT[n + 1] + 1):

                    s = ''

                    s = s + num_to_str(self.TWINSET[i], 2) + '\t'

                    ts = TwinSet(
                        self.CVIV[i],
                        self.CVP[i],
                        self.KODEC[i],
                        self.TWINIV[i],
                        self.TWINP[i],
                        self.KODEE[i],
                        self.TOTALM[i],
                        self.THICKM[i],
                        self.TOTALT[i],
                        self.THICKO[i],
                        self.THICKI[i],
                        self.WIDTHN[i]
                    )

                    s = s + ts.__str__()

                    self.output.append(s)

                self.output.append('')

                self.output.append(
                    "Data will be Rotated According to the Following Direction Cosines")
                self.output.append("L1=\t" + num_to_str(self.ALPHA1[n], 10) + "\tM1 =\t" + num_to_str(
                    self.BETA1[n], 10) + "\tN1 =\t" + num_to_str(self.GAMMA1[n], 10))
                self.output.append("L2=\t" + num_to_str(self.ALPHA2[n], 10) + "\tM2 =\t" + num_to_str(
                    self.BETA2[n], 10) + "\tN2 =\t" + num_to_str(self.GAMMA2[n], 10))
                self.output.append("L3=\t" + num_to_str(self.ALPHA3[n], 10) + "\tM3 =\t" + num_to_str(
                    self.BETA3[n], 10) + "\tN3 =\t" + num_to_str(self.GAMMA3[n], 10))

                self.output.append('')

        for n in range(1, self.file_num+1):
            nd1 = self.NUMDAT[n] + 1
            nd2 = self.NUMDAT[n + 1]

            for i in range(nd1, nd2+1):
                self.CVIV[i] = self.bearin(self.CVIV[i], self.KODEC[i])
                self.TWINIV[i] = self.bearin(self.TWINIV[i], self.KODEE[i])

            for i in range(nd1, nd2+1):
                ref_results = self.dircos(
                    self.CVIV[i], self.CVP[i], self.PC[i], self.QC[i], self.RC[i])
                self.PC[i] = ref_results[0]
                self.QC[i] = ref_results[1]
                self.RC[i] = ref_results[2]
                ref_results = self.dircos(
                    self.TWINIV[i], self.TWINP[i], self.DIRCE[i][1], self.DIRCE[i][2], self.DIRCE[i][3])
                self.DIRCE[i][1] = ref_results[0]
                self.DIRCE[i][2] = ref_results[1]
                self.DIRCE[i][3] = ref_results[2]

            if self.IROTAT[n] == 1:
                for i in range(nd1, nd2+1):
                    ref_results = self.rotate(self.PC[i], self.QC[i], self.RC[i], self.ALPHA1[n], self.ALPHA2[n], self.ALPHA3[n],
                                              self.BETA1[n], self.BETA2[n], self.BETA3[n], self.GAMMA1[n], self.GAMMA2[n], self.GAMMA3[n])
                    self.PC[i] = ref_results[0]
                    self.QC[i] = ref_results[1]
                    self.RC[i] = ref_results[2]
                    ref_results = self.rotate(self.DIRCE[i][1], self.DIRCE[i][2], self.DIRCE[i][3], self.ALPHA1[n], self.ALPHA2[n],
                                              self.ALPHA3[n], self.BETA1[n], self.BETA2[n], self.BETA3[n], self.GAMMA1[n], self.GAMMA2[n], self.GAMMA3[n])
                    self.DIRCE[i][1] = ref_results[0]
                    self.DIRCE[i][2] = ref_results[1]
                    self.DIRCE[i][3] = ref_results[2]
            for i in range(nd1, nd2+1):
                a = self.PC[i] * self.DIRCE[i][1] + self.QC[i] * \
                    self.DIRCE[i][2] + self.RC[i] * self.DIRCE[i][3]
                self.ANGLE[i] = 57.2957795 * FNACOS(a)

                if self.ANGLE[i] - 90 > 0:
                    self.PC[i] = -1 * self.PC[i]
                    self.QC[i] = -1 * self.QC[i]
                    self.RC[i] = -1 * self.RC[i]

                self.ANGCVE[i] = FNACOS(ABS(a))

            for i in range(nd1, nd2+1):
                ref_results = self.strain(self.THICKM[i], self.TOTALM[i], self.THICKO[i],
                                          self.THICKI[i], self.TOTALT[i], self.WIDTHN[i], i, ratio, i_fudge, 'C')
                self.THICKM[i] = ref_results[0]
                ref_results = self.gAxis(self.PC[i], self.QC[i], self.RC[i], self.DIRCE[i][1], self.DIRCE[i]
                                         [2], self.DIRCE[i][3], self.ANGCVE[i], self.DIRCG[i][1], self.DIRCG[i][2], self.DIRCG[i][3])
                self.DIRCG[i][1] = ref_results[0]
                self.DIRCG[i][2] = ref_results[1]
                self.DIRCG[i][3] = ref_results[2]

            for i in range(nd1, nd2+1):
                bearc = 0
                plunc = 0
                kc = 0
                beare = 0
                plune = 0
                ke = 0
                bearg = 0
                plung = 0
                kg = 0

                ref_results = self.bear_pl(
                    self.PC[i], self.QC[i], self.RC[i], bearc, plunc, kc)
                # reassign bearc, plunc, kc to simulate pass by reference
                bearc = ref_results[0]
                plunc = ref_results[1]
                kc = ref_results[2]

                ref_results = self.bear_pl(
                    self.DIRCE[i][1], self.DIRCE[i][2], self.DIRCE[i][3], beare, plune, ke)
                beare = ref_results[0]
                plune = ref_results[1]
                ke = ref_results[2]

                ref_results = self.bear_pl(
                    self.DIRCG[i][1], self.DIRCG[i][2], self.DIRCG[i][3], bearg, plung, kg)
                bearg = ref_results[0]
                plung = ref_results[1]
                kg = ref_results[2]

                self.ANGCE[i] = self.ANGCVE[i] * 57.2957795
                self.BEARC[i] = bearc
                self.PLUNC[i] = plunc
                self.BEARE[i] = beare
                self.PLUNE[i] = plune
                self.BEARG[i] = bearg
                self.PLUNG[i] = plung

            for i in range(nd1, nd2 + 1):
                bten = 0.0
                pten = 0.0
                k = 0.0  # ??
                bcomp = 0.0
                pcomp = 0.0

                ref_results = self.ct_axis(self.PC[i], self.QC[i], self.RC[i], self.DIRCE[i][1], self.DIRCE[i][2], self.DIRCE[i][3],
                                           self.ANGCVE[i], self.TAXIS[i][1], self.TAXIS[i][2], self.TAXIS[i][3], self.CAXIS[i][1], self.CAXIS[i][2], self.CAXIS[i][3])
                self.TAXIS[i][1] = ref_results[0]
                self.TAXIS[i][2] = ref_results[1]
                self.TAXIS[i][3] = ref_results[2]
                self.CAXIS[i][1] = ref_results[3]
                self.CAXIS[i][2] = ref_results[4]
                self.CAXIS[i][3] = ref_results[5]

                ref_results = self.bear_pl(
                    self.TAXIS[i][1], self.TAXIS[i][2], self.TAXIS[i][3], bten, pten, k)
                bten = ref_results[0]
                pten = ref_results[1]
                k = ref_results[2]

                ref_results = self.bear_pl(
                    self.CAXIS[i][1], self.CAXIS[i][2], self.CAXIS[i][3], bcomp, pcomp, k)
                bcomp = ref_results[0]
                pcomp = ref_results[1]
                k = ref_results[2]

                if (self.TOTALM[i] + self.TOTALT[i]) == 0:
                    self.AVWIDTH[i] = math.nan
                else:
                    self.AVWIDTH[i] = (self.TOTALM[i] * self.THICKM[i] + self.TOTALT[i]
                                       * self.THICKI[i]) / (self.TOTALM[i] + self.TOTALT[i])  # pot 0

                if self.WIDTHN[i] == 0:
                    self.SINDEX[i] = math.nan
                else:
                    self.SINDEX[i] = (
                        self.TOTALM[i] + self.TOTALT[i]) / (self.WIDTHN[i] * 0.001)  # pot 0

                self.BCOMP[i] = bcomp
                self.PCOMP[i] = pcomp
                self.BTENS[i] = bten
                self.PTENS[i] = pten

            if i_egspi == 1:
                self.output.append('\n')

                self.output.append(
                    "Thin Section: " + num_to_str(self.SLIDE[n], self.max_precision))
                self.output.append("Number of Twin Sets is " +
                                   str((self.NUMDAT[n + 1] - self.NUMDAT[n])))
                self.output.append(
                    "THICKTWIN/MICROTWIN Ration = " + str(ratio))
                self.output.append("Thick Twin Option is " + str(i_fudge))

                if self.IROTAT[n] == 1:
                    self.output.append('')
                    self.output.append(
                        'Angles are with Respect to the Rotated Coordiante System')

                self.output.append('')

                self.output.append(
                    'TW\tBEARC\tPLUNC\tBEARE\tPLUNE\tANGCE\tBEARG\tPLUNG\tTANS/2 ')

                for i in range(nd1, nd2 + 1):
                    s = ''

                    s = s + num_to_str(self.TWINSET[i], 2) + '\t'
                    s = s + num_to_str(self.BEARC[i], 2) + '\t'
                    s = s + num_to_str(self.PLUNC[i], 2) + '\t'
                    s = s + num_to_str(self.BEARE[i], 2) + '\t'
                    s = s + num_to_str(self.PLUNE[i], 2) + '\t'
                    s = s + num_to_str(self.ANGCE[i], 2) + '\t'
                    s = s + num_to_str(self.BEARG[i], 2) + '\t'
                    s = s + num_to_str(self.PLUNG[i], 2) + '\t'
                    s = s + num_to_str(self.TENSHR[i], 2)

                    self.output.append(s)

                self.output.append('\n')
                self.output.append(
                    'Dynamic Analysis of Thin Section  ' + str(self.SLIDE[n]))

                if self.IROTAT[n] == 1:
                    self.output.append(
                        'Angles are with Respect to the Rotated Coordinate System')

                self.output.append('')

                self.output.append(
                    'TW\tCOMP AXES\t\tTENS AXES\t\tPER MM AV WIDTH')
                self.output.append('\tBEAR\tPL\tBEAR\tPL')

                for i in range(nd1, nd2 + 1):
                    s = ''

                    s = s + num_to_str(self.TWINSET[i], 2) + '\t'
                    s = s + num_to_str(self.BCOMP[i], 2) + '\t'
                    s = s + num_to_str(self.PCOMP[i], 2) + '\t'
                    s = s + num_to_str(self.BTENS[i], 2) + '\t'
                    s = s + num_to_str(self.PTENS[i], 2) + '\t'
                    s = s + num_to_str(self.SINDEX[i], 2) + '\t'
                    s = s + num_to_str(self.AVWIDTH[i], 2)

                    self.output.append(s)

        # next N

        if self.file_num == 1:
            self.total_num = self.NUMDAT[2]
        elif self.file_num == 2:
            self.total_num = self.NUMDAT[3]
        elif self.file_num == 3:
            self.total_num = self.NUMDAT[4]

        for m in range(1, self.total_num + 1):
            self.TWINSET[m] = m

        temp_string = ''
        ref_results = self.spang(self.total_num, i_con, temp_string)
        self.total_num = ref_results[0]
        i_con = ref_results[1]
        temp_string = ref_results[2]

        self.datat(self.total_num)

        '''
        if (flag3 == 1)
        {
            CVIV = null;
            CVP = null;
            KODEC = null;
            TWINIV = null;
            TWINP = null;
            KODEE = null;
        }
        '''

        self.regres(self.total_num, 5, i_con)
        self.tidy_up(i_con)

        tot_width = 0.0
        tot_num_twn = 0.0
        tot_gr_width = 0.0

        if i_fudge == 1:
            for i in range(1, self.total_num + 1):
                tot_width = tot_width + \
                    (self.TOTALM[i] * self.THICKM[i] +
                     self.TOTALT[i] * self.THICKO[i])
        elif i_fudge == 2:
            for i in range(1, self.total_num + 1):
                tot_width = tot_width + \
                    (self.TOTALM[i] * self.THICKM[i] +
                     self.TOTALT[i] * self.THICKI[i])
        elif i_fudge == 3:
            for i in range(1, self.total_num + 1):
                if self.THICKO[i] == 0:
                    tot_width = math.nan
                    break
                else:
                    tot_width = tot_width + \
                        (self.TOTALM[i] * self.THICKM[i] + self.TOTALT[i]
                         * ((self.THICKI[i] / self.THICKO[i]) / 2))

        for ii in range(1, self.total_num + 1):
            tot_num_twn = tot_num_twn + (self.TOTALM[ii] + self.TOTALT[ii])
            tot_gr_width = tot_gr_width + self.WIDTHN[ii]

        if tot_num_twn == 0:
            tot_av_width = math.nan
        else:
            tot_av_width = tot_width / tot_num_twn  # pot 0

        if tot_gr_width == 0:
            tot_sindex = math.nan
        else:
            tot_sindex = tot_num_twn / (tot_gr_width * 0.001)  # pot 0

        self.output.append(
            'The average twin width (MICRONS) for the sample is: ' + str(tot_av_width))
        self.output.append(
            'The average twin intensity (TWINS/MM) for the sample is: ' + str(tot_sindex))

        temp_string2 = ''

        self.deviat(self.total_num, i_dev, self.file_num + 1, temp_string2)

        highwater = 0
        for i in range(1, 4):
            if self.NUMDAT[i] > highwater:
                highwater = self.NUMDAT[i]

        # TODO check if this works
        if snet:
            ref_results = self.snet_menu(highwater, '', self.BCOMP, self.PCOMP, self.BTENS, self.PTENS,
                                         self.BEARE, self.PLUNE, self.BEARC, self.PLUNC, self.BEARG, self.PLUNG, save_SVG, plot_picture, snet_plot_type, is_snet_rotate, rot1, tilt, rot2, back_color, grid_color, point_color, icon_color)
            self.BCOMP = ref_results[0]
            self.PCOMP = ref_results[1]
            self.BTENS = ref_results[2]
            self.PTENS = ref_results[3]
            self.BEARE = ref_results[4]
            self.PLUNE = ref_results[5]
            self.BEARC = ref_results[6]
            self.PLUNC = ref_results[7]
            self.BEARG = ref_results[8]
            self.PLUNG = ref_results[9]

    def load_sets(self, data_set1, data_set2, data_set3, ds1_is_rotate, ds2_is_rotate, ds3_is_rotate, ds1_rotation, ds2_rotation, ds3_rotation):
        all_sets = []

        max_twinsets = 0
        max_twinsets = self.load_single_set(
            data_set1, max_twinsets, all_sets, ds1_is_rotate, ds1_rotation)
        max_twinsets = self.load_single_set(
            data_set2, max_twinsets, all_sets, ds2_is_rotate, ds2_rotation)
        max_twinsets = self.load_single_set(
            data_set3, max_twinsets, all_sets, ds3_is_rotate, ds3_rotation)

        if max_twinsets == 0:
            return 0

        # emulates FileOpen

        num = [0] * 5
        num[1] = 1
        self.NUMDAT[1] = 1
        l = 1

        for cur_set in all_sets:
            cur_pos = 1
            for cur_twin in cur_set:
                self.TWINSET[num[l]] = cur_pos
                self.CVIV[num[l]] = cur_twin.cviv
                self.CVP[num[l]] = cur_twin.cvp
                self.KODEC[num[l]] = cur_twin.kodec
                self.TWINIV[num[l]] = cur_twin.twiniv
                self.TWINP[num[l]] = cur_twin.twinp
                self.KODEE[num[l]] = cur_twin.kodee
                self.TOTALM[num[l]] = cur_twin.totalm
                self.THICKM[num[l]] = cur_twin.thickm
                self.TOTALT[num[l]] = cur_twin.totalt
                self.THICKO[num[l]] = cur_twin.thicko
                self.THICKI[num[l]] = cur_twin.thicki
                self.WIDTHN[num[l]] = cur_twin.widthn
                self.WIDTHP[num[l]] = cur_twin.widthp

                cur_pos += 1
                num[l] = num[l] + 1

            # end 'file"
            self.NUMDAT[l + 1] = num[l] - 1
            l += 1
            num[l] = num[l - 1]
        # end FileOpen
        return len(all_sets)

    def load_single_set(self, data_set: list[TwinSet], max_twinsets, all_sets: list, ds_is_rotate, ds_rotation: list):
        if data_set == None or len(data_set) == 0:
            return max_twinsets

        max_twinsets += 1
        all_sets.append(data_set)
        if ds_is_rotate:
            self.IROTAT[max_twinsets] = 1
            set_rotations = ds_rotation
            self.ALPHA1[max_twinsets] = set_rotations[0]
            self.ALPHA2[max_twinsets] = set_rotations[3]
            self.ALPHA3[max_twinsets] = set_rotations[6]
            self.BETA1[max_twinsets] = set_rotations[1]
            self.BETA2[max_twinsets] = set_rotations[4]
            self.BETA3[max_twinsets] = set_rotations[7]
            self.GAMMA1[max_twinsets] = set_rotations[2]
            self.GAMMA2[max_twinsets] = set_rotations[5]
            self.GAMMA3[max_twinsets] = set_rotations[8]

        return max_twinsets

    def clear_data(self):
        self.BEAR = [0.0] * 4
        self.PLUNGE = [0.0] * 4
        self.B = [0.0] * 4
        self.P = [0.0] * 4
        self.DELGR = [0.0] * 51
        self.SLISTR = [0.0] * 7
        self.ALPHA1 = [0.0] * 4
        self.BETA1 = [0.0] * 4
        self.GAMMA1 = [0.0] * 4
        self.ALPHA2 = [0.0] * 4
        self.BETA2 = [0.0] * 4
        self.GAMMA2 = [0.0] * 4
        self.ALPHA3 = [0.0] * 4
        self.BETA3 = [0.0] * 4
        self.GAMMA3 = [0.0] * 4
        self.SLIDE = [0.0] * 4
        self.DEV = [0.0] * 151
        self.DFILE = [0.0] * 4
        self.BR = [0.0] * 4
        self.PLG = [0.0] * 4
        self.CVIV = [0.0] * 151
        self.CVP = [0.0] * 151
        self.KODEC = [0.0] * 151
        self.TWINIV = [0.0] * 151
        self.TWINP = [0.0] * 151
        self.KODEE = [0.0] * 151
        self.TOTALM = [0.0] * 151
        self.THICKM = [0.0] * 151
        self.TOTALT = [0.0] * 151
        self.THICKO = [0.0] * 151
        self.PC = [0.0] * 151
        self.QC = [0.0] * 151
        self.RC = [0.0] * 151
        self.ANGLE = [0.0] * 151
        self.ANGCVE = [0.0] * 151
        self.THICKI = [0.0] * 151
        self.DIRCG = [[0.0] * 4 for i in range(151)]
        self.DIRCE = [[0.0] * 4 for i in range(151)]
        self.TENSHR = [0.0] * 151
        self.COEFMX = [[0.0] * 6 for i in range(151)]
        self.ESLIDE = [0.0] * 7
        self.ERRR = [0.0] * 7
        self.TWINSET = [0.0] * 151
        self.CAXIS = [[0.0] * 4 for i in range(151)]
        self.TAXIS = [[0.0] * 4 for i in range(151)]
        self.WIDTHN = [0.0] * 151
        self.WIDTHP = [0.0] * 151
        self.NUMDAT = [0] * 5  # ints
        self.IROTAT = [0.0] * 151
        self.BEARC = [0.0] * 151
        self.PLUNC = [0.0] * 151
        self.BEARE = [0.0] * 151
        self.PLUNE = [0.0] * 151
        self.BEARG = [0.0] * 151
        self.PLUNG = [0.0] * 151
        self.BCOMP = [0.0] * 151
        self.PCOMP = [0.0] * 151
        self.BTENS = [0.0] * 151
        self.PTENS = [0.0] * 151
        self.ANGCE = [0.0] * 151
        self.SINDEX = [0.0] * 151
        self.AVWIDTH = [0.0] * 151
        self.EXPECT = [0.0] * 151

        self.total_num = 0
        self.file_num = 0

    def bearin(self, siv, kode):
        newang = 0.0
        if kode == 1:
            newang = 180 - siv
        elif kode == 2:
            newang = 270 - siv
        elif kode == 3:
            newang = 360 - siv
        elif kode == 4:
            newang = 90 - siv

        if newang < 0:
            newang = 360 + newang

        return newang

    def dircos(self, baring, plunge, p, q, r):
        con = 0.01745

        p = COS(plunge * con) * COS(baring * con)
        q = COS(plunge * con) * SIN(baring * con)
        r = SIN(plunge * con)

        return [p, q, r]

    def rotate(self, p, q, r, al1, al2, al3, bet1, bet2, bet3, gam1, gam2, gam3):
        rol = al1 * p + al2 * q + al3 * r
        rom = bet1 * p + bet2 * q + bet3 * r
        r = gam1 * p + gam2 * q + gam3 * r
        p = rol
        q = rom

        return [p, q, r]

    def bear_pl(self, p, q, r, bear, plunge, k):
        pp = p
        qq = q + 0.00001  # unsure of purpose
        rr = r
        theta = 57.29578 * math.atan(pp/qq)

        k = 0

        if rr < 0:
            pp = -p
            qq = -q
            rr = -r
            k = 1

        if qq >= 0:
            bear = 90 - theta
        else:
            bear = 270 - theta

        d = 57.29578 * FNACOS(rr)

        plunge = 90 - d

        return [bear, plunge, k]

    def ct_axis(self, pc, qc, rc, pe, qe, re, angcve, ta, tb, tc, ca, cb, cc):
        a = qc * re - qe * rc
        b = pe * rc - pc * re
        c = pc * qe - pe * qc
        d = POW(a, 2) + POW(b, 2) + POW(c, 2)

        if c == 0:
            c = 0.0000001
        if d <= 0:
            d = 0.00001

        angt = COS(45 * .0174533 - angcve)
        ya = (qc * c - rc * b) * 0.70711
        yb = (rc * a - pc * c) * 0.70711
        za = (qe * c - re * b) * angt
        zb = (re * a - pe * c) * angt
        ta = (ya - za) / d
        tb = (yb - zb) / d
        tc = (a * (ya - za) + b * (yb - zb)) / (c * d)
        tc = -1 * tc
        angt = COS(45 * .0174533 + angcve)
        za = (qe * c - re * b) * angt
        zb = (re * a - pe * c) * angt
        ca = (ya - za) / d
        cb = (yb - zb) / d
        cc = (a * (ya - za) + b * (yb - zb)) / (c * d)
        cc = -1 * cc

        return [ta, tb, tc, ca, cb, cc]

    def gAxis(self, pc, qc, rc, pe, qe, re, angcve, pg, qg, rg):
        coscvg = COS(90 * 0.0174533 - angcve)

        a = qc * re - qe * rc
        b = pe * rc - pc * re
        c = pc * qe - pe * qc
        d = POW(a, 2) + POW(b, 2) + POW(c, 2)

        if d <= 0:
            d = 0.000001
        else:
            rg = ((pe * b - qe * a) * coscvg) / d
            qg = ((re * a - pe * c) * coscvg) / d
            pg = ((qe * c - re * b) * coscvg) / d

        return [pg, qg, rg]

    def strain(self, thick_m, total_m, thick_o, thick_i, total_t, width_n, i, ratio, i_fudge, caldol):
        thick_m = ratio * thick_m

        thick_t = 0.0

        if total_t != 0:
            if i_fudge == 1:
                thick_t = thick_o
            elif i_fudge == 2:
                thick_t = thick_i
            elif i_fudge == 3:
                thick_t = (thick_o + thick_i) / 2.0

        if caldol == 'C':
            if width_n == 0:
                self.TENSHR[i] = math.nan
            else:
                # pot 0
                self.TENSHR[i] = 0.347 * \
                    ((thick_m * total_m + thick_t * total_t) / width_n)
        elif caldol == 'D':
            if width_n == 0:
                self.TENSHR[i] = math.nan
            else:
                # pot 0
                self.TENSHR[i] = 0.2395 * \
                    ((thick_m * total_m + thick_t * total_t) / width_n)

        return [thick_m]

    def tidy_up(self, i_con):
        prinax = [0.0] * 10

        self.SLISTR[1] = self.ESLIDE[1]
        self.SLISTR[2] = self.ESLIDE[3]
        self.SLISTR[3] = self.ESLIDE[2]
        self.SLISTR[4] = self.ESLIDE[5]
        self.SLISTR[5] = self.ESLIDE[4]
        self.SLISTR[6] = self.ESLIDE[6]

        unimportant1 = 0.0
        unimportant2 = 1.0
        unimportant3 = 2.0

        ref_results = self.eigen(self.SLISTR, prinax, 3, 0)
        self.SLISTR = ref_results[0]
        prinax = ref_results[1]

        ref_results = self.bear_pl(
            prinax[1], prinax[2], prinax[3], self.BEAR[1], self.PLUNGE[1], unimportant1)
        self.BEAR[1] = ref_results[0]
        self.PLUNGE[1] = ref_results[1]
        unimportant1 = ref_results[2]

        ref_results = self.bear_pl(
            prinax[4], prinax[5], prinax[6], self.BEAR[2], self.PLUNGE[2], unimportant2)
        self.BEAR[2] = ref_results[0]
        self.PLUNGE[2] = ref_results[1]
        unimportant2 = ref_results[2]

        ref_results = self.bear_pl(
            prinax[7], prinax[8], prinax[9], self.BEAR[3], self.PLUNGE[3], unimportant3)
        self.BEAR[3] = ref_results[0]
        self.PLUNGE[3] = ref_results[1]
        unimportant3 = ref_results[2]

        LambdaPrim1 = self.SLISTR[1] * 100
        LambdaPrim2 = self.SLISTR[3] * 100
        LambdaPrim3 = self.SLISTR[6] * 100

        alStr = LambdaPrim1 * LambdaPrim2 + LambdaPrim2 * \
            LambdaPrim3 + LambdaPrim3 * LambdaPrim1
        allStrain = SQR(ABS(alStr))

        self.output.append('\n')
        self.output.append('Twinning Strain and Orientation of Principle Axis')
        if i_con == 1:
            self.output.append('\tPrin.\tBearing\tPlunge')
            self.output.append('\tStrain')
        elif i_con == 0:
            self.output.append('\tPr Str. Bearing Plunge')

        s = ''

        s += 'e1:\t'
        s += num_to_str(LambdaPrim1, 3, True) + '\t'
        s += num_to_str(self.BEAR[1], 3, True) + '\t'
        s += num_to_str(self.PLUNGE[1], 3, True)
        self.output.append(s)

        s = ''

        s += 'e2:\t'
        s += num_to_str(LambdaPrim2, 3, True) + '\t'
        s += num_to_str(self.BEAR[2], 3, True) + '\t'
        s += num_to_str(self.PLUNGE[2], 3, True)
        self.output.append(s)

        s = ''

        s += 'e3:\t'
        s += num_to_str(LambdaPrim3, 3, True) + '\t'
        s += num_to_str(self.BEAR[3], 3, True) + '\t'
        s += num_to_str(self.PLUNGE[3], 3, True)
        self.output.append(s)

        s = ''

        self.output.append('e1, e2, and e3 are percent enlongations')
        self.output.append('')

        s += 'Total Distortion by Twinning SQRT(J2) in Percent Strain: '
        s += num_to_str(allStrain, 3)

        self.output.append(s)

    def spang(self, num, i_con, sample):
        conels = [0.0] * 7
        strn = [0.0] * 151
        prinax = [0.0] * 10

        for n in range(1, num + 1):
            strn[n] = 1.0 / num

        self.output.append('')

        self.output.append('Sample ' + str(sample))
        self.output.append(
            'Spang Numerical Dynamic Analysis: Number of Twin Sets = ' + str(num))

        for n in range(1, 7):
            conels[n] = 0

        for n in range(1, num + 1):
            conels[1] = conels[1] + \
                (POW(self.TAXIS[n][1], 2) - POW(self.CAXIS[n][1], 2)) * strn[n]
            conels[3] = conels[3] + \
                (POW(self.TAXIS[n][2], 2) - POW(self.CAXIS[n][2], 2)) * strn[n]
            conels[6] = conels[6] + \
                (POW(self.TAXIS[n][3], 2) - POW(self.CAXIS[n][3], 2)) * strn[n]
            conels[2] = conels[2] + (self.TAXIS[n][1] * self.TAXIS[n]
                                     [2] - self.CAXIS[n][1] * self.CAXIS[n][2]) * strn[n]
            conels[4] = conels[4] + (self.TAXIS[n][1] * self.TAXIS[n]
                                     [3] - self.CAXIS[n][1] * self.CAXIS[n][3]) * strn[n]
            conels[5] = conels[5] + (self.TAXIS[n][2] * self.TAXIS[n]
                                     [3] - self.CAXIS[n][2] * self.CAXIS[n][3]) * strn[n]

        ref_results = self.eigen(conels, prinax, 3, 0)
        conels = ref_results[0]
        prinax = ref_results[1]

        bear1 = 0.0
        bear2 = 0.0
        bear3 = 0.0
        plung1 = 0.0
        plung2 = 0.0
        plung3 = 0.0
        k = 0.0

        ref_results = self.bear_pl(
            prinax[1], prinax[2], prinax[3], bear1, plung1, k)
        bear1 = ref_results[0]
        plung1 = ref_results[1]
        k = ref_results[2]

        ref_results = self.bear_pl(
            prinax[4], prinax[5], prinax[6], bear2, plung2, k)
        bear2 = ref_results[0]
        plung2 = ref_results[1]
        k = ref_results[2]

        ref_results = self.bear_pl(
            prinax[7], prinax[8], prinax[9], bear3, plung3, k)
        bear3 = ref_results[0]
        plung3 = ref_results[1]
        k = ref_results[2]

        self.output.append('')

        self.output.append('EIGENVALUES AND EIGENVECTORS')
        self.output.append('MAG\tBEAR\tPLUNG')

        s = ''
        s += num_to_str(conels[1], 3) + '\t'
        s += num_to_str(bear1, 3) + '\t'
        s += num_to_str(plung1, 3)
        self.output.append(s)

        s = ''
        s += num_to_str(conels[3], 3) + '\t'
        s += num_to_str(bear2, 3) + '\t'
        s += num_to_str(plung2, 3)
        self.output.append(s)

        s = ''
        s += num_to_str(conels[6], 3) + '\t'
        s += num_to_str(bear3, 3) + '\t'
        s += num_to_str(plung3, 3)
        self.output.append(s)

        s = ''

        return [num, i_con, sample]

    def eigen(self, a: list, r: list, n: int, mv):
        range_ = 0.000001

        if (mv - 1) != 0:
            iq = (-1 * n)

            for j in range(1, n + 1):
                iq += n

                for i in range(1, n + 1):
                    ij = iq + i
                    r[ij] = 0

                    if i - j == 0:
                        r[ij] = 1
        # end select

        anorm = 0.0

        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if i - j != 0:
                    ia = i + (j * j - j) // 2
                    anorm = anorm + a[ia] * a[ia]

        n1 = n

        if anorm > 0:
            anorm = 1.414 * SQR(anorm)
            anrmx = anorm * range_ / n1

            ind = 0
            thr = anorm

            while True:  # endless DO
                thr = thr / n1

                while True:  # endless DO
                    l = 1

                    while True:  # endless DO
                        m = l + 1

                        while True:
                            mq = (m * m - m) // 2
                            lq = (l * l - l) // 2
                            lm = l + mq

                            if ABS(a[lm]) - thr >= 0:
                                ind = 1
                                ll = l + lq
                                mm = m + mq

                                x = 0.5 * (a[ll] - a[mm])
                                y = (-1 * a[lm]) / SQR(a[lm] * a[lm] + x * x)

                                if x < 0:
                                    y = -1 * y

                                sinX = y / SQR(2 * (1 + (SQR(1 - y * y))))
                                sinX2 = sinX * sinX
                                cosX = SQR(1 - sinX2)
                                cosX2 = cosX * cosX
                                sinCS = sinX * cosX

                                ilq = n * (l - 1)
                                imq = n * (m - 1)

                                for i in range(1, n + 1):
                                    iq = (i * i - i) // 2
                                    if (i - l) != 0:
                                        if (i - m) < 0:
                                            im = i + mq

                                            il = 0

                                            if (i - l) < 0:
                                                il = i + lq
                                            else:
                                                il = l + iq

                                            x = a[il] * cosX - a[im] * sinX
                                            a[im] = a[il] * sinX + a[im] * cosX
                                            a[il] = x
                                        elif (i - m) > 0:
                                            im = m + iq

                                            il = 0

                                            if (i - l) < 0:
                                                il = i + lq
                                            else:
                                                il = l + iq

                                            x = a[il] * cosX - a[im] * sinX
                                            a[im] = a[il] * sinX + a[im] * cosX
                                            a[il] = x

                                    if (mv - 1) != 0:
                                        ilr = ilq + i
                                        imr = imq + i

                                        x = r[ilr] * cosX - r[imr] * sinX
                                        r[imr] = r[ilr] * sinX + r[imr] * cosX
                                        r[ilr] = x

                                x = 2 * a[lm] * sinCS
                                y = a[ll] * cosX2 + a[mm] * sinX2 - x
                                x = a[ll] * sinX2 + a[mm] * cosX2 + x
                                a[lm] = (a[ll] - a[mm]) * sinCS + \
                                    a[lm] * (cosX2 - sinX2)
                                a[ll] = y
                                a[mm] = x

                            if (m - n) != 0:
                                m += 1
                            elif (m - n) == 0:
                                break

                        if (l - (n - 1)) != 0:
                            l = l + 1
                        elif (l - (n - 1)) == 0:
                            break

                    if (ind - 1) == 0:
                        ind = 0
                    elif (ind - 1) != 0:
                        break

                if (thr - anrmx <= 0):
                    break

        IQ = -1 * n  # IQ in original program

        for i in range(1, n + 1):
            IQ = IQ + n
            ll = i + (i * i - i) // 2
            jq = n * (i - 2)

            for j in range(i, n + 1):
                jq = jq + n
                mm = j + (j * j - j) // 2

                if a[ll] - a[mm] < 0:
                    x = float(a[ll])
                    a[ll] = a[mm]
                    a[mm] = x

                    if (mv - 1) != 0:
                        for k in range(1, n + 1):
                            ilr = IQ + k
                            imr = jq + k
                            x = r[ilr]
                            r[ilr] = r[imr]
                            r[imr] = x

        return [a, r]

    def regres(self, num, n_col, i_con):
        coeftr = [[0.0] * 151 for i in range(6)]
        l = [0] * 6
        m = [0] * 6
        covect = [0.0] * 26
        xy = [0.0] * 6

        for j in range(1, n_col + 1):
            for i in range(1, num + 1):
                coeftr[j][i] = self.COEFMX[i][j]

        for j in range(1, n_col + 1):
            ji = (j - 1) * n_col

            for i in range(1, n_col + 1):
                zij = 0.0

                for k in range(1, num + 1):
                    zij = coeftr[j][k] * self.COEFMX[k][i] + zij

                covect[i + ji] = zij

        # There was no D prior to this call, nor is it used outside of this.
        d = 0.0

        ref_results = self.minv(covect, n_col, d, l, m)
        covect = ref_results[0]
        n_col = ref_results[1]
        d = ref_results[2]
        l = ref_results[3]
        m = ref_results[4]

        for i in range(1, n_col + 1):
            xy[i] = 0

            for j in range(1, num + 1):
                xy[i] = coeftr[i][j] * self.TENSHR[j] + xy[i]

        for i in range(1, n_col + 1):
            ii = (i - 1) * n_col
            self.ESLIDE[i] = 0.0

            for j in range(1, n_col + 1):
                self.ESLIDE[i] = self.ESLIDE[i] + covect[j + ii] * xy[j]

        self.ESLIDE[6] = (-1 * self.ESLIDE[1]) - self.ESLIDE[2]

        yy = 0.0

        for i in range(1, num + 1):
            yy += POW(self.TENSHR[i], 2)

        bxy = 0.0

        for i in range(1, n_col + 1):
            bxy += self.ESLIDE[i] * xy[i]

        sse = yy - bxy

        varnce = -1.0
        if (num - n_col) == 0:
            varnce = 0
        elif (num - n_col) != 0:
            varnce = sse / (num - n_col)

        if varnce >= 0:
            jdiag = 1
            neg = -1  # placeholder value
            for i in range(1, n_col + 1):
                if covect[jdiag] >= 0:
                    neg = 1
                    self.ERRR[i] = SQR(varnce) * SQR(covect[jdiag])
                    jdiag = jdiag + 1 + n_col
                elif covect[jdiag] < 0:
                    neg = 1
                    break

            if neg == 1:
                self.ERRR[6] = SQR(POW(self.ERRR[1], 2) + POW(self.ERRR[2], 2))

        # end select

        self.output.append('')

        self.output.append('Least squares strain calculation')

        temp = ''

        temp = "Sum of squares 'Error' = "
        temp += num_to_str(sse, 7)
        self.output.append(temp)
        temp = 'Sample varience = '
        temp += num_to_str(varnce, 7)
        self.output.append(temp)

        sterror = 0.5 * (self.ERRR[1] + self.ERRR[2]) * 100

        self.output.append(
            'Standard ERR of strain components = ' + str(sterror))

        self.output.append('')

        temp = 'EX = '
        temp += num_to_str(self.ERRR[1], 7)
        self.output.append(temp)

        temp = 'EY = '
        temp += num_to_str(self.ERRR[2], 7)
        self.output.append(temp)

        temp = 'EXY = '
        temp += num_to_str(self.ERRR[3], 7)
        self.output.append(temp)

        temp = 'EYZ = '
        temp += num_to_str(self.ERRR[4], 7)
        self.output.append(temp)

        temp = 'EXZ = '
        temp += num_to_str(self.ERRR[5], 7)
        self.output.append(temp)

        temp = 'EZ = '
        temp += num_to_str(self.ERRR[6], 7)
        self.output.append(temp)

    def datat(self, n):
        for i in range(1, n + 1):
            self.COEFMX[i][1] = self.DIRCE[i][1] * \
                self.DIRCG[i][1] - self.DIRCE[i][3] * self.DIRCG[i][3]
            self.COEFMX[i][2] = self.DIRCE[i][2] * \
                self.DIRCG[i][2] - self.DIRCE[i][3] * self.DIRCG[i][3]
            self.COEFMX[i][3] = self.DIRCE[i][1] * \
                self.DIRCG[i][2] + self.DIRCE[i][2] * self.DIRCG[i][1]
            self.COEFMX[i][4] = self.DIRCE[i][2] * \
                self.DIRCG[i][3] + self.DIRCE[i][3] * self.DIRCG[i][2]
            self.COEFMX[i][5] = self.DIRCE[i][3] * \
                self.DIRCG[i][1] + self.DIRCE[i][1] * self.DIRCG[i][3]

    def deviat(self, i, iDev, n, sample: str):
        num = self.NUMDAT[(n + 1) - 1]  # +1 -1?

        for m in range(1, i + 1):
            z1 = self.DIRCE[m][1] * self.DIRCG[m][1] * self.ESLIDE[1]
            z2 = self.DIRCE[m][2] * self.DIRCG[m][2] * self.ESLIDE[2]

            z3 = self.DIRCE[m][3] * self.DIRCG[m][3] * self.ESLIDE[6]
            z4 = (self.DIRCE[m][2] * self.DIRCG[m][3] +
                  self.DIRCG[m][2] * self.DIRCE[m][3]) * self.ESLIDE[4]
            z5 = (self.DIRCE[m][3] * self.DIRCG[m][1] +
                  self.DIRCG[m][3] * self.DIRCE[m][1]) * self.ESLIDE[5]
            z6 = (self.DIRCE[m][1] * self.DIRCG[m][2] +
                  self.DIRCG[m][1] * self.DIRCE[m][2]) * self.ESLIDE[3]
            self.EXPECT[m] = z1 + z2 + z3 + z4 + z5 + z6

            self.DEV[m] = self.TENSHR[m] - self.EXPECT[m]

        if iDev == 1:
            self.output.append('')

            self.output.append('Sample: ' + str(sample))
            self.output.append(
                'Deviations of measured strains from calculated strains for thin section.')
            self.output.append(
                'GR\tTANS/2                  EXPVAL                   TANS/2-EV')

            numnegexp = 0.0

            for iterator in range(1, i + 1):
                s = ''

                s += str(self.TWINSET[iterator])
                s += '\t'
                s += num_to_str(self.TENSHR[iterator], 6, True)
                s += '                '
                s += num_to_str(self.EXPECT[iterator], 6, True)

                if self.EXPECT[iterator] > 0:
                    s += '                  '
                else:
                    s += '                 '

                s += num_to_str(self.DEV[iterator], 6, True)
                self.output.append(s)

            for k in range(1, i + 1):
                if self.EXPECT[k] < 0:
                    numnegexp += 1

            pctnegex = (numnegexp / i) * 100

            self.output.append(
                'Percent negative expected values is: ' + str(pctnegex) + '%')

    def minv(self, a: list, n, d, l: list, m: list):
        d = 1.0
        nk = -1 * n

        for k in range(1, n + 1):
            nk += n
            l[k] = k
            m[k] = k

            kk = nk + k

            bigA = float(a[kk])

            for j in range(k, n + 1):
                iz = n * (j - 1)

                for i in range(k, n + 1):
                    ij = iz + i

                    if (ABS(bigA) - ABS(a[ij])) < 0:
                        bigA = a[ij]
                        l[k] = i
                        m[k] = j

            # Because of later calculations, it is necessitated that l[] must be of type int.
            J = l[k]

            if (J - k) > 0:
                ki = k - n

                for i in range(1, n + 1):
                    ki = ki + n
                    hold = (-1 * a[ki])
                    ji = ki - k + J
                    a[ki] = a[ji]
                    a[ji] = hold

            # Because of later calculations, it is necessitated that m[] must be of type int.
            I = m[k]

            if (I - k) > 0:
                jp = n * (I - 1)

                for j in range(1, n + 1):
                    jk = nk + j
                    ji = jp + j
                    hold = (-1 * a[jk])
                    a[jk] = a[ji]
                    a[ji] = hold

            if bigA == 0:
                d = 0.0
                return [a, n, d, l, m]

            for i in range(1, n + 1):
                if (i - k) != 0:
                    ik = nk + i
                    a[ik] = a[ik] / (-1 * bigA)

            for i in range(1, n + 1):
                ik = nk + i
                hold = a[ik]
                ij = i - n

                for j in range(1, n + 1):
                    ij = ij + n

                    if (i - k) != 0:
                        if (j - k) != 0:
                            kj = ij - i + k
                            a[ij] = hold * a[kj] + a[ij]

            KJ = k - n  # KJ in orig program

            for j in range(1, n + 1):
                KJ += n

                if (j - k) != 0:
                    a[KJ] = a[KJ] / bigA

            d = d * bigA
            a[kk] = 1 / bigA

        K = n  # K in orig program

        while True:  # DO
            K -= 1

            if K <= 0:
                break  # exit do

            I = l[K]  # I in orig program

            if (I - K) > 0:
                jq = n * (K - 1)
                jr = n * (I - 1)

                for j in range(1, n + 1):
                    jk = jq + j
                    hold = a[jk]
                    ji = jr + j
                    a[jk] = (-1 * a[ji])
                    a[ji] = hold

            J = m[K]  # J in orig program

            if (J - K) > 0:
                ki = K - n

                for i in range(1, n + 1):
                    ki = ki + n
                    hold = a[ki]
                    ji = ki - K + J
                    a[ki] = (-1 * a[ji])
                    a[ji] = hold

        return [a, n, d, l, m]

    def import_analysis(self, path: str):
        file = open(path, 'r')

        line = ''
        sample = ''
        num = 0
        curPos = 1

        read = file.readline().strip().split(',')  # read 1
        num = int(read[0])
        sample = read[1]

        read = file.readline().strip().split(',')  # read 2
        self.store_SLISTR[1] = float(read[0])
        self.store_SLISTR[3] = float(read[1])
        self.store_SLISTR[6] = float(read[2])

        read = file.readline().strip().split(',')  # read 3
        self.store_BEAR[1] = float(read[0])
        self.store_PLUNGE[1] = float(read[1])

        read = file.readline().strip().split(',')  # read 4
        self.store_BEAR[2] = float(read[0])
        self.store_PLUNGE[2] = float(read[1])

        read = file.readline().strip().split(',')  # read 5
        self.store_BEAR[3] = float(read[0])
        self.store_PLUNGE[3] = float(read[1])

        line = file.readline()

        while not (line == None or line == '' or line == '\n'):
            read = line.strip().split(',')
            self.store_BCOMP[curPos] = float(read[0])
            self.store_PCOMP[curPos] = float(read[1])
            self.store_BTENS[curPos] = float(read[2])
            self.store_PTENS[curPos] = float(read[3])
            self.store_BEARE[curPos] = float(read[4])
            self.store_PLUNE[curPos] = float(read[5])
            self.store_BEARC[curPos] = float(read[6])
            self.store_PLUNC[curPos] = float(read[7])
            self.store_BEARG[curPos] = float(read[8])
            self.store_PLUNG[curPos] = float(read[9])
            self.store_AVWIDTH[curPos] = float(read[10])
            self.store_SINDEX[curPos] = float(read[11])
            self.store_EXPECT[curPos] = float(read[12])
            curPos += 1
            line = file.readline()

        self.store_NUMDAT[0] = num

    def save_analysis(self, file):

        num = self.NUMDAT[(self.file_num + 1)]

        lines = [''] * 156
        lines[0] = str(num) + "," + "SavedAnalysis"
        lines[1] = str(self.SLISTR[1]) + "," + \
            str(self.SLISTR[3]) + "," + str(self.SLISTR[6])
        lines[2] = str(self.BEAR[1]) + "," + str(self.PLUNGE[1])
        lines[3] = str(self.BEAR[2]) + "," + str(self.PLUNGE[2])
        lines[4] = str(self.BEAR[3]) + "," + str(self.PLUNGE[3])

        for i in range(1, self.NUMDAT[(self.file_num + 1)] + 1):
            s = str(self.BCOMP[i]) + "," + str(self.PCOMP[i]) + "," + str(self.BTENS[i]) + "," + str(self.PTENS[i]) + "," + str(self.BEARE[i]) + "," + str(self.PLUNE[i]) + "," + str(
                self.BEARC[i]) + "," + str(self.PLUNC[i]) + "," + str(self.BEARG[i]) + "," + str(self.PLUNG[i]) + "," + str(self.AVWIDTH[i]) + "," + str(self.SINDEX[i]) + "," + str(self.EXPECT[i])

            # +5 to move past the initial lines, -1 for 0 indexing.
            lines[(i + 5 - 1)] = s

        for line in lines:
            file.write('%s\n' % line)

        file.close()

    def save_analysis_as_image(self, file):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = temp_dir + '\\temp.svg'
            self.curDrawing.filename = temp_file_path
            self.curDrawing.save()
            drawing = svg2rlg(temp_file_path)
            extension = file.name.split('.')[-1]
            if extension == 'gif':
                renderPM.drawToFile(drawing, file.name, fmt='GIF')
            elif extension == 'jpg':
                renderPM.drawToFile(drawing, file.name, fmt='JPG')
            elif extension == 'bmp':
                renderPM.drawToFile(drawing, file.name, fmt='BMP')

    def snet_menu(self, n, sample, bcomp: list, pcomp: list, btens: list, ptens: list, beare: list, plune: list, bearc: list, plunc: list, bearg: list, plung: list, saveSVG, plotPicture, snet_plot_type, is_snet_rotate, rot1, tilt, rot2, back_color, grid_color, point_color, icon_color):
        flg2 = 0
        num = 0
        if n <= 3:
            num = self.NUMDAT[(n + 1) - 1]
        elif n > 3:
            num = n

        if snet_plot_type == 'compression':
            if is_snet_rotate:
                ref_results = self.snet_rotate(
                    "Placeholder", self.BEAR, self.PLUNGE, num, sample, bcomp, pcomp, flg2, saveSVG, plotPicture, rot1, tilt, rot2, back_color, grid_color, point_color, icon_color)
                self.BEAR = ref_results[0]
                self.PLUNGE = ref_results[1]
                bcomp = ref_results[2]
                pcomp = ref_results[3]
            else:
                self.stereonet("Placeholder", self.BEAR, self.PLUNGE,
                               num, sample, bcomp, pcomp, flg2, saveSVG, plotPicture, back_color, grid_color, point_color, icon_color)
        elif snet_plot_type == 'tension':
            if is_snet_rotate:
                ref_results = self.snet_rotate(
                    "Placeholder", self.BEAR, self.PLUNGE, num, sample, btens, ptens, flg2, saveSVG, plotPicture, rot1, tilt, rot2, back_color, grid_color, point_color, icon_color)
                self.BEAR = ref_results[0]
                self.PLUNGE = ref_results[1]
                btens = ref_results[2]
                ptens = ref_results[3]
            else:
                self.stereonet("Placeholder", self.BEAR, self.PLUNGE,
                               num, sample, btens, ptens, flg2, saveSVG, plotPicture, back_color, grid_color, point_color, icon_color)
        elif snet_plot_type == 'e twin poles':
            if is_snet_rotate:
                ref_results = self.snet_rotate(
                    "Placeholder", self.BEAR, self.PLUNGE, num, sample, beare, plune, flg2, saveSVG, plotPicture, rot1, tilt, rot2, back_color, grid_color, point_color, icon_color)
                self.BEAR = ref_results[0]
                self.PLUNGE = ref_results[1]
                beare = ref_results[2]
                plune = ref_results[3]
            else:
                self.stereonet("Placeholder", self.BEAR, self.PLUNGE,
                               num, sample, beare, plune, flg2, saveSVG, plotPicture, back_color, grid_color, point_color, icon_color)
        elif snet_plot_type == 'c axes':
            if is_snet_rotate:
                ref_results = self.snet_rotate(
                    "Placeholder", self.BEAR, self.PLUNGE, num, sample, bearc, plunc, flg2, saveSVG, plotPicture, rot1, tilt, rot2, back_color, grid_color, point_color, icon_color)
                self.BEAR = ref_results[0]
                self.PLUNGE = ref_results[1]
                bearc = ref_results[2]
                plunc = ref_results[3]
            else:
                self.stereonet("Placeholder", self.BEAR, self.PLUNGE,
                               num, sample, bearc, plunc, flg2, saveSVG, plotPicture, back_color, grid_color, point_color, icon_color)
        elif snet_plot_type == 'g poles':
            if is_snet_rotate:
                ref_results = self.snet_rotate(
                    "Placeholder", self.BEAR, self.PLUNGE, num, sample, bearg, plung, flg2, saveSVG, plotPicture, rot1, tilt, rot2, back_color, grid_color, point_color, icon_color)
                self.BEAR = ref_results[0]
                self.PLUNGE = ref_results[1]
                bearg = ref_results[2]
                plung = ref_results[3]
            else:
                self.stereonet("Placeholder", self.BEAR, self.PLUNGE,
                               num, sample, bearg, plung, flg2, saveSVG, plotPicture, back_color, grid_color, point_color, icon_color)

        return [bcomp, pcomp, btens, ptens, beare, plune, bearc, plunc, bearg, plung]

    def plot_saved_analysis(self, saveSVG, plotImage, snet_plot_type, is_snet_rotate, rot1, tilt, rot2, back_color, grid_color, point_color, icon_color):
        self.SLISTR = self.store_SLISTR
        self.BEAR = self.store_BEAR
        self.PLUNGE = self.store_PLUNGE
        self.BCOMP = self.store_BCOMP
        self.PCOMP = self.store_PCOMP
        self.BTENS = self.store_BTENS
        self.PTENS = self.store_PTENS
        self.SINDEX = self.store_SINDEX
        self.AVWIDTH = self.store_AVWIDTH
        self.EXPECT = self.store_EXPECT
        self.BEARC = self.store_BEARC
        self.PLUNC = self.store_PLUNC
        self.BEARE = self.store_BEARE
        self.PLUNE = self.store_PLUNE
        self.BEARG = self.store_BEARG
        self.PLUNG = self.store_PLUNG
        self.NUMDAT = self.store_NUMDAT

        ref_results = self.snet_menu(self.NUMDAT[0], '', self.BCOMP, self.PCOMP, self.BTENS, self.PTENS,
                                     self.BEARE, self.PLUNE, self.BEARC, self.PLUNC, self.BEARG, self.PLUNG, saveSVG, plotImage, snet_plot_type, is_snet_rotate, rot1, tilt, rot2, back_color, grid_color, point_color, icon_color)
        self.BCOMP = ref_results[0]
        self.PCOMP = ref_results[1]
        self.BTENS = ref_results[2]
        self.PTENS = ref_results[3]
        self.BEARE = ref_results[4]
        self.PLUNE = ref_results[5]
        self.BEARC = ref_results[6]
        self.PLUNC = ref_results[7]
        self.BEARG = ref_results[8]
        self.PLUNG = ref_results[9]

    def snet_rotate(self, z, bear: list, plunge: list, num, sample, az: list, pl: list, flg2, saveSVG, plotPicture, rot1, tilt, rot2, back_color, grid_color, point_color, icon_color):
        u = [0.0] * 151
        v = [0.0] * 151
        w = [0.0] * 151
        xx = [0.0] * 151
        yy = [0.0] * 151
        zz = [0.0] * 151
        azn = [0.0] * 151
        pln = [0.0] * 151

        pi = 3.1415926
        dr = pi / 180

        flg2 = 0

        phi = rot1 * dr
        theta = tilt * dr
        psi = rot2 * dr

        for i in range(1, num + 1):
            azn[i] = az[i] * dr
            pln[i] = pl[i] * dr

            u[i] = COS(azn[i]) * COS(pln[i])
            v[i] = SIN(azn[i]) * COS(pln[i])
            w[i] = SIN(pln[i])

            # XX(I) = (U(I) * (COS(PSI) * COS(THETA) * COS(PHI) - SIN(PSI) * SIN(PHI))) + (V(I) * (COS(PSI) * COS(THETA) * SIN(PHI) + SIN(PSI) * COS(PHI)) - (W(I) * COS(PSI) * SIN(THETA)))
            xx[i] = (u[i] * (COS(psi) * COS(theta) * COS(phi) - SIN(psi) * SIN(phi))) + (v[i] *
                                                                                         (COS(psi) * COS(theta) * SIN(phi) + SIN(psi) * COS(phi)) - (w[i] * COS(psi) * SIN(theta)))
            # YY(I) = -(U(I) * (SIN(PSI) * COS(THETA) * COS(PHI) + COS(PSI) * SIN(PHI))) - (V(I) * (SIN(PSI) * COS(THETA) * SIN(PHI) - COS(PSI) * COS(PHI))) + (W(I) * SIN(PSI) * SIN(THETA))
            yy[i] = -1 * (u[i] * (SIN(psi) * COS(theta) * COS(phi) + COS(psi) * SIN(phi))) - (v[i] * (
                SIN(psi) * COS(theta) * SIN(phi) - COS(psi) * COS(phi))) + (w[i] * SIN(psi) * SIN(theta))
            # ZZ(I) = (U(I) * SIN(THETA) * COS(PHI)) + (V(I) * SIN(THETA) * SIN(PHI)) + (W(I) * COS(THETA))
            zz[i] = (u[i] * SIN(theta) * COS(phi)) + \
                (v[i] * SIN(theta) * SIN(phi)) + (w[i] * COS(theta))

            u[i] = xx[i]
            v[i] = yy[i]
            w[i] = zz[i]

            if w[i] < 0:
                w[i] = -1 * w[i]
                v[i] = -1 * v[i]
                u[i] = -1 * u[i]
            elif w[i] == 0:
                w[i] = 0.00001

            # end select

            if u[i] >= 0 and v[i] >= 0:
                v[i] = -1 * v[i]
            elif u[i] >= 0 and v[i] < 0:
                v[i] = -1 * v[i]

            pln[i] = FNASIN(w[i])
            azn[i] = FNACOS(ABS(u[i]) / COS(pln[i]))

            pln[i] = pln[i] * 57.2957795
            azn[i] = azn[i] * 57.2957795

            if u[i] >= 0 and v[i] >= 0:
                azn[i] = 0 - azn[i]
            elif u[i] < 0 and v[i] >= 0:
                azn[i] = 180 - azn[i]
            elif u[i] >= 0 and v[i] < 0:
                azn[i] = 0 + azn[i]
            elif u[i] < 0 and v[i] < 0:
                azn[i] = 180 + azn[i]

            if (azn[i] > 360):
                azn[i] = azn[i] - 360

        for i in range(1, 4):
            self.B[i] = bear[i] * dr
            self.P[i] = plunge[i] * dr

            u[i] = COS(self.B[i]) * COS(self.P[i])
            v[i] = SIN(self.B[i]) * COS(self.P[i])
            w[i] = SIN(self.P[i])

            # XX(I) = (U(I) * (COS(PSI) * COS(THETA) * COS(PHI) - SIN(PSI) * SIN(PHI))) + (V(I) * (COS(PSI) * COS(THETA) * SIN(PHI) + SIN(PSI) * COS(PHI)) - (W(I) * COS(PSI) * SIN(THETA)))
            xx[i] = (u[i] * (COS(psi) * COS(theta) * COS(phi) - SIN(psi) * SIN(phi))) + (v[i] *
                                                                                         (COS(psi) * COS(theta) * SIN(phi) + SIN(psi) * COS(phi)) - (w[i] * COS(psi) * SIN(theta)))
            # YY(I) = -(U(I) * (SIN(PSI) * COS(THETA) * COS(PHI) + COS(PSI) * SIN(PHI))) - (V(I) * (SIN(PSI) * COS(THETA) * SIN(PHI) - COS(PSI) * COS(PHI))) + (W(I) * SIN(PSI) * SIN(THETA))
            yy[i] = -1 * (u[i] * (SIN(psi) * COS(theta) * COS(phi) + COS(psi) * SIN(phi))) - (v[i] * (
                SIN(psi) * COS(theta) * SIN(phi) - COS(psi) * COS(phi))) + (w[i] * SIN(psi) * SIN(theta))
            # ZZ(I) = (U(I) * SIN(THETA) * COS(PHI)) + (V(I) * SIN(THETA) * SIN(PHI)) + (W(I) * COS(THETA))
            zz[i] = (u[i] * SIN(theta) * COS(phi)) + \
                (v[i] * SIN(theta) * SIN(phi)) + (w[i] * COS(theta))

            u[i] = xx[i]
            v[i] = yy[i]
            w[i] = zz[i]

            if w[i] < 0:
                w[i] = -1 * w[i]
                v[i] = -1 * v[i]
                u[i] = -1 * u[i]
            elif w[i] == 0:
                w[i] = 0.00001

            if u[i] >= 0 and v[i] >= 0:
                v[i] = -1 * v[i]
            elif u[i] >= 0 and v[i] < 0:
                v[i] = -1 * v[i]

            self.P[i] = FNASIN(w[i])
            self.B[i] = FNACOS(ABS(u[i]) / COS(self.P[i]))

            self.P[i] = self.P[i] * 57.2957795
            self.B[i] = self.B[i] * 57.2957795

            if u[i] >= 0 and v[i] >= 0:
                self.B[i] = 0 - self.B[i]
            elif u[i] < 0 and v[i] >= 0:
                self.B[i] = 180 - self.B[i]
            elif u[i] >= 0 and v[i] < 0:
                self.B[i] = 0 + self.B[i]
            elif u[i] < 0 and v[i] < 0:
                self.B[i] = 180 + self.B[i]

            if self.B[i] > 360:
                self.B[i] = self.B[i] - 360

            self.B[i] = self.B[i] / dr
            self.P[i] = self.P[i] / dr

        flg2 = 1

        self.stereonet(z, self.B, self.P, num, sample, azn,
                       pln, flg2, saveSVG, plotPicture, back_color, grid_color, point_color, icon_color)

        return [bear, plunge, az, pl]

    def stereonet(self, z, bear: list, plunge: list, num, sample, az: list, pl: list, flg2, saveSVG, plotPicture, back_color, grid_color, point_color, icon_color):

        drawing = svgwrite.Drawing(
            'svgwrite-example.svg',
            size=('2000px', '2000px')
        )
        # for the background color
        drawing.add(
            drawing.rect(
                insert=(0, 0),
                size=('100%', '100%'),
                rx=None,
                ry=None,
                fill=back_color
            )
        )

        # place grid circle
        drawing.add(
            drawing.circle(
                center=(convert_point(0), convert_point(0)),
                r=1000,
                stroke=grid_color,
                fill=back_color
            )
        )

        pi = 3.1415926
        dr = pi / 180

        xs = [0.0] * 151
        ys = [0.0] * 151

        for i in range(1, num + 1):
            p = pl[i] * dr
            a = az[i] * dr
            d = math.sin(pi / 4 - p / 2) * math.sqrt(2)

            x = d * math.sin(a)
            y = d * math.cos(a)

            drawing.add(
                drawing.circle(
                    center=(convert_point(x), (2000 - convert_point(y))),
                    r=8,
                    stroke=point_color,
                    fill=point_color
                )
            )

            xs[i] = x
            ys[i] = y

        drawing.add(
            drawing.path(
                d='M0 1000 L2000 1000 Z',
                stroke=grid_color,
                fill=grid_color
            )
        )
        drawing.add(
            drawing.path(
                d='M1000 0 L1000 2000 Z',
                stroke=grid_color,
                fill=grid_color
            )
        )

        if flg2 == 1:
            for j in range(1, 4):
                self.B[j] = bear[j] * dr * dr
                self.P[j] = plunge[j] * dr * dr
        else:
            for j in range(1, 4):
                self.B[j] = bear[j] * dr
                self.P[j] = plunge[j] * dr

        d2 = SIN(pi / 4 - self.P[1] / 2) * SQR(2)
        x2 = d2 * SIN(self.B[1])
        y2 = d2 * COS(self.B[1])
        # add circle
        drawing.add(
            drawing.circle(
                center=(convert_point(x2), 2000 - convert_point(y2)),
                r=50,
                stroke=icon_color,
                fill=icon_color
            )
        )
        d2 = SIN(pi / 4 - self.P[2] / 2) * SQR(2)
        # Shift to left and down to make the origin closer to the center.
        x2 = d2 * SIN(self.B[2]) - 0.05
        # Shift to left and down to make the origin closer to the center.
        y2 = d2 * COS(self.B[2]) - 0.05
        # add triangle (left, top, right)
        drawing.add(
            drawing.polygon(
                points=[
                    (convert_point(x2), 2000 - convert_point(y2)),
                    (convert_point(x2 + 0.05), 2000 - convert_point(y2 + 0.1)),
                    (convert_point(x2 + 0.1), 2000 - convert_point(y2))
                ],
                stroke=icon_color,
                fill=icon_color

            )
        )
        d2 = SIN(pi / 4 - self.P[3] / 2) * SQR(2)
        # Shift to left and down to make the origin closer to the center.
        x2 = d2 * SIN(self.B[3]) - 0.05
        # Shift to left and down to make the origin closer to the center.
        y2 = d2 * COS(self.B[3]) - 0.05
        # add triangle (left, top, right)
        drawing.add(
            drawing.rect(
                insert=(convert_point(x2), 2000 - convert_point(y2)),
                size=(75, 75),
                stroke=icon_color,
                fill=icon_color
            )
        )

        self.cur_drawing = drawing

        if saveSVG:
            try:
                default_file_name = "StereonetPlot-" + \
                    datetime.now().strftime('%m-%d-%Y-%H-%M') + ".svg"

                file = filedialog.asksaveasfile(
                    initialfile=default_file_name,
                    filetypes=(('Scalable Vector Graphic files', '*.svg'),),
                    title='Save',
                    mode='w'
                )

                if file != None:
                    file.write(drawing.tostring())
                    file.close()

            except Exception as e:
                messagebox.showerror(title='Error', message=e)
        elif plotPicture:
            SVG_file_desc, SVG_path = tempfile.mkstemp(suffix='.svg')
            PNG_file_desc, PNG_path = tempfile.mkstemp(suffix='.png')

            with os.fdopen(SVG_file_desc, 'w') as temp_svg_file:
                drawing.filename = SVG_path
                drawing.save()

                with os.fdopen(PNG_file_desc, 'w') as temp_png_file:
                    PNG_drawing = svg2rlg(SVG_path)
                    self.PNG_path = PNG_path
                    renderPM.drawToFile(PNG_drawing, PNG_path, fmt='PNG')

            os.remove(SVG_path)
