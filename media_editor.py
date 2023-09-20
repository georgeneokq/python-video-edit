'''
USEFUL INFO:

There are 44100 frames per second in an audio clip by default.
The default sample rate is 16-bit (2 bytes).
For stereo sound, the size would increase to 4 bytes per frame.
'''

import subprocess
import os.path as path
import os
import json
from moviepy.editor import *
import json
import numpy as np
from scipy.io.wavfile import write as wav_write
from helper import get_basename_from_path

with open('config.json') as config_file:
    config = json.load(config_file)

ffmpeg_path = path.join(os.getcwd(), config['ffmpeg_path'])
print('[INFO] Using ffmpeg binary from: {}'.format(ffmpeg_path))


# t is either negative or positive. If positive, the audio will start earlier
# If negative, audio will start later
def seek_audio(src_audio_path, seek_time):
    new_file_path = src_audio_path + '.seek_{}_seconds.wav'.format(seek_time)
    audioclip = AudioFileClip(src_audio_path)
    sound_array = audioclip.to_soundarray()
    sound_array = np.array(sound_array)
    sample_rate = audioclip.fps # default is 44100 times per second
    duration = audioclip.duration

    time = abs(seek_time)
    empty_sound_count = int(time * sample_rate)
    empty_sound = [0, 0]
    empty_sounds = np.zeros((empty_sound_count, 2))
    
    # If seek_time > 0, put the empty sound at the back after shifting sound to front
    # If seek time < 0, put the empty sound at the front after shifting sound to back (sound at back is lost)
    if seek_time > 0:
        sound_array = sound_array[empty_sound_count:len(sound_array)]
        sound_array = np.append(sound_array, empty_sounds)
    else:
        sound_array = sound_array[0:len(sound_array) - empty_sound_count]
        sound_array = np.append(empty_sounds, sound_array)

    sound_array = np.reshape(sound_array, (len(sound_array) // audioclip.nchannels, audioclip.nchannels))

    scaled = np.int16(sound_array/np.max(np.abs(sound_array)) * 32767)
    os.remove(src_audio_path)
    wav_write(new_file_path, sample_rate, scaled)
    
    return new_file_path


def sep_audio_video(src_file_path, output_folder='.'):
    file_count = len(os.listdir(output_folder)) # File count in output folder
    new_file_name = '{}.wav'.format(file_count + 1)
    new_file_path = path.join(output_folder, new_file_name)
    command = '{} -i {} -ab 160k -ac 2 -ar 44100 -vn {}'.format(ffmpeg_path, src_file_path, new_file_path)
    subprocess.call(command, shell=True)
    return new_file_path


def combine_audio_video(src_video_path, src_audio_path) -> str:
    """
    Combines video and audio

    Returns:
        str: output file path
    """
    video_file_name = get_basename_from_path(src_video_path)
    new_video_file_name = f'{video_file_name}-combined.mp4'
    src_videoclip = VideoFileClip(src_video_path)
    src_audioclip = AudioFileClip(src_audio_path)
    new_videoclip = src_videoclip.set_audio(src_audioclip)
    new_videoclip.write_videofile(new_video_file_name)
    return path.join(os.getcwd(), new_video_file_name)