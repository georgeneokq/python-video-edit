"""
TO FIX: Decreased quality of gif
"""
import subprocess
import json
import sys
import os
import os.path as path

with open('config.json') as config_file:
    config = json.load(config_file)

ffmpeg_path = path.join(os.getcwd(), config['ffmpeg_path'])
print('[INFO] Using ffmpeg binary from: {}'.format(ffmpeg_path))
ffmpeg_path = path.join(os.getcwd(), config['ffmpeg_path'])


def to_gif(video_path, output_path):
    command = f'{ffmpeg_path} -i "{video_path}" "{output_path}"'
    subprocess.call(command, shell=True)


if __name__ == '__main__':
    video_path = sys.argv[1]
    output_path = f'{os.path.basename(video_path).split(".")[0]}.gif'
    to_gif(video_path, output_path)
