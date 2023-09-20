import argparse
from moviepy.editor import *


def get_basename_from_path(file_path: str):
    return os.path.basename(file_path).split('.')[0]


def loop_video(video_path, loop_count):
    video_clip = VideoFileClip(video_path)
    video_clip: VideoFileClip = video_clip.fx(vfx.loop, n=loop_count+1)
    audio_clip = AudioFileClip(video_path)
    audio_clip: AudioFileClip = audio_clip.fx(afx.audio_loop, nloops=loop_count+1)
    final_clip: VideoFileClip = video_clip.set_audio(audio_clip)
    video_file_name = get_basename_from_path(video_path)
    output_file_name = f'{video_file_name}-{loop_count}-loop{"s" if loop_count > 1 else ""}.mp4'
    final_clip.write_videofile(output_file_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str)
    parser.add_argument('-n', type=int, required=True, help="Loop count. First playback does not count as a loop.")
    
    args = parser.parse_args()
    file_path = args.input_file
    loop_count = args.n

    if loop_count <= 0:
        print("Loop count should greater than 0.")
        exit()

    loop_video(file_path, loop_count)