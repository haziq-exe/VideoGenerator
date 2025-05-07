from pydub import AudioSegment
import random
import subprocess
import os


def audio_replace(total_dur, file_name, week_number, input_vid):

    audio = AudioSegment.from_mp3(f'/Users/haziq/Desktop/TikTokGenerator/RedditTypeVideo/speeches/week{week_number}/{file_name}.mp3')

    segment_duration = len(audio) / 1000

    max_start_time = total_dur - segment_duration
    start_time = abs(random.uniform(0, max_start_time))

    command_seg = [
            'ffmpeg', '-y',
            '-ss', str(start_time),         
            '-i', input_vid,                
            '-t', str(segment_duration),     
            '-c:v', 'copy',
            "-hide_banner", "-loglevel", "error",
            f'/Users/haziq/Desktop/TikTokGenerator/RedditTypeVideo/FinalVideos/{file_name}_SEGMENT.mp4'                 # Output file
    ]

    command_aud = [
         'ffmpeg', '-y',
            '-i', f'/Users/haziq/Desktop/TikTokGenerator/RedditTypeVideo/FinalVideos/{file_name}_SEGMENT.mp4',                # Input video file
            '-i', f'/Users/haziq/Desktop/TikTokGenerator/RedditTypeVideo/speeches/week{week_number}/{file_name}.mp3', ##REMOVED CHILL BACKGROUND MUSIC
            '-map','0:v',
            '-map', '1:a',
            '-c:v', 'copy',
            '-c:a', 'aac',
            "-hide_banner", "-loglevel", "error",
            f'/Users/haziq/Desktop/TikTokGenerator/RedditTypeVideo/FinalVideos/{file_name}_AUDIO.mp4'                 # Output file
    ]

    subprocess.run(command_seg)#, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # subprocess.run(command_aud_file)#, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(command_aud)#, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    os.remove(f'/Users/haziq/Desktop/TikTokGenerator/RedditTypeVideo/FinalVideos/{file_name}_SEGMENT.mp4')
    #os.remove(f'/Users/haziq/Desktop/TikTokGenerator/RedditTypeVideo/tempaudios/{file_name}.mp3')

    return len(audio)

def mega_cmd(title_time, file_name, week_number, position=10):

    title_time_sec = title_time / 1000

    command_mega = [
        'ffmpeg', '-y',
        '-i', f'/Users/haziq/Desktop/TikTokGenerator/RedditTypeVideo/FinalVideos/{file_name}_AUDIO.mp4',
        '-i', f'/Users/haziq/Desktop/TikTokGenerator/RedditTypeVideo/PostImage/FinalPostImages/week{week_number}/{file_name}.png',
        '-filter_complex', f"[1:v]scale=iw*0.85:ih*0.85[overlay];[0:v][overlay]overlay=x='(W/12.65):y='(H/2.65):enable='between(t,0,{title_time_sec})',subtitles='/Users/haziq/Desktop/TikTokGenerator/RedditTypeVideo/str_scripts/week{week_number}/{file_name}.srt':force_style='Alignment={position},FontName='AvenirNextCyr-HeavyItalic',FontSize=25'",
        '-c:v', 'libx264',                     
        '-c:a', 'copy',
        "-hide_banner", "-loglevel", "error",
        f'/Users/haziq/Desktop/TikTokGenerator/RedditTypeVideo/FinalVideos/week{week_number}/{file_name}_FINAL.mp4'
    ]
    subprocess.run(command_mega)#, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    os.remove(f'/Users/haziq/Desktop/TikTokGenerator/RedditTypeVideo/FinalVideos/{file_name}_AUDIO.mp4')


# def add_img(title_time=5000, file_name='test', scaling_factor=0.5):

#     time_in_sec = 5 #title_time / 1000
    
#     command_img = [
#         'ffmpeg',
#         '-i', f'/Users/haziq/Desktop/TikTokGenerator/Testvid.mp4',
#         '-i', f'/Users/haziq/Desktop/TikTokGenerator/PostImage/FinalPostImages/{file_name}.png',
#         '-filter_complex',
#         "[1:v]scale=iw*0.85:ih*0.85[img]; "
#         f"[0:v][img]overlay=x='W/12.65':y='H/2.65':enable='between(t,0,{time_in_sec})'",
#         '-vcodec', 'libx264',
#         '-pix_fmt', 'yuv420p',
#         '-c:a', 'copy',
#         '-y',
#         f'/Users/haziq/Desktop/TikTokGenerator/Testimg3.mp4',
#     ]

#     subprocess.run(command_img)
    


# def final_vid_gen(file_name, position=10):

#     command_final = [
#         'ffmpeg', '-y',  # '-y' option to overwrite output file
#         '-i', f'/Users/haziq/Desktop/TikTokGenerator/FinalVideos/{file_name}_AUDIO.mp4',
#         '-vf', f"subtitles='/Users/haziq/Desktop/TikTokGenerator/str_scripts/{file_name}.srt':force_style='Alignment={position},FontName='AvenirNextCyr-HeavyItalic',FontSize=30'",
#         #'-map', '0:v',  # Map the video stream from the first input
#         '-c:v', 'libx264',  # Re-encode the video using the H.264 codec
#         #'-c:a', 'aac',  # Use AAC codec for audio
#         f'/Users/haziq/Desktop/TikTokGenerator/FinalVideos/{file_name}_FINAL.mp4'
#     ]

#     subprocess.run(command_final)

#     os.remove(f'/Users/haziq/Desktop/TikTokGenerator/FinalVideos/{file_name}_AUDIO.mp4')