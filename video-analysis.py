from analysis.frame import FrameAnalysis
from analysis.size import SizeAnalysis
from utilities.plot import Plotter
from utilities.constants import (VIDEO_PATH, VIDEO_TEST_AGAINST)
import os


def main():
    try:
        # try to get video names into a list
        # at index 0 will stay the original video we'll be comparing against with
        video_names = os.listdir(VIDEO_PATH)
        old_index = video_names.index(VIDEO_TEST_AGAINST)
        video_names.insert(0, video_names.pop(old_index))

        # remove file extentions (e.g. webm, mp4)
        video_labels = []
        for item in range(0, len(video_names)):
            video_labels.append(video_names[item].partition('.')[0])
        print("video_labels = ", video_labels[1:])

        # frame analysis tests
        frame_analysis = FrameAnalysis(video_names)
        frame_analysis.run_tests()
        video_ssim = frame_analysis.ssim_results
        print("video_ssim = ", video_ssim[1:])
        video_psnr = frame_analysis.psnr_results
        print("video_psnr = ", video_psnr[1:])

        # size analysis tests
        size_analysis = SizeAnalysis(video_names)
        size_analysis.run_tests()
        video_sizes = size_analysis.size_results
        print("video_size = ", video_sizes[1:])

        # plotting results
        plotter = Plotter(video_labels)
        # 1. frame
        plotter.plot_ssim(video_ssim)
        plotter.plot_psnr(video_psnr)
        # 2. size
        plotter.plot_sizes(video_sizes)

    except Exception as e:
        print("VideoAnalysis error:", e)


if __name__ == '__main__':
    main()
