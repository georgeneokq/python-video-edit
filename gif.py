from moviepy.editor import VideoFileClip
import os
import argparse
from helper import multiglob


def convert_to_gif(video_path, output_path):
    video = VideoFileClip(video_path)
    video.write_gif(output_path, program='ffmpeg')
    video.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_files', type=str, nargs='+')
    args = parser.parse_args()

    input_files = args.input_files

    input_files = multiglob(input_files)
    joined_files_str = '\n'.join(input_files)
    print(f'Processing files:\n{joined_files_str}')
    for input_file in input_files:
        parent_folders = os.path.dirname(input_file)
        output_path = os.path.join(parent_folders, f'{os.path.basename(input_file).split(".")[0]}.gif')
        convert_to_gif(input_file, output_path)
