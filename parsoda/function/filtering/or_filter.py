from typing import List
from parsoda.model import Filter


class OrFilter(Filter):

    def __init__(self, filter_functions: List[Filter]):
        self.filter_functions = filter_functions

    def test(self, item):
        for filter_func in self.filter_functions:
            if filter_func.test(item):
                return True
        return False

