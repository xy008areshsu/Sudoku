# utility.py
# ------
# Licensing Information:
# Created by Ye Xu on 10/25/2014
# copyright (c) 2014 Ye Xu. All rights reserved

"""
In utility.py, There are a couple of helper functions implemented. These functions are independent from MVC parts of the
game, but are used by solver.py and gui.py
"""

import csv
import random


def load_csv(filename):
    """
    It loads a csv file, and converts into a grid format that the Sudoku solver will use
    :param filename
    :return: grid data format that the Sudoku solver will use
    """
    with open(filename, 'rt', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        str = []
        for row in reader:
            str.append(''.join(row[0].split(',')))

    return(''.join(str))


def write_csv(filename, values):
    """
    It writes to a csv file as an output, from the dictionary of values. The total number of values would be 81
    :param values:
    :return: a csv file
    """
    values_to_be_written = [item[1] for item in sorted(values.items())]
    assert(len(values_to_be_written) == 81)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for i in range(9):
            writer.writerow(values_to_be_written[0 : 9])
            values_to_be_written = values_to_be_written[9:]


def cross(A, B):
    """
    cross product of elements in A and in B. E.g. A = 'AB', B = '12', cross(A, B) = ['A1','A2', 'B1', 'B2']
    """
    return [a + b for a in A for b in B]


def from_file(filename, sep='\n'):
    """
    Parse a file into a list of strings, separated by sep.
    :param filename:
    :param sep:separator
    :return: list of strings representing files
    """
    return file(filename).read().strip().split(sep)

def shuffled(seq):
    """
    Return a randomly shuffled copy of the input sequence.
    :param seq:Original sequence
    :return:randomly shuffled copy of the input sequence
    """
    seq = list(seq)
    random.shuffle(seq)
    return seq


