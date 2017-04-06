import pickle
import xml.etree.ElementTree as eT
from math import floor
from math import log10
from multiprocessing.dummy import Pool

import matplotlib.pyplot as plt

from logic import Stats


def fitting_stats(token, v, t_successors, v_successors):
    common = t_successors.keys() & v_successors.keys()
    intersection = sum(map(min, zip([t_successors[x] for x in common],
                                    [v_successors[x] for x in common])))
    union = len(token.meta) + len(v.meta) - intersection
    return intersection, union


class Main:
    def __init__(self):
        self.counter = 0
        tree = eT.parse('pl_bt5')
        root = tree.getroot()

        self.s = Stats()
        for book in root[1]:
            self.s.analyse_book(book)

    def fitting(self, name):
        self.log_fitting(name)
        token = self.s.tokens[name]
        fitting = dict()
        for (k, v) in self.s.tokens.items():
            p_intersection, p_union = fitting_stats(token, v, token.predecessors, v.predecessors)
            s_intersection, s_union = fitting_stats(token, v, token.successors, v.successors)

            # cross-ratio to reduce asymmetric pre-post sets fitting deformation ('.' for next words)
            ps_fitting = p_intersection / s_union
            sp_fitting = s_intersection / p_union
            fitting_value = (ps_fitting + sp_fitting) / 2
            fitting[k] = (fitting_value, ps_fitting, sp_fitting, p_intersection, p_union, s_intersection, s_union)
            # fitting[fitting_value] = k
        return fitting

    def log_fitting(self, name):
        self.counter += 1
        all_tokens = len(self.s.tokens)
        print('[', repr(self.counter).rjust(floor(log10(all_tokens)) + 1), '/', repr(all_tokens),
              '] fitting: %s' % name)

    def all_fittings(self):
        self.counter = 0
        with Pool() as pool:
            return pool.map(lambda token: (token, self.fitting(token)), self.s.tokens)


def plot(x):
    plt.plot(x)


def serialize(var, filename):
    with open(filename, 'wb') as output:
        pickle.dump(var, output)


def deserialize(filename):
    with open(filename, 'rb') as input_file:
        return pickle.load(input_file)

m = Main()
