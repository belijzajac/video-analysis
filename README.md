# video-analysis

Transcodes the given video file into a bunch of different video file formats, and does the analysis on them based on their size, structural similarity (ssim), and peak signal-to-noise ratio (psnr)

## dependencies

- ffmpeg
- python (3.8)
  - scikit-image >= 0.17.2
  - matplotlib >= 3.2.1

## usage

1. `bash video-transcode.sh` to transcode *input.mp4* into a bunch of different video file formats
2. `python3.8 video-analysis.py` to do the analysis on generated video files

## credits

- https://en.wikipedia.org/wiki/Video_file_format
- https://slhck.info/video/2017/02/24/vbr-settings.html
- https://github.com/KDE/kdenlive/blob/f8654e66ced4c4f71c875a0a6205b5abec06930f/data/profiles.xml
