import os

"""
A class responsible for conducting a size analysis on video files
"""


class SizeAnalysis:
    VIDEO_PATH = 'video_samples/'  # relative path containing video files
    video_names = []               # list containing video names

    def __init__(self, names: list):
        self.video_names = names

    def get_results(self):
        sizes_array = []
        for video in self.video_names:
            sizes_array.append(os.path.getsize(self.VIDEO_PATH + video) / 1000)
        return sizes_array
