from utilities.constants import VIDEO_PATH
import os

"""
A class responsible for conducting a size analysis on video files
"""


class SizeAnalysis:
    video_names = []  # list containing video names

    def __init__(self, names: list):
        self.video_names = names

    def get_results(self):
        sizes_array = []
        for video in self.video_names:
            sizes_array.append(os.path.getsize(VIDEO_PATH + video) / 1000)
        return sizes_array
