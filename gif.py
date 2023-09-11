from moviepy.editor import VideoFileClip
import sys
import os


def convert_to_gif(video_path, output_path):
    video = VideoFileClip(video_path)
    video.write_gif(output_path, program='ffmpeg')
    video.close()


if __name__ == '__main__':
    video_path = sys.argv[1]
    output_path = f'{os.path.basename(video_path).split(".")[0]}.gif'
    convert_to_gif(video_path, output_path)
