from skimage.metrics import (structural_similarity as ssim, peak_signal_noise_ratio as psnr)
from utilities.constants import (VIDEO_PATH, FRAMES_TO_TEST)
from concurrent.futures import (ThreadPoolExecutor, as_completed)
import os
import numpy as np
import math
import cv2


"""
A class responsible for conducting a frame analysis on video files
    - ssim
    - psnr
"""


class FrameAnalysis:
    video_names = []  # list containing video names
    workers = 1       # number of cpu cores

    # results
    ssim_results = []
    psnr_results = []

    def __init__(self, names: list):
        self.video_names = names
        self.workers = os.cpu_count()
        np.seterr(divide='ignore')  # ignore numpy's division by 0 warning

    def create_colorspace_array(self, vid_name: str, color_space):
        cv_color_space = None
        grayscale_array = []
        vidcap = cv2.VideoCapture(VIDEO_PATH + vid_name)

        if color_space == 'gray':
            cv_color_space = cv2.COLOR_BGR2GRAY
        elif color_space == 'ycbcr':
            cv_color_space = cv2.COLOR_BGR2YCR_CB
        else:
            raise Exception("unspecified color space: {}".format(color_space))

        # create an array full of grayscale space frames for the original video
        for frame_no in range(FRAMES_TO_TEST):
            (res, frame) = vidcap.read()

            if not res:
                raise Exception("retrieving the frame: {}".format(vid_name))

            grayscale_frame = cv2.cvtColor(frame, cv_color_space)
            grayscale_array.append(grayscale_frame)

        return grayscale_array

    # runs the ssim test
    def run_ssim_test(self):
        ssim_array = [1.0]
        grayscale_original_video = self.create_colorspace_array(self.video_names[0], 'gray')

        for video in self.video_names[1:]:
            grayscale_video_to_test = self.create_colorspace_array(video, 'gray')
            ssim_score = self.calculate_ssim(grayscale_original_video, grayscale_video_to_test)
            ssim_array.append(ssim_score)

        return ssim_array

    # a helper function for the ssim test
    def calculate_ssim(self, original: list, test_against: list):
        ssim_array = []

        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            future_to_ssim = {
                executor.submit(ssim, original[i], test_against[i], full=True): i for i in range(FRAMES_TO_TEST)
            }

        for future in as_completed(future_to_ssim):
            (score, diff) = future.result()
            ssim_array.append(score)

        return np.mean(ssim_array)

    # runs the psnr test
    def run_psnr_test(self):
        psnr_array = [100.0]
        ycbcr_original_video = self.create_colorspace_array(self.video_names[0], 'ycbcr')

        for video in self.video_names[1:]:
            ycbcr_video_to_test = self.create_colorspace_array(video, 'ycbcr')
            psnr_score = self.calculate_psnr(ycbcr_original_video, ycbcr_video_to_test)
            psnr_array.append(psnr_score)

        return psnr_array

    # a helper function for the psnr test
    def calculate_psnr(self, original: list, test_against: list):
        psnr_array = []

        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            future_to_psnr = {
                executor.submit(psnr, original[i], test_against[i]): i for i in range(FRAMES_TO_TEST)
            }

        for future in as_completed(future_to_psnr):
            score = future.result()
            # to avoid np.inf as a result
            # since we'll always devide by 0 if two images are visually the same
            if math.isinf(score):
                score = 100.0

            psnr_array.append(score)

        return np.mean(psnr_array)

    # Driver function
    # Run this function to conduct the frame analysis tests
    def run_tests(self):
        if len(self.ssim_results) == 0:
            self.ssim_results = self.run_ssim_test()
        if len(self.psnr_results) == 0:
            self.psnr_results = self.run_psnr_test()
