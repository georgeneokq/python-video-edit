from moviepy.editor import VideoFileClip
import sys
import os
import argparse

def convert_to_gif(video_path, output_path):
    video = VideoFileClip(video_path)
    video.write_gif(output_path, program='ffmpeg')
    video.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str)
    args = parser.parse_args()

    video_path = args.input_file
    output_path = f'{os.path.basename(video_path).split(".")[0]}.gif'
    convert_to_gif(video_path, output_path)
