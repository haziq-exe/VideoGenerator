from pydub import AudioSegment
import random
import subprocess
import os

# WARNING: MANY WAYS TO IMPROVE EFFICIENCY OF THIS CODE, CURRENTLY IT GENERATES TOO MANY VIDEOS SEPERATELY
# NEED TO COMBINE COMMANDS TO REDUCE RUNTIME

def audio_replace(gennumber, pos_start, neg_start, whole_end, total_dur=148, input_vid='/Users/haziq/Desktop/TikTokGenerator/PressTheButton/LongVid/LongVid.mp4', input_audio_vol=0.04):

    audio_path = f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/speeches/Gen{gennumber}.mp3'
    main_audio = AudioSegment.from_mp3(audio_path)

    segment_duration = len(main_audio) / 1000

    max_start_time = total_dur - segment_duration
    start_time = abs(random.uniform(0, max_start_time))

    command_seg = [
            'ffmpeg', '-y',
            '-ss', str(start_time),         
            '-i', input_vid,                
            '-t', str(segment_duration),
            '-c:v', 'copy',
            f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_SEGMENT.mp4'
    ]

    command_aud_file = [
        "ffmpeg", '-y',
        "-i", f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/audio/Background.mp3',
        "-i", f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/speeches/Gen{gennumber}.mp3',
        "-filter_complex", f"[0:a]volume={input_audio_vol}[a1];[1:a]volume=1[a2];[a1][a2]amix=inputs=2[a]",
        "-map", "[a]",
        "-c:v", "copy",
        "-shortest",
        "-t", f'{segment_duration}',
        f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/tempaudios/Gen{gennumber}.mp3'
    ]
    command_aud = [
         'ffmpeg', '-y',
            '-i', f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_SEGMENT.mp4',              
            '-i', f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/tempaudios/Gen{gennumber}.mp3',
            '-map','0:v',
            '-map', '1:a',
            '-c:v', 'copy',
            '-c:a', 'aac',
            f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_AUDIOTEMP.mp4'               
    ]

    sound_effect = '/Users/haziq/Desktop/TikTokGenerator/PressTheButton/VidElements/Timer.mp3'

    command = [
    "ffmpeg", "-y",
    "-i", f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_AUDIOTEMP.mp4'
    ]

    for i in range(len(whole_end)):
        command.extend(["-i", sound_effect])
    
    filter_complex = []

    for i, time in enumerate(whole_end):
        delay_ms = time * 1000
        print(f'TIME: {time}')
        filter_complex.append(f"[{i+1}:a]adelay={delay_ms}|{delay_ms}[sf{i+1}];")
    
    mix_inputs = "".join([f"[sf{i+1}]" for i in range(len(whole_end))])
    filter_complex.append(f"[0:a]{mix_inputs}amix=inputs={len(whole_end) + 1}[aout]")

    filter_complex = "".join(filter_complex)

    command.extend([
        "-filter_complex", filter_complex,
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "copy",
        f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_AUDIO.mp4'
    ])




    subprocess.run(command_seg)#, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(command_aud_file)
    audio_path = f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/tempaudios/Gen{gennumber}.mp3'
    main_audio = AudioSegment.from_mp3(audio_path)
    increased_volume_audio = main_audio + 9
    increased_volume_audio.export(audio_path, format="mp3")
    subprocess.run(command_aud)#, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(command)#, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    os.remove(f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_SEGMENT.mp4')
    os.remove(f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_AUDIOTEMP.mp4')
    os.remove(f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/tempaudios/Gen{gennumber}.mp3')


def ImageAdd(pos_start, neg_start, whole_end, gennumber):

    command_img = [
        "ffmpeg", "-y",
        "-i", f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_AUDIO.mp4'
    ]

    for i in range(len(pos_start)):
        command_img.extend(["-i", f"/Users/haziq/Desktop/TikTokGenerator/PressTheButton/Images/GenNumber{gennumber}/Results/Q{i}.png", "-i", f"/Users/haziq/Desktop/TikTokGenerator/PressTheButton/Images/GenNumber{gennumber}/Conditions/Q{i}.png"])
    
    filter_complex = []

    for i in range(len(pos_start)):
        pos_start[i] += 1
        neg_start[i] += 1
        slideanimationPos = f'if(gte(t,{pos_start[i]}+0.1), (main_w-overlay_w)/2, W*(1 - (t-{pos_start[i]})/0.1))'
        slideanimationNeg = f'if(gte(t,{neg_start[i]}+0.1), (main_w-overlay_w)/2, W*(1 - (t-{neg_start[i]})/0.1))'

        if i == 0:    
            filter_complex.append( 
                f"[{(2*i)+1}:v]scale=iw*0.55:ih*0.55[overlaypos{i}];"
                f"[0:v][overlaypos{i}]overlay=x='{slideanimationPos}':y=140:enable='between(t,{pos_start[i]},{whole_end[i] + 3.5})'[overlaycompletepos{i}];"
                f"[{(2*i)+2}:v]scale=iw*0.55:ih*0.55[overlayneg{i}];"
                f"[overlaycompletepos{i}][overlayneg{i}]overlay=x='{slideanimationNeg}':y=main_h-overlay_h-140:enable='between(t,{neg_start[i]},{whole_end[i] + 3.5})'[overlaycompleteneg{i}];"
            )

        else:
            filter_complex.append(
                f"[{(2*i)+1}:v]scale=iw*0.55:ih*0.55[overlaypos{i}];"
                f"[overlaycompleteneg{i-1}][overlaypos{i}]overlay=x='{slideanimationPos}':y=140:enable='between(t,{pos_start[i]},{whole_end[i] + 3.5})'[overlaycompletepos{i}];"
                f"[{(2*i)+2}:v]scale=iw*0.55:ih*0.55[overlayneg{i}];"
                f"[overlaycompletepos{i}][overlayneg{i}]overlay=x='{slideanimationNeg}':y=main_h-overlay_h-140:enable='between(t,{neg_start[i]},{whole_end[i] + 3.5})'[overlaycompleteneg{i}];"
            )


    filter_complex_string = "".join(filter_complex)

        
    command_img.extend([
        "-filter_complex", filter_complex_string,
        "-map", f"[overlaycompleteneg{len(pos_start) - 1}]",
        "-map", "0:a",
        '-c:v', 'libx264',
        "-c:a", "aac",
        f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_OUTPUT.mp4'
    ])


    subprocess.run(command_img)

def FinalTouches(pos_start, neg_start, whole_end, gennumber):

    commandFinal = [
        'ffmpeg', '-y',
        '-i', f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_OUTPUT.mp4',
        '-i', f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/VidElements/Timer.mov',
    ]

    filter_complex = []

    for i in range(len(whole_end)):
        if i == 0:
            filter_complex.append(
                f"[1:v]scale=iw*0.55:ih*0.55[scaledtimer];"
                f"[scaledtimer]setpts=PTS+{whole_end[i]}/TB[overlay_delayed{i}];"
                f"[0:v][overlay_delayed{i}]overlay=x=((main_w-overlay_w)/2)+11:y=((main_h-overlay_h)/2)-2:enable='between(t, {whole_end[i]}, {whole_end[i]} + 3.5)'[timer{i}];"
            )
        else:
            filter_complex.append(
                f"[1:v]scale=iw*0.55:ih*0.55[scaledtimer];"
                f"[scaledtimer]setpts=PTS+{whole_end[i]}/TB[overlay_delayed{i}];"
                f"[timer{i-1}][overlay_delayed{i}]overlay=x=((main_w-overlay_w)/2)+11:y=((main_h-overlay_h)/2)-2:enable='between(t, {whole_end[i]}, {whole_end[i]} + 3.5)'[timer{i}];"
            )

    filter_complex_string = "".join(filter_complex)

    commandFinal.extend([
        "-filter_complex", filter_complex_string,
        "-map", f"[timer{len(whole_end) - 1}]:v",
        "-map", "0:a",
        "-c:a", "aac",
        f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_PREFINAL.mp4'
    ]
        )
    
    pospercent = []

    for i in range(len(neg_start)):
        pospercent.append(random.randint(0, 100))
    
    command_percent = [
        "ffmpeg",  "-y",
        "-i", f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_PREFINAL.mp4',
    ]

    vf_command = []

    for i in range(len(whole_end)):
        vf_command.append(
        (   f"drawtext=text='\t{pospercent[i]}%':expansion=none:"
            f"fontfile=/Users/haziq/Library/Fonts/SummerFavourite-ARLr6.ttf:"
            f"fontcolor=green:fontsize=115:"
            f"x=((w-text_w)/2):y=(290):"
            f"enable='between(t,{whole_end[i]} + 3.6, {whole_end[i]} + 6)',"
            f"drawtext=text='PUSHED THE BUTTON':expansion=none:"
            f"fontfile=/Users/haziq/Library/Fonts/SummerFavourite-ARLr6.ttf:"
            f"fontcolor=green:fontsize=115:"
            f"x=((w-text_w)/2):y=(425):"
            f"enable='between(t,{whole_end[i]} + 3.6, {whole_end[i]} + 6)',"
            f"drawtext=text='{100 - pospercent[i]}%':expansion=none:"
            f"fontfile=/Users/haziq/Library/Fonts/SummerFavourite-ARLr6.ttf:"
            f"fontcolor=red:fontsize=115:"
            f"x=(w-text_w)/2:y=((h-text_h)) - 500:"
            f"enable='between(t,{whole_end[i]} + 3.6, {whole_end[i]} + 6)',"
            f"drawtext=text='DECIDED AGAINST IT':expansion=none:"
            f"fontfile=/Users/haziq/Library/Fonts/SummerFavourite-ARLr6.ttf:"
            f"fontcolor=red:fontsize=115:"
            f"x=(w-text_w)/2:y=((h-text_h)) - 365:"
            f"enable='between(t,{whole_end[i]} + 3.6, {whole_end[i]} + 6)',"

        )
    ) 

    
    vf_command_str = "".join(vf_command)
    command_percent.extend([
        '-vf', vf_command_str,
        '-codec:a', 'copy',
        f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_FINALOUT.mp4'
    ])

    command_Actual_Final = [
        'ffmpeg', '-y',
        '-i', '/Users/haziq/Desktop/TikTokGenerator/PressTheButton/LongVid/Intro.mov',
        '-i', f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_FINALOUT.mp4',
        "-filter_complex", "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]",
        "-map", "[v]",
        "-map", "[a]",
        f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_FINAL.mp4'
    ]

    command_desc = [
        "ffmpeg", "-y",
        "-i", f"/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_FINAL.mp4"
    ]

    for i in range(len(pos_start)):
        command_desc.extend(["-i", f"/Users/haziq/Desktop/TikTokGenerator/PressTheButton/Images/GenNumber{gennumber}/Results/Q{i}-Desc.png", "-i", f"/Users/haziq/Desktop/TikTokGenerator/PressTheButton/Images/GenNumber{gennumber}/Conditions/Q{i}-Desc.png"])
    
    filter_complex = []

    for i in range(len(pos_start)):
        slideanimationPos = f'if(gte(t,{neg_start[i]}+0.1), (main_w-overlay_w)/2, W*(1 - (t-{neg_start[i]})/0.1))'
        slideanimationNeg = f'if(gte(t,{whole_end[i] - 2.5}+0.1), (main_w-overlay_w)/2, W*(1 - (t-{whole_end[i] - 2.5})/0.1))'

        if i == 0:    
            filter_complex.append(
                f"[0:v][{(2*i)+1}:v]overlay=x='{slideanimationPos}':y=0:enable='between(t,{neg_start[i]},{whole_end[i] + 4.5})'[overlaycompletepos{i}];"
                f"[overlaycompletepos{i}][{(2*i)+2}:v]overlay=x='{slideanimationNeg}':y=974:enable='between(t,{whole_end[i] - 2.5},{whole_end[i] + 4.5})'[overlaycompleteneg{i}];"
            )

        else:
            filter_complex.append(
                f"[overlaycompleteneg{i-1}][{(2*i)+1}:v]overlay=x='{slideanimationPos}':y=0:enable='between(t,{neg_start[i]},{whole_end[i] + 4.5})'[overlaycompletepos{i}];"
                f"[overlaycompletepos{i}][{(2*i)+2}:v]overlay=x='{slideanimationNeg}':y=974:enable='between(t,{whole_end[i] - 2.5},{whole_end[i] + 4.5})'[overlaycompleteneg{i}];"
            )

    filter_complex_string = "".join(filter_complex)

        
    command_desc.extend([
        "-filter_complex", filter_complex_string,
        "-map", f"[overlaycompleteneg{len(pos_start) - 1}]",
        "-map", "0:a",
        '-c:v', 'libx264',                        
        "-c:a", "aac",
        f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_DESC.mp4'
    ])

    subprocess.run(commandFinal)
    subprocess.run(command_percent)
    subprocess.run(command_Actual_Final)
    subprocess.run(command_desc)
    os.remove(f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_FINALOUT.mp4')
    os.remove(f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_PREFINAL.mp4')
    os.remove(f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_AUDIO.mp4')
    os.remove(f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_OUTPUT.mp4')
    #os.remove(f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_FINAL.mp4')