from media_editor import combine_audio_video
import sys

if __name__ == '__main__':
    video_file_path = sys.argv[1]
    audio_file_path = sys.argv[2]
    combine_audio_video(video_file_path, audio_file_path, output_folder='.')