import time
import requests
import os
from dotenv import load_dotenv
load_dotenv()


def format_timestamp(ms):
    """Convert milliseconds to SRT timestamp format (HH:MM:SS,ms)."""
    total_seconds = ms / 1000
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    milliseconds = int((ms % 1000))
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def SpeechAndSrt(file_name, script, week_number, speaker="Liv", playback_speed_increase=0.20, pitch=1):

    key = os.environ['UNREAL_KEY']


    url = "https://api.v7.unrealspeech.com/synthesisTasks"

    payload = {
    "Text": script,
    "VoiceId": speaker,
    "Bitrate": "320k",
    "Speed": f'{playback_speed_increase}',
    "Pitch": f'{pitch}',
    "TimestampType": "word"
    }
    headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": f"Bearer {key}" 
    }

    response = requests.post(url, json=payload, headers=headers)
    time.sleep(15)
    response_json = response.json()
     
    audio_url = response_json.get('SynthesisTask').get('OutputUri') 
    audio_response = requests.get(audio_url)

    audio_path = f'/Users/haziq/Desktop/TikTokGenerator/RedditTypeVideo/speeches/week{week_number}/{file_name}.mp3'
    with open(audio_path, 'wb') as audio_file:
        audio_file.write(audio_response.content)

    timestamps_uri = response_json.get('SynthesisTask').get('TimestampsUri') ##see if synthesis workin
    timestamps_response = requests.get(timestamps_uri)
    timestamps_json = timestamps_response.json()
     

    srt_index = []

    for word_info in timestamps_json:
        word = word_info['word']
        start_time = word_info['start'] * 1000
        end_time = word_info['end'] * 1000
        start = format_timestamp(start_time)
        end = format_timestamp(end_time)
        srt_index.append((word, start, end))
        if ':_:' in word:
            srt_index.clear()
            post_end = start_time

    with open(f'/Users/haziq/Desktop/TikTokGenerator/RedditTypeVideo/str_scripts/week{week_number}/{file_name}.srt', 'w', encoding='utf-8') as srt_file:
        for i, (text, start, end) in enumerate(srt_index, start=1):
            srt_file.write(f"{i}\n")
            srt_file.write(f"{start} --> {end}\n")
            srt_file.write(f"{text}\n\n")
    
    return post_end











# from gtts import gTTS
# import os
# from pydub import AudioSegment
# import subprocess
# # import re

# def findTitleTime(Title, playback_speed=1.25):
#      TitleSpeech = gTTS(text=Title, lang='en', slow=False)
#      directory = f'/Users/haziq/Desktop/TikTokGenerator/tempaudios/TitleTime.mp3'
#      TitleSpeech.save(directory)
#      audio = AudioSegment.from_mp3(directory)
#      time = len(audio) / playback_speed
#      os.remove(directory)

#      return time

# def generate_speech(text, video_name, week_number, playback_speed=1.25):
#      wholespeech = gTTS(text=text, lang='en', slow=False)
#      dir = f'/Users/haziq/Desktop/TikTokGenerator/tempaudios/{video_name}.mp3'
#      wholespeech.save(dir)

#      command_aud_speed = [
#           "ffmpeg", '-y',
#           "-i", f'/Users/haziq/Desktop/TikTokGenerator/tempaudios/{video_name}.mp3',
#           "-filter:a", f'atempo={playback_speed}',
#           "-vn",
#           f'/Users/haziq/Desktop/TikTokGenerator/speeches/week{week_number}/{video_name}.mp3'
#      ]

#      subprocess.run(command_aud_speed, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#      os.remove(f'/Users/haziq/Desktop/TikTokGenerator/tempaudios/{video_name}.mp3')

#      audio = AudioSegment.from_mp3(f'/Users/haziq/Desktop/TikTokGenerator/speeches/week{week_number}/{video_name}.mp3')
#      length = len(audio) / 1000
#      print(f'The video will be {length // 60} minutes and {length % 60} seconds long')

# import os
# from dotenv import load_dotenv
# from deepgram import (
#         DeepgramClient,
#         SpeakOptions,
#     )



# def TtS(text, file_name):

#     load_dotenv()

#     SPEAK_OPTIONS = {"text" : text}
#     filename = f'/Users/haziq/Desktop/TikTokGenerator/speeches/{file_name}.mp3'

#     deepgram = DeepgramClient(api_key=os.getenv("DEEPGRAM_KEY"))

#     options = SpeakOptions(model="aura-asteria-en")

#     response = deepgram.speak.rest.v("1").save(filename, SPEAK_OPTIONS, options)
#     #print(response.to_json(indent=4))