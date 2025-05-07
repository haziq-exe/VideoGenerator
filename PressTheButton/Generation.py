from ButtonFetch import ButtonFetch, FetchImages, GetShortenedDesc, NewFetchImages
from ScriptRefine import RefineScript
from SpeechGen import SpeechGen
from VideoGen import audio_replace, ImageAdd, FinalTouches
from ShortsUpload import upload_video
from ImageDesc import AddDesc
from pydub import AudioSegment
import subprocess

def increase_playback_speed(input_file, output_file, speed_factor):
    command = [
        'ffmpeg', '-y',
        '-i', input_file,                  
        '-filter:v', f'setpts={1/speed_factor}*PTS',  
        '-filter:a', f'atempo={speed_factor}',        
        '-c:v', 'libx264',                 
        '-c:a', 'aac',                     
        '-b:a', '320k',         
        output_file                        
    ]

    subprocess.run(command, check=True)

def Generation(gen_number, num_questions, desired_dur_ms=58000):

    print("Getting Scenarios...")
    positive, negative = ButtonFetch(numofquestions=num_questions)
    print("Scenarios Fetched!")
    for pos, neg in zip(positive, negative):
        print(f"{pos} but {neg}")
    PosDesc, NegDesc, positive_img, negative_img = GetShortenedDesc(positive, negative)
    print("Got Descriptions!")
    print("Got Image Prompts!")
    print("Getting Images...")
    print(PosDesc)
    # NewFetchImages(gennumber=gen_number, ImgP=positive_img, ImgN=negative_img)
    FetchImages(gennumber=gen_number, ImgP=positive_img, ImgN=negative_img)
    print("Got Images!")
    script = RefineScript(positive, negative)
    posStart, negStart, wholeEnd = SpeechGen(script=script, gennumber=gen_number, speaker="Scarlett", pitch= 1.0)
    AddDesc(gennumber=gen_number, numofquestions=num_questions, positive=PosDesc, negative=NegDesc)
    audio_replace(gennumber=gen_number, pos_start=posStart, neg_start=negStart, whole_end=wholeEnd)
    ImageAdd(pos_start=posStart, neg_start=negStart, whole_end=wholeEnd, gennumber=gen_number)
    FinalTouches(pos_start=posStart, neg_start=negStart, whole_end=wholeEnd, gennumber=gen_number)
   
    audio = AudioSegment.from_file(f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gen_number}_DESC.mp4')

    if len(audio) > 74000:
        speedfactor = len(audio) / desired_dur_ms
        increase_playback_speed(f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gen_number}_DESC.mp4', output_file=f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gen_number}_SPED__FINAL.mp4', speed_factor=speedfactor)
        upload_video(gennumber=gen_number, pos_prompt=positive, neg_prompt=negative, sped=True)
    else:
        speedfactor = len(audio) / desired_dur_ms
        increase_playback_speed(f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gen_number}_DESC.mp4', output_file=f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gen_number}_SPED__FINAL.mp4', speed_factor=1.25)
        upload_video(gennumber=gen_number, pos_prompt=positive, neg_prompt=negative, sped=True)