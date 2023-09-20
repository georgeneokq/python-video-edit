from moviepy.editor import concatenate_videoclips, VideoFileClip
import json
import subprocess
import os

with open('config.json') as config_file:
    config = json.load(config_file)

ffmpeg_path = os.path.join(os.getcwd(), config['ffmpeg_path'])
print('[INFO] Using ffmpeg binary from: {}'.format(ffmpeg_path))

def concatenate(video_clip_paths, output_path):
    # TODO: Assert same dimensions for all videos
    video_path_args = ' '.join([f'-i {file_path}' for file_path in video_clip_paths])
    va_args = ' '.join([f'[{i}:v] [{i}:a]' for i in range(len(video_clip_paths))])
    
    command = f'{ffmpeg_path} {video_path_args} -filter_complex "{va_args} concat=n={len(video_clip_paths)}:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" {output_path}'
    print(command)

    # write the output video file
    subprocess.call(command, shell=True)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Simple Video Concatenation script in Python with MoviePy Library")
    parser.add_argument("-c", "--clips", nargs="+",
                        help="List of audio or video clip paths")
    parser.add_argument("-o", "--output", help="Output file name")
    args = parser.parse_args()
    clips = args.clips
    output_path = args.output
    concatenate(clips, output_path)

    print(f"Concatenated video written to {output_path}")