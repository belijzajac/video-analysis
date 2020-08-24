from skimage.metrics import structural_similarity as ssim
import cv2


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
    VIDEO_PATH_1 = 'video_samples/input.mp4'
    VIDEO_PATH_2 = 'video_samples/output.avi'

    # take 2 frames
    frame_1 = get_frame(VIDEO_PATH_1)
    frame_2 = get_frame(VIDEO_PATH_2)

    # convert to grayscale color space
    gray_1 = cv2.cvtColor(frame_1, cv2.COLOR_BGR2GRAY)
    gray_2 = cv2.cvtColor(frame_2, cv2.COLOR_BGR2GRAY)

    # calculate ssim
    (score, diff) = ssim(gray_1, gray_2, full=True)
    print("score = ", score)


except Exception as e:
    print(e)

