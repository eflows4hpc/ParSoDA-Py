import functools
import os
from os.path import dirname as up

from parsoda.model import Visualizer


class SortGapBIDE(Visualizer[dict]):

    def __init__(self, file: str, key: str, mode: str = 'descending', min_length: int = 1):
        self.file = file
        self.key = key
        self.mode = mode
        self.min_length = min_length

    def visualize(self, result):
        filtered_result = []
        if self.min_length is not None and self.min_length > 1:
            for elem in result:
                if len(elem[0]) >= self.min_length:
                    filtered_result.append(elem)
        else:
            filtered_result = result
        if self.key=="support":
            if self.mode=="descending":
                sorted_result = sorted(filtered_result, key=functools.cmp_to_key(lambda x, y: (y[1] > x[1]) - (y[1] < x[1])))
            elif self.mode=="ascending":
                sorted_result = sorted(filtered_result, key=functools.cmp_to_key(lambda x, y: (y[1] < x[1]) - (y[1] > x[1])))
            else:
                raise Exception("Parametri visualizzazione errati!")
        elif self.key=="pois":
            if self.mode=="descending":
                sorted_result = sorted(filtered_result, key=functools.cmp_to_key(SortGapBIDE.__compare_pois_inv))
            elif self.mode=="ascending":
                sorted_result = sorted(filtered_result, key=functools.cmp_to_key(SortGapBIDE.__compare_pois))
            else:
                raise Exception("Parametri visualizzazione errati!")
        else:
            raise Exception("Parametri visualizzazione errati!")

        print("\n")
        print("Sequential Pattern Mining:")
        print("[Trajectory]          [Support]")
        print()
        for element in sorted_result:
            print(element[:2])

        if self.file is not None:
            with open(self.file, 'w') as f:
                print("\n", file=f)
                print("Sequential Pattern Mining:", file=f)
                print("[Trajectory]          [Support]", file=f)
                print("\n", file=f)
                for item in sorted_result:
                    print(item[:2], file=f)

    @staticmethod
    def __compare_pois(tuple1, tuple2):
        list1 = tuple1[0]
        list2 = tuple2[0]
        l1 = len(list1)
        l2 = len(list2)
        for e1, e2 in zip(list1,list2):
            l1 = l1-1
            l2 = l2-1
            if str(e1)>str(e2):
                return 1
            elif str(e1)<str(e2):
                return -1
            elif l1==0:
                return 1
            elif l2==0:
                return -1


    @staticmethod
    def __compare_pois_inv(tuple1, tuple2):
        return -1*SortGapBIDE.__compare_pois(tuple1, tuple2)
