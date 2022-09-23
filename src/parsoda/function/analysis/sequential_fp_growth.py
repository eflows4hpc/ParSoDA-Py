# coding=utf-8
from pyfpgrowth import pyfpgrowth

from parsoda.model import Analyzer


class SequentialFPGrowth(Analyzer):

    def __init__(self, min_support: float, association_rules: dict, association_rules_min_confidence: float = 0.2):
        self.min_support = min_support
        self.association_rules = association_rules
        self.ass_rules_min_confidence = association_rules_min_confidence  # default

    def __call__(self, data):
        """
        l'input è un insieme di traiettorie, l'output è una tupla formata da (l'insieme di itemset con relativo
        supporto e le regole associative ottenute, nel caso il parametro association_rule sia diverso da 'yes'
        viene ritornata una tupla il cui secondo elemento è nullo
        """
        # prepare data
        prepared_data = []
        for a in data:
            d = a[1]  # type: dict
            prepared_data.extend(list(d.values()))

        # run the algorithm
        support = int(len(prepared_data) * self.min_support)
        patterns = pyfpgrowth.find_frequent_patterns(prepared_data, support)
        lenD = len(prepared_data)
        freq_itms = {}
        for poi in list(patterns.keys()):
            support_poi = float("{0:.4f}".format(patterns[poi] / float(lenD)))
            freq_itms[poi] = support_poi

        rules = None
        if self.association_rules == "yes":
            rules = pyfpgrowth.generate_association_rules(patterns, self.ass_rules_min_confidence)
        return freq_itms, rules
