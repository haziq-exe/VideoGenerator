from SpeechAndSrt import SpeechAndSrt
from GenVid import audio_replace, mega_cmd
from ImageGen import create_post
from PostFetch import fetch
from pydub import AudioSegment
import random
from datetime import datetime
from tiktokautouploader import upload_tiktok
import os
random.seed(datetime.now().timestamp())

def create_folder(weeknumber):
    os.makedirs(f'/Users/haziq/Desktop/TikTokGenerator/RedditTypeVideo/FinalVideos/week{weeknumber}', exist_ok=True)
    os.makedirs(f'/Users/haziq/Desktop/TikTokGenerator/RedditTypeVideo/PostImage/FinalPostImages/week{weeknumber}', exist_ok=True)
    os.makedirs(f'/Users/haziq/Desktop/TikTokGenerator/RedditTypeVideo/speeches/week{weeknumber}', exist_ok=True)
    os.makedirs(f'/Users/haziq/Desktop/TikTokGenerator/RedditTypeVideo/str_scripts/week{weeknumber}', exist_ok=True)

def retrive_vid(VidType):

    for vid in VidType:
        if vid == 'creepyencounters':
            options = ['Horror', 'Horror2']
            Vid = options[random.randint(0, len(options) - 1)]
        else:
            options = ['RL', 'Powerwash', 'Ski', 'BikeFPS', 'GTA', 'MC', 'ClashRoyale', 'Cooking']
            Vid = options[random.randint(0, len(options) - 1)]
    
    return Vid

def retrieve_hashtags_sound(VidType):
    hashtags = ['#storytime', '#redditstories', '#fyp', '#reddit']
    sound = None
    sound_vol = None

    if VidType == 'AmITheAsshole?':
        hashtags = ['#AITA', '#drama', '#reddit', '#fyp']
    if VidType == 'creepyencounters':
        hashtags = ['#horror', '#horrortok', '#creepy', '#scary', '#fyp', '#reddithorror']
        sound = 'Suspense, horror, piano and music box'
    if VidType == 'confessions':
        hashtags = ['#confessions', '#redditstories', '#fyp', '#reddit']

    return hashtags, sound, sound_vol
    



def Subreddit_Video(weeknumber, numberofposts, Vid=None, sound=None, sound_vol='background', playbackspeedincrease=0, pitch=1, speaker="Liv", subreddit=None, time=None, post_id=None):

    create_folder(weeknumber=weeknumber)

    Part, Titles, VidType = fetch(total_posts=numberofposts, subreddit=subreddit, time=time, post_id=post_id)
    print(f'FETCHED: {Titles}')


    for i in range(len(Part)):
        if Vid == None:
            Vid = retrive_vid(VidType=VidType[0])
        Vidaudio = AudioSegment.from_file(f'/Users/haziq/Desktop/TikTokGenerator/RedditTypeVideo/BigVid/{Vid}.mp4')
        Viddur = len(Vidaudio) / 1000
        hashtags, sound1, sound_vol1 = retrieve_hashtags_sound(VidType=VidType[0])
        if sound==None:
            sound = sound1
        if sound_vol ==None:
            sound_vol = sound_vol1

        for parts in Part:
            if "my wife" in parts.lower() or 'my girlfriend' in parts.lower():
                speaker = 'Will'
            if "my husband" in parts.lower() or 'my boyfriend' in parts.lower():
                speaker = 'Scarlett'

        filename = f'{weeknumber}--Vid--PART{i}'
        Title = Titles[0]
        # print(len(Part[i]))
        # print(len(Part))
        # if VidType[0] == 'confessions':
        #     Title = "CONFESSION: " + Title

        if len(Part) - 1 > 0:
            if i == 0:
                Title = Title + f" PART {i + 1}"
                Part[i] = Title + ":_: " + Part[i]
            else:
                if i == len(Part) - 1:
                    Title = Title + f" FINAL PART"
                    Part[i] = Title + ":_: " + Part[i]
                    
                else:
                    Title = Title + f" PART {i + 1}"
                    Part[i] = Title + ":_: " + Part[i]
        
        else:
            Title = Title
            Part[i] = Title + ":_: " + Part[i]
        
        title_time = SpeechAndSrt(file_name=filename, script=Part[i], week_number=weeknumber, speaker=speaker, playback_speed_increase=playbackspeedincrease, pitch=pitch)
        if VidType[0].lower() != "amitheasshole":
            Title = f'[r/{VidType[0]}] ' + Title
        create_post(title=Title, file_name=filename, week_number=weeknumber)
        print(f"post created for video{i + 1}")
        videolength = audio_replace(total_dur=Viddur, file_name=filename, input_vid=f'/Users/haziq/Desktop/TikTokGenerator/RedditTypeVideo/BigVid/{Vid}.mp4', week_number=weeknumber)
        print(f"audio done for video{i + 1}")
        mega_cmd(title_time=title_time, file_name=filename, week_number=weeknumber)
        print(f'Video {i + 1} Done generating') 
        # upload_tiktok(video=f'/Users/haziq/Desktop/TikTokGenerator/RedditTypeVideo/FinalVideos/week1/{filename}_FINAL.mp4', description=f"REAL STORY FROM REDDIT\n{Title}", accountname='GitShowcase',hashtags=hashtags, sound_name=sound, sound_aud_vol=sound_vol, copyrightcheck=True, suppressprint=False)

















# def Uplifting_News_Vid(weeknumber, numberofposts=5, Vid='ski', playbackspeedincrease=0, pitch=1, speaker="Liv"):

#     os.makedirs(f'/Users/haziq/Desktop/TikTokGenerator/FinalVideos/week{weeknumber}', exist_ok=True)
#     os.makedirs(f'/Users/haziq/Desktop/TikTokGenerator/PostImage/week{weeknumber}', exist_ok=True)
#     os.makedirs(f'/Users/haziq/Desktop/TikTokGenerator/speeches/week{weeknumber}', exist_ok=True)
#     os.makedirs(f'/Users/haziq/Desktop/TikTokGenerator/str_scripts/week{weeknumber}', exist_ok=True)


#     if Vid == 'ski':
#         Viddur = 617

#     Title = 'Sit back and relax while I bring you some uplifting news from the past week to give you hope TitleDone'
#     Script = fetch_uplifting_news(total_posts=numberofposts)
#     Final_Script = Title + Script
#     filename = f'Week{weeknumber}-Uplifting'
#     title_time = SpeechAndSrt(file_name=filename, script=Final_Script, week_number=weeknumber, speaker=speaker, playback_speed_increase=playbackspeedincrease, pitch=pitch)
#     #generate_speech(Final_Script, video_name=filename, week_number=weeknumber, playback_speed=playbackspeed)
#     #title_time = findTitleTime(Title=Title, playback_speed=playbackspeed)
#     #print("TtS done for uplift")
#     #create_srt(audio_name=filename, srt_name=filename, title_time=title_time, week_number=weeknumber)
#     #print("srt done for uplift")
#     create_post(Title=Title, file_name=filename, week_number=weeknumber)
#     print("post created for uplift")
#     audio_replace(total_dur=Viddur, file_name=filename, input_vid=f'/Users/haziq/Desktop/TikTokGenerator/BigVid/{Vid}.mp4', week_number=weeknumber, input_audio_vol=0.5)
#     mega_cmd(title_time=title_time, file_name=filename, week_number=weeknumber)
#     print("Uplift video done generating")