Python-Video-Edit
===

## What's this?

A series of python scripts to edit video and audio, written mainly using `moviepy` library.

Features:
- Shift audio
- Combine video and audio
- Reverse video
- Concatenate videos
- Boomerang effect
- Create GIF

## Usage

### Shift audio
python main.py [--seek] SEEK [--video-path] VIDEO-PATH

Where SEEK is a number in seconds and VIDEO-PATH is the full path to the video.

SEEK is a required parameter.
Think from the perspective of the audio; Specifying a SEEK value of 2 seconds will start the audio from the 2 second mark.
Specifying a SEEK value of -2 seconds will cause the first 2 seconds of the video to play without audio.

Example usage:
``` python main.py --seek 10 --video-path C:\Users\USERNAME\my_video.mp4 ```

### Combine video and audio

To be written...

### Reverse video

To be written...

### Concatenate videos

To be written...

### Boomerang effect

To be written...

### Create GIF

To be written...

## Dependencies

`pip install -r requirements.txt`
