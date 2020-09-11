from skimage.metrics import (structural_similarity as ssim, peak_signal_noise_ratio as psnr)
from utilities.constants import (VIDEO_PATH, FRAMES_TO_TEST)
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

    def __init__(self, names: list):
        self.video_names = names
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

    # ssim helper function
    def calculate_ssim(self, original: list, test_against: list):
        ssim_array = []

        for index in range(FRAMES_TO_TEST):
            (score, diff) = ssim(original[index], test_against[index], full=True)
            ssim_array.append(score)

        return np.mean(ssim_array)

    # function that does the ssim computation and returns the results
    def get_ssim_results(self):
        ssim_array = [1.0]
        grayscale_original_video = self.create_colorspace_array(self.video_names[0], 'gray')

        for video in self.video_names[1:]:
            grayscale_video_to_test = self.create_colorspace_array(video, 'gray')
            ssim_score = self.calculate_ssim(grayscale_original_video, grayscale_video_to_test)
            ssim_array.append(ssim_score)

        return ssim_array

    # psnr helper function
    def calculate_psnr(self, original: list, test_against: list):
        psnr_array = []

        for index in range(FRAMES_TO_TEST):
            score = psnr(original[index], test_against[index])

            # to avoid np.inf as a result
            # since we'll always devide by 0 if two images are visually the same
            if math.isinf(score):
                score = 100.0

            psnr_array.append(score)

        return np.mean(psnr_array)

    # function that does the psnr computation and returns the results
    def get_psnr_results(self):
        psnr_array = [100.0]
        ycbcr_original_video = self.create_colorspace_array(self.video_names[0], 'ycbcr')

        for video in self.video_names[1:]:
            ycbcr_video_to_test = self.create_colorspace_array(video, 'ycbcr')
            psnr_score = self.calculate_psnr(ycbcr_original_video, ycbcr_video_to_test)
            psnr_array.append(psnr_score)

        return psnr_array
