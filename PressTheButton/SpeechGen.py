import os
import requests
from dotenv import load_dotenv
import base64
from pydub import AudioSegment
import json
load_dotenv()


def format_timestamp(ms):
    """Convert milliseconds to SRT timestamp format (HH:MM:SS,ms)."""
    total_seconds = ms / 1000
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    milliseconds = int((ms % 1000))
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def SpeechGen(script, gennumber, speaker="Scarlett", playback_speed_increase=0, pitch=1):

    pos_start = []
    neg_start = []
    whole_end = []

    key = os.environ['UNREAL_KEY']

    url = "https://api.v7.unrealspeech.com/speech"

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
    response_json = response.json()
     
    audio_url = response_json.get('OutputUri') 
    audio_response = requests.get(audio_url)

    audio_path = f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/speeches/Gen{gennumber}.mp3'
    with open(audio_path, 'wb') as audio_file:
        audio_file.write(audio_response.content)

    timestamps_uri = response_json.get('TimestampsUri')
    timestamps_response = requests.get(timestamps_uri)
    timestamps_json = timestamps_response.json()

    for word_info in timestamps_json:
        word = word_info['word']
        start_time = word_info['start']
        if '::_:' in word:
            pos_start.append(start_time)
        if ':_::' in word:
            neg_start.append(start_time)
        if '_:_:_' in word:
            whole_end.append(start_time)
    
    for x in range(len(whole_end)):
        whole_end[x] += (6.0 * x)
        pos_start[x] += (6.0 * x)
        neg_start[x] += (6.0 * x)
        add_silence_to_audio(audio_path, audio_path, start_time=whole_end[x])
    

    # srt_index = []
    # Qs = 0

    # for word_info in timestamps_json:
    #     word = word_info['word']
    #     start_time = (word_info['start'] * 1000) + (6000 * Qs)
    #     end_time = word_info['end'] * 1000 + (6000 * Qs)
    #     start = format_timestamp(start_time)
    #     end = format_timestamp(end_time)
    #     if '::_:' in word:
    #         continue
    #     if ':_::' in word:
    #         continue
    #     if '_:_:_' in word:
    #         Qs += 1
    #         continue
    
    #     srt_index.append((word, start, end))

    #     with open(f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/str_scripts/Gen{gennumber}.srt', 'w', encoding='utf-8') as srt_file:
    #         for i, (text, start, end) in enumerate(srt_index, start=1):
    #             srt_file.write(f"{i}\n")
    #             srt_file.write(f"{start} --> {end}\n")
    #             srt_file.write(f"{text}\n\n")

    return pos_start, neg_start, whole_end

def add_silence_to_audio(input_file, output_file, start_time, silence_duration=6000):
    audio = AudioSegment.from_file(input_file)

    before_silence = audio[:start_time * 1000]  # pydub works in milliseconds
    after_silence = audio[start_time * 1000:]

    # Create a 6-second silent segment
    silence = AudioSegment.silent(duration=silence_duration)

    # Concatenate the audio segments: before silence + silence + after silence
    new_audio = before_silence + silence + after_silence

    # Export the modified audio to a new file
    new_audio.export(output_file, format="mp3")

# def NewSpeechGen(Script, gennumber):

#     pos_start = []
#     neg_start = []
#     whole_end = []

#     VOICE_ID = "N2lVS1w4EtoT3dr4eOWO"  # Callum
#     YOUR_XI_API_KEY = os.getenv("ELEVENLABS_KEY")

#     url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps"

#     headers = {
#     "Content-Type": "application/json",
#     "xi-api-key": YOUR_XI_API_KEY
#     }

#     data = {
#     "text": (
#         Script
#     ),
#     "model_id": "eleven_multilingual_v2",
#     "voice_settings": {
#         "stability": 0.5,
#         "similarity_boost": 0.75
#     }
#     }


#     response = requests.post(
#         url,
#         json=data,
#         headers=headers,
#     )

#     if response.status_code != 200:
#         print(f"Error encountered, status: {response.status_code}, "
#                 f"content: {response.text}")
#         quit()

#     # convert the response which contains bytes into a JSON string from utf-8 encoding
#     json_string = response.content.decode("utf-8")

#     # parse the JSON string and load the data as a dictionary
#     response_dict = json.loads(json_string)

#     # the "audio_base64" entry in the dictionary contains the audio as a base64 encoded string, 
#     # we need to decode it into bytes in order to save the audio as a file
#     audio_bytes = base64.b64decode(response_dict["audio_base64"])
#     audio_path = f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/speeches/Gen{gennumber}.mp3'

#     with open(audio_path, 'wb') as f:
#         f.write(audio_bytes)

#     # the 'alignment' entry contains the mapping between input characters and their timestamps
#     AlignedResponse = response_dict['alignment']
#     CharacList = AlignedResponse['characters']
#     start_time_list = AlignedResponse['character_start_times_seconds']
#     #end_time_list = AlignedResponse['character_end_times_seconds']

#     #print(CharacList)

#     for i in range(len(CharacList)):
#         word1 = "".join(CharacList[i:i+4])
#         word2 = "".join(CharacList[i:i+5])
#         if word1 == "::_:":
#             print(f'Found ::_: at: Index-{i}')
#             pos_start.append(start_time_list[i])
#         if word1 == ":_::":
#             print(f'Found :_:: at: Index-{i}')
#             neg_start.append(start_time_list[i])
#         if word2 == "_:_:_":
#             print(f'Found _:_:_ at: Index-{i}')
#             whole_end.append(start_time_list[i+5])

#     for x in range(len(whole_end)):
#         whole_end[x] += (6.0 * x)
#         pos_start[x] += (6.0 * x)
#         neg_start[x] += (6.0 * x)
#         add_silence_to_audio(audio_path, audio_path, start_time=whole_end[x])

#     return pos_start, neg_start, whole_end
