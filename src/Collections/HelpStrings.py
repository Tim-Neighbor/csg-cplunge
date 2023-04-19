from enum import Enum


class Tag(Enum):
    TITLE = 'title'
    BODY = 'body'
    BOLD = 'bold'
    BULLETED_LIST_1 = 'bulleted_list_1'
    BULLETED_LIST_2 = 'bulleted_list_2'
    NUMBERED_LIST = 'numbered_list'


def get_content_cplunge():

    list_of_tuples = [
        ('The Cplunge tab is used for calculating the plunge and direction of the optical axis for an individual calcite grain.\n\n', Tag.BODY.value),
        ('From the Cplunge tab, you can:\n', Tag.BODY.value),
        ('\u2022\tAdd the data for a new calcite grain.\n', Tag.BULLETED_LIST_1.value),
        ('\u2022\tClear all currently stored data.\n', Tag.BULLETED_LIST_1.value),
        ('\u2022\tSave all currently stored data.\n', Tag.BULLETED_LIST_1.value),
        ('\u2022\tThe data can be stored in a CSV file or a DAT file.\n\n',
         Tag.BULLETED_LIST_2.value),
        ('Adding a grain\'s data\n', Tag.TITLE.value),
        ('When adding data for a new calcite grain, you must enter the following 4 measurements from the microscope stage:\n', Tag.BODY.value),
        ('1.\tThe trend of the optical axis,\n', Tag.BULLETED_LIST_1.value),
        ('2.\tThe trend of the twin pole,\n', Tag.BULLETED_LIST_1.value),
        ('3.\tThe plunge of the twin pole, and\n', Tag.BULLETED_LIST_1.value),
        ('4.\tThe direction that the microscope stage is sloping towards (+ for North, - for South).\n\n',
         Tag.BULLETED_LIST_1.value),
        ('After the measurements have been added, you can then calculate the 2 possible pairs of values for the optical axis plunge and direction. Only one of the two pairs is correct, and you must check both on your microscope stage in order to determine which is the correct pair. After selecting the correct option, you can then add all of the data to the running list by clicking OK.\n\nNote that the direction values will change from signs and arrows (+, >, -, <) to numbers (1, 2, 3, 4) when added to your list. This is intended, as it allows for more seamless compatibility with the strain analysis portion of this program.\n\n', Tag.BODY.value),
        ('A Note on "dA"\n', Tag.TITLE.value),
        ('The original Cplunge program contained an option to calculate dA, which was described as the angle between the C-axis (optical axis) and the E-pole (twin pole). This dA value is also calculated alongside the values for the optical axis and is adding to the running list when you click OK.\n\n', Tag.BODY.value),
        ('Saving Data\n', Tag.TITLE.value),
        ('At any point, you may save your data to either a CSV file or a DAT file. Both options will produce a file that is consistent with what is described in the "File Types -> .dat Files" section of the help tab (with 0\'s serving as placeholders for the unknown values). Choosing either CSV or DAT will result in the same file, with the only difference being the file extension. Both file types can be read in via the "Twinsets" tab for further analysis.\n\n', Tag.BODY.value)
    ]

    return list_of_tuples


def get_content_twinsets():

    list_of_tuples = [
        ('The Twinsets tab is used for loading or creating the collections of twinsets that represent calcite strains for further analysis.\n\n', Tag.BODY.value),
        ('Data Set Tabs\n', Tag.TITLE.value),
        ('Each of the three Data Set tabs stores a collection of up to fifty data sets along with a rotation to be applied to the entire collection during the analysis steps.\nFrom each of the tabs, you can...\n', Tag.BODY.value),
        ('\u2022\tLoad Sets from a preformatted .dat file. (See File Types for instructions on creating this file)\n',
         Tag.BULLETED_LIST_1.value),
        ('\u2022\tModify individual sets in the collection.\n',
         Tag.BULLETED_LIST_1.value),
        ('\u2022\tThis includes deleting individual sets.\n', Tag.BULLETED_LIST_2.value),
        ('\u2022\tManually Add sets to the data set.\n', Tag.BULLETED_LIST_1.value),
        ('\u2022\tClear the data set, removing it from the analysis entirely.\n',
         Tag.BULLETED_LIST_1.value),
        ('\u2022\tEnable and set a Rotation for the data set using cosines to reference axes to be used during analysis.\n',
         Tag.BULLETED_LIST_1.value),
        ('\u2022\tThese rotations must be calculated outside of this program, and should be based off of the orientation of the data at collection.\n', Tag.BULLETED_LIST_2.value),
        ('\n\n', Tag.BODY.value),
        ('Data Cleanup Tab\n', Tag.TITLE.value),
        ('The individual strains in each of the collections may be removed based on their deviation from their expected values. Negative deviations are highlighted in red.\nFrom this tab, you can...\n', Tag.BODY.value),
        ('\u2022\tSelect all twinsets with Positive Deviations from all of the sets.\n',
         Tag.BULLETED_LIST_1.value),
        ('\u2022\tSelect all twinsets with Negative Deviations from all of the sets.\n',
         Tag.BULLETED_LIST_1.value),
        ('\u2022\tSelect the twinsets with the 20% Greatest Deviations from all of the sets, based on absolute values.\n',
         Tag.BULLETED_LIST_1.value),
        ('\u2022\tManually select twinsets.\n', Tag.BULLETED_LIST_1.value),
        ('Pressing the Delete Selected button will remove the selected twinsets from their respective collections, and automatically display the newly calculated deviations for the remaining sets.\n', Tag.BODY.value),
    ]

    return list_of_tuples


def get_content_report():
    list_of_tuples = [
        ('The Report tab is used for generating reports based off of the analysis of the twinset collections.\n\n', Tag.BODY.value),
        ('The report can be generated as either a Full Report, which includes the Twinset collections data, the Axis data for the twinsets, the Strain data, the Statistical data, and the Deviations; a report containing only the Strain, Statistical, and Deviation data; or only the Strain and Statistical data.\n\n', Tag.BODY.value),
        ('The report can also be saved as a rich text file (.rtf) for further for formatting or documentation.\n\n', Tag.BODY.value),
        ('Full Report\n', Tag.TITLE.value),
        ('Produces a lengthy output of 5 to 14 pages depending on the number of data sets used for the sample. It includes all of the original input data for each data set, calculated c-axes orientations, poles to e twin planes, g-axis orientations, and the angle between the c-axis and e twin plane. Also included are calculated orientations of the compression and tension axes for each twin set, and the twin intensity and average twin width for each twin set. A separate page includes all of the strain data and statistical data. Calculated deviations are the final part of the output along with the percent negative expected values.\n\n', Tag.BODY.value),
        ('Strains, Stats, and Deviations\n', Tag.TITLE.value),
        ('Produces a much shorter output of the most necessary information: the strain data and statistical data along with the calculated deviations and percent negative expected values.\n\n', Tag.BODY.value),
        ('Strains and Stats\n', Tag.TITLE.value),
        ('Produces a single page output of the strain data and statistical data.\n\n', Tag.BODY.value)
    ]

    return list_of_tuples


def get_content_stereonet():
    list_of_tuples = [
        ('The Stereonet Plot tab is used for displaying the contents of the twinset collections as a 2D stereonet.\n\nThe plotted stereonet may be saved as either an image file (.jpeg, .bmp, or .gif) or as a vector based .svg file that can be edited and scaled with more advanced image editing software.\n\n', Tag.BODY.value),
        ('Plot Type\n', Tag.TITLE.value),
        ('You may choose which data from the twinset collections you want plotted on the screen, only one of the choices may be plotted at any given time.\n\n', Tag.BODY.value),
        ('Rotation\n', Tag.TITLE.value),
        ('\u2022\tFirst: A horizontal rotation around the center of the stereonet.\n',
         Tag.BULLETED_LIST_1.value),
        ('\u2022\tTilt: A vertical rotation around the East-West axis of the stereonet done after the first rotation.\n',
         Tag.BULLETED_LIST_1.value),
        ('\u2022\tSecond: An additional horizontal rotation around the center of the stereonet done after the tilt.\n\n',
         Tag.BULLETED_LIST_1.value),
        ('Saved Analysis\n', Tag.TITLE.value),
        ('You may also Iimport and display the stereonet of a previously saved analysis, or export the current analyzed twinsets for plotting the stereonets at a later date.\nSaved analyses are stored as .all files, which should not be edited as they may put the data into an incosistent or unstable state.\n\n', Tag.BODY.value)
    ]

    return list_of_tuples


def get_content_fudge():

    list_of_tuples = [
        ('The Fudge Factor tab is used for setting parameters of the thickness of the twinsets used in the analysis.\n\n', Tag.BODY.value),
        ('Thickness Type\n', Tag.TITLE.value),
        ('You may choose between the Outer, Inner, and Average thickness of the twinsets as the one to be used for the current analysis. Inner Thickness is the default setting, and the most commonly used.\n\n', Tag.BODY.value),
        ('Ratio\n', Tag.TITLE.value),
        ('A specific ratio for the actual twin/microtwin thickness may be provided for the analysis.  0.5 is the most commonly used ratio. However, using a 0.5 ratio will change thin twin thicknesses by -50% due to an error in the program. Using a ratio of 1.0 (the default setting in this program) corrects this known error.\n\n', Tag.BODY.value)
    ]

    return list_of_tuples


def get_content_file_types():

    list_of_tuples = [
        ('This program reads output from two different file formats that are comma delimited text files using custom extensions.\n\n', Tag.BODY.value),
        ('.dat Files\n', Tag.TITLE.value),
        ('The .dat file type is used for storing collections of twinsets in a standard format.\nEach line in the file represents a single twinset, the segments of the represent in order…\n', Tag.BODY.value),
        ('1.\tTWINSET: Twin measurement number\n', Tag.BULLETED_LIST_1.value),
        ('2.\tCVIV: c-axis bearing, universal stage A1 (0° to 360°)\n',
         Tag.BULLETED_LIST_1.value),
        ('3.\tCVP: c-axis plunge, universal stage NS (A2) (0° to approximately 35°)\n',
         Tag.BULLETED_LIST_1.value),
        ('4.\tKODEC: c-axis plunge direction (of stage) where 2 = east and 4 = west\n',
         Tag.BULLETED_LIST_1.value),
        ('5.\tTWINIV: Twin pole bearing, universal stage A1 (0° to 360°)\n',
         Tag.BULLETED_LIST_1.value),
        ('6.\tTWINP: Twin pole plunge, universal stage EW (A4) (0° to approximately 35°)\n',
         Tag.BULLETED_LIST_1.value),
        ('7.\tKODEE: Twin pole plunge direction (of stage) where 1 = north and 3 = south\n',
         Tag.BULLETED_LIST_1.value),
        ('8.\tTOTALM: Number of thin twins\n', Tag.BULLETED_LIST_1.value),
        ('9.\tTHICKM: Average thickness of thin twins in microns\n',
         Tag.BULLETED_LIST_1.value),
        ('10.\tTOTALT: Total number of thick twins\n', Tag.BULLETED_LIST_1.value),
        ('11.\tTHICKI: Average inner thickness of thick twins in microns\n',
         Tag.BULLETED_LIST_1.value),
        ('12.\tTHICKO: Average outer thickness of thick twins in microns\n',
         Tag.BULLETED_LIST_1.value),
        ('13.\tWIDTHN: Grain width (in microns) perpendicular to the twins\n',
         Tag.BULLETED_LIST_1.value),
        ('The file is terminated by a sentinel line beginning with 999, and there should be no more than 50 sets prior to this line.\n\n', Tag.BODY.value),
        ('.all Files\n', Tag.TITLE.value),
        ('The .all file type is used for storing a completed analysis to be re-used to generate stereonets.\nThe file should not be modified, as doing so may put the data and the program into an inconsistent or unstable state.\n\n', Tag.BODY.value)
    ]

    return list_of_tuples


def get_content_about():

    list_of_tuples = [
        ('CPLUNGE + CSG\nVersion: 1.0\n\nCreated by Tim Neighbor (timneighbor@gmail.com) as a practicum under the supervision of George Thomas and Timothy Paulsen (CS 490), Spring 2022 at the University of Wisconsin Oshkosh.\n\nBased off of the Strain Analysis User Interface program by Thomas Petersen and the command line program CPLUNGE by Barry McBride.\n\nBelow is the "About" section of the help tab from Thomas Petersen\'s Strain Analysis User Interface Program.\n\n---------------------------------------------------------------------------------------------------------------------------------------------------\n\n', Tag.BODY.value),
        ('Strain Analysis User Interface\nVersion: 1.0\n\nCreated by Thomas Petersen (thomasrpetersen@gmail.com) as a practicum under the supervision of George Thomas and Timothy Paulsen (CS 390), Summer 2015 at the University of Wisconsin Oshkosh\n\nBased on a Graphical User Interface created by Thomas Petersen, Steven Beshensky, and Alexander Karius as part of Software Engineering II (CS 342), Spring 2015 at the University of Wisconsin Oshkosh.\n\nBased off of the CSG22 command line interface by Mark A. Evans.', Tag.BODY.value)
    ]

    return list_of_tuples
