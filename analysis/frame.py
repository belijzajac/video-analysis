from skimage.metrics import structural_similarity as ssim
from utilities.constants import VIDEO_PATH
import cv2

"""
A class responsible for conducting a frame analysis on video files
    - ssim
"""


class FrameAnalysis:
    video_names = []  # list containing video names

    def __init__(self, names: list):
        self.video_names = names

    def get_frame(self, video_name: str):
        cap = cv2.VideoCapture(VIDEO_PATH + video_name)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        middle_frame = int(total_frames / 2)

        # take the middle frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame)
        (res_, frame_) = cap.read()

        if not res_:
            raise Exception("errors retrieving the frame: {}".format(video_name))
        else:
            return frame_

    def populate_ssim_array(self, frames: list):
        ssim_array = [1.0]
        original_frame = frames[0]

        for frame in frames[1:]:
            (score, diff) = ssim(original_frame, frame, full=True)
            ssim_array.append(score)

        return ssim_array

    def get_ssim_results(self):
        grayscale_array = []

        # create an array full of grayscale space frames
        for video in self.video_names:
            frame = self.get_frame(video)
            grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            grayscale_array.append(grayscale_frame)

        return self.populate_ssim_array(grayscale_array)
