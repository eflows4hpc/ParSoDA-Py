import pandas
from pycompss.dds import DDS
#from ddf_library.ddf import DDF
#from ddf_library.functions.ml.fpm import FPGrowth, AssociationRules

from parsoda_costantino.common.abstract_analysis_function import AbstractAnalysisFunction

class ParallelFPGrowth(AbstractAnalysisFunction):

    def __init__(self):
        AbstractAnalysisFunction.__init__(self)
        self.min_support = None
        self.association_rules = None
        self.ass_rules_min_confidence = 0.2 #default

    def set_options(self, options):
        if options is not None:
            self.min_support = float(options.get_option("min_support"))
            self.association_rules = options.get_option("association_rules")
            self.ass_rules_min_confidence = float(options.get_option("ass_rules_min_confidence"))

    def run(self, data):
        prepared_data = prepare_data(data)
        data_frame = pandas.DataFrame({"sequences": prepared_data})
        data_set = DDS().parallelize(data_frame)
        fp = FPGrowth('sequences', self.min_support)
        fp.run(data_set)
        result = fp.get_frequent_itemsets().toDF().values.tolist()
        lenD = len(prepared_data)
        freq_itms = []
        for poi in result:
            support_poi = float("{0:.4f}".format(poi[1]/float(lenD)))
            freq_itms.append((poi[0],support_poi))

        rules = None
        if self.association_rules == "yes":
            rules = AssociationRules(confidence=self.ass_rules_min_confidence).run(data_set)

        return freq_itms, rules



def prepare_data(data):
    new_data = []
    for a in data:
        d = a[1]  # type: dict
        new_data.extend(list(d.values()))
    prepared_data = []
    for a in new_data:
        result = []
        i = 1
        for e in a:
            if e not in result:
                result.append(e)
            i += 1
        prepared_data.append(result)
    return prepared_data
