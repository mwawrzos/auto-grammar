import xml.etree.ElementTree as eT

import matplotlib.pyplot as plt

from logic import Stats


class Main:
    def __init__(self):
        tree = eT.parse('../pl_bt5')
        root = tree.getroot()

        self.s = Stats()
        for book in root[1]:
            self.s.analyse_book(book)

    def fitting(self, name):
        token = self.s.tokens[name]
        fitting = dict()
        for (k, v) in self.s.tokens.items():
            common = token.successors.keys() & v.successors.keys()
            intersection = sum(map(min, zip([token.successors[x] for x in common],
                                            [v.successors[x] for x in common])))
            fitting[intersection / (len(token.meta) + len(v.meta))] = k
            # max(len(token.meta), len(v.meta))
        return fitting


def plot(x):
    plt.plot(x)

# m = Main()
