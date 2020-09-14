from utilities.constants import VIDEO_PATH
import os

"""
A class responsible for conducting a size analysis on video files
"""


class SizeAnalysis:
    video_names = []   # list containing video names
    size_results = []  # results

    def __init__(self, names: list):
        self.video_names = names

    # runs the size test
    def run_size_test(self):
        sizes_array = []
        for video in self.video_names:
            sizes_array.append(os.path.getsize(VIDEO_PATH + video) / 1000)
        return sizes_array

    # Driver function
    # Run this function to conduct the size analysis tests
    def run_tests(self):
        if len(self.size_results) == 0:
            self.size_results = self.run_size_test()
