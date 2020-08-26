from skimage.metrics import structural_similarity as ssim
from utilities.constants import (VIDEO_PATH, FRAMES_TO_TEST)
import numpy as np
import cv2

"""
A class responsible for conducting a frame analysis on video files
    - ssim
"""


class FrameAnalysis:
    video_names = []  # list containing video names

    def __init__(self, names: list):
        self.video_names = names

    def create_grayscale_array(self, vid_name: str):
        grayscale_array = []
        vidcap = cv2.VideoCapture(VIDEO_PATH + vid_name)

        # create an array full of grayscale space frames for the original video
        for frame_no in range(FRAMES_TO_TEST):
            (res, frame) = vidcap.read()

            if not res:
                raise Exception("retrieving the frame: {}".format(vid_name))

            grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            grayscale_array.append(grayscale_frame)

        return grayscale_array

    def calculate_ssim(self, original: list, test_against: list):
        ssim_array = []

        for index in range(FRAMES_TO_TEST):
            (score, diff) = ssim(original[index], test_against[index], full=True)
            ssim_array.append(score)

        return np.mean(ssim_array)

    def get_ssim_results(self):
        ssim_array = [1.0]
        grayscale_original_video = self.create_grayscale_array(self.video_names[0])

        for video in self.video_names[1:]:
            grayscale_video_to_test = self.create_grayscale_array(video)
            ssim_score = self.calculate_ssim(grayscale_original_video, grayscale_video_to_test)
            ssim_array.append(ssim_score)

        return ssim_array
