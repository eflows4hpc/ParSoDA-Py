from abc import ABC
from datetime import date
from typing import Dict, List

from parsoda.model import Analyzer
from parsoda.utils.gap_bide import Gapbide
from parsoda.utils.roi import RoI


class GapBIDE(Analyzer[int, Dict[date, RoI], List]):
    def __init__(self, min_support: float, min_gap: int, max_gap: int):
        self.min_support = min_support
        self.min_gap = min_gap
        self.max_gap = max_gap

    def analyze(self, data):
        # prepare data
        prepared_data = []
        for a in data:
            d = data[a]  # type: dict
            prepared_data.extend(list(d.values()))

        supp = int(self.min_support * len(prepared_data))
        gb = Gapbide(prepared_data, supp, self.min_gap, self.max_gap)
        gb.run()
        trajectories = gb.result
        lenD = len(prepared_data)
        result = []
        for elem in trajectories:
            supp_trj = float("{0:.4f}".format(elem[1] / float(lenD)))
            if supp_trj >= self.min_support:
                result.append((elem[0], supp_trj))
        return result
