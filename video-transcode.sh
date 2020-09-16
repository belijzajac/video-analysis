#!/bin/bash
#
# Information taken from the following sources:
# https://en.wikipedia.org/wiki/Video_file_format
# https://slhck.info/video/2017/02/24/vbr-settings.html
# https://github.com/KDE/kdenlive/blob/f8654e66ced4c4f71c875a0a6205b5abec06930f/data/profiles.xml
#

input_file="input.mp4"
save_location="video_samples"

# --------------------------------------------------------------------------------
# Starting point of the script
# --------------------------------------------------------------------------------
startup () {
  mkdir -p ${save_location}
  check_if_exists
}

# --------------------------------------------------------------------------------
# Prints informational messages
# --------------------------------------------------------------------------------
print_message () {
  case "$1" in
    "good")
      printf '\E[32m'; echo "GOOD: $2"; printf '\E[0m'
      ;;
    "error")
      printf '\E[31m'; echo "ERROR: $2"; printf '\E[0m'
      exit 1
      ;;
  esac
}

# --------------------------------------------------------------------------------
# Checks if the input video file exists
# --------------------------------------------------------------------------------
check_if_exists () {
  if [ ! -f $(pwd)/${input_file} ];
    then print_message error "the input file ${input_file} doesn't exist";
  fi
  
  cp ${input_file} ${save_location}/${input_file}
}

# --------------------------------------------------------------------------------
# Silens commands' output
# --------------------------------------------------------------------------------
stfu () {
  "$@" >/dev/null 2>&1
  return $?
}

# --------------------------------------------------------------------------------
# Generic (HD for web, mobile devices...)
# --------------------------------------------------------------------------------
convert_generic () {
  print_message good "generating Generic Definition video files..."
  
  stfu ffmpeg -i ${input_file} -c:v libvpx -crf 30 -b:v 0 -quality good -c:a libvorbis -q:a 5 ${save_location}/webm_vp8_vorbis.webm
  
  stfu ffmpeg -i ${input_file} -c:v libx264 -crf 30 -c:a aac -ab 160k ${save_location}/mp4_h264_aac.mp4
  
  stfu ffmpeg -i ${input_file} -c:v mpeg2video -q:v 5 -q:a 3 ${save_location}/mpg_mpeg2video.mpg
}

# --------------------------------------------------------------------------------
# Ultra-High Definition (4K)
# --------------------------------------------------------------------------------
convert_ultrahd () {
  print_message good "generating Ultra-High Definition video files..."
  
  stfu ffmpeg -i ${input_file} -c:v libvpx-vp9 -crf 25 -b:v 0 -quality good -c:a libvorbis -q:a 5 ${save_location}/webm_vp9_vorbis.webm
  
  stfu ffmpeg -i ${input_file} -c:v libx265 -crf 25 -c:a aac -ab 160k ${save_location}/mp4_h265_aac.mp4
  
  stfu ffmpeg -i ${input_file} -c:v ffv1 -c:a flac -lossless 1 ${save_location}/mkv_ffv1_flac.mkv
}

# --------------------------------------------------------------------------------
# Old-TV definition (DVD...)
# --------------------------------------------------------------------------------
convert_oldtv () {
  print_message good "generating Old-TV definition video files..."
  
  stfu ffmpeg -i ${input_file} -c:v mpeg2video -q:v 5 -c:a ac3 -ab 160k ${save_location}/vob_mpeg2video_ac3.vob
  
  stfu ffmpeg -i ${input_file} -c:v libx264 -crf 5 -c:a aac -ab 128k ${save_location}/flv_h264_aac.flv
  
  stfu ffmpeg -i ${input_file} -c:v libx264 -crf 5 -c:a aac -q:a 5 ${save_location}/avi_h264_aac.avi
  
  stfu ffmpeg -i ${input_file} -c:v wmv2 -q:v 5 -c:a wmav2 -q:a 5 ${save_location}/wmv_wmv2_wmav2.wmv
}

# --------------------------------------------------------------------------------
# Runs the script
# --------------------------------------------------------------------------------
run () {  
  startup
  convert_generic
  convert_ultrahd
  convert_oldtv
}

run
