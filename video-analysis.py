from skimage.metrics import structural_similarity as ssim
import cv2
import os

from analysis.size import SizeAnalysis
from utilities.plot import Plotter


def get_frame(video_path: str):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    middle_frame = int(total_frames / 2)

    # take the middle frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame)
    (res_, frame_) = cap.read()

    if not res_:
        raise Exception("errors retrieving the frame: {}".format(video_path))
    else:
        return frame_


try:
    VIDEO_PATH = 'video_samples/'
    VIDEO_TEST_AGAINST = 'input.mp4'

    VIDEO_PATH_1 = 'video_samples/input.mp4'
    VIDEO_PATH_2 = 'video_samples/output.avi'

    video_names = os.listdir(VIDEO_PATH)
    old_index = video_names.index(VIDEO_TEST_AGAINST)
    video_names.insert(0, video_names.pop(old_index))
    print(video_names)

    # take 2 frames
    frame_1 = get_frame(VIDEO_PATH_1)
    frame_2 = get_frame(VIDEO_PATH_2)

    # convert to grayscale color space
    gray_1 = cv2.cvtColor(frame_1, cv2.COLOR_BGR2GRAY)
    gray_2 = cv2.cvtColor(frame_2, cv2.COLOR_BGR2GRAY)

    # calculate ssim
    (score, diff) = ssim(gray_1, gray_2, full=True)
    print("score = ", score)

    # obtain size of the provided video files
    print()
    print("VIDEO_PATH_1 size = {0:.2f} KiB".format(os.path.getsize(VIDEO_PATH_1) / 1000))
    print("VIDEO_PATH_1 size = {0:.2f} KiB".format(os.path.getsize(VIDEO_PATH_2) / 1000))

    # obtaining results
    size_analysis = SizeAnalysis(video_names)
    video_sizes = size_analysis.get_results()

    # plotting results
    plotter = Plotter(video_names)
    plotter.plot_sizes(video_sizes)

except Exception as e:
    print(e)
