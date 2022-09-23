import os
from os.path import dirname as up

from parsoda.model import Visualizer


class PrintEmojiPolarization(Visualizer):

    def __init__(self, file_path):
        self.file = file_path

    def visualize(self, result):
        print(result)
        if self.file is not None:
            with open(self.file, 'w') as f:
                print(result, file=f)


