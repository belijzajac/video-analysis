import os

from analysis.frame import FrameAnalysis
from analysis.size import SizeAnalysis
from utilities.plot import Plotter
from utilities.constants import (VIDEO_PATH, VIDEO_TEST_AGAINST)
import traceback


def main():
    try:
        # try to get video names into a list
        # at index 0 stay the original video we'll be comparing against with
        video_names = os.listdir(VIDEO_PATH)
        old_index = video_names.index(VIDEO_TEST_AGAINST)
        video_names.insert(0, video_names.pop(old_index))

        # obtaining results
        # 1. frame
        frame_analysis = FrameAnalysis(video_names)
        video_ssim = frame_analysis.get_ssim_results()
        # 2. size
        size_analysis = SizeAnalysis(video_names)
        video_sizes = size_analysis.get_results()

        # plotting results
        plotter = Plotter(video_names)
        # 1. frame
        plotter.plot_ssim(video_ssim)
        # 2. size
        plotter.plot_sizes(video_sizes)

    except Exception as e:
        print("VideoAnalysis error:", e)
        traceback.print_exc()


if __name__ == '__main__':
    main()
