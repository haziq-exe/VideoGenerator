from pydub import AudioSegment
import random
import subprocess
import os


def audio_replace(gennumber, pos_start, neg_start, whole_end, total_dur=148, input_vid='/Users/haziq/Desktop/TikTokGenerator/PressTheButton/LongVid/LongVid.mov', input_audio_vol=0.5):

    audio = AudioSegment.from_mp3(f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/speeches/Gen{gennumber}.mp3')

    segment_duration = len(audio) / 1000

    max_start_time = total_dur - segment_duration
    start_time = abs(random.uniform(0, max_start_time))

    command_seg = [
            'ffmpeg', '-y',
            '-ss', str(start_time),         # Start time
            '-i', input_vid,                # Input video file
            '-t', str(segment_duration),     # Duration of the segment
            '-c:v', 'copy',
            f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_SEGMENT.mp4'
    ]

    command_aud = [
         'ffmpeg', '-y',
            '-i', f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_SEGMENT.mp4',                # Input video file
            '-i', f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/speeches/Gen{gennumber}.mp3',
            '-map','0:v',
            '-map', '1:a',
            '-c:v', 'copy',
            '-c:a', 'aac',
            f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_AUDIOTEMP.mp4'                 # Output file
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
    subprocess.run(command_aud)#, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(command)#, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    os.remove(f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_SEGMENT.mp4')
    os.remove(f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_AUDIOTEMP.mp4')


def ImageAdd(pos_start, neg_start, whole_end, gennumber):

    command_img = [
        "ffmpeg", "-y",
        "-i", f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_AUDIO.mp4'
    ]

    for i in range(len(pos_start)):
        command_img.extend(["-i", f"/Users/haziq/Desktop/TikTokGenerator/PressTheButton/Images/GenNumber{gennumber}/Results/Q{i}.png", "-i", f"/Users/haziq/Desktop/TikTokGenerator/PressTheButton/Images/GenNumber{gennumber}/Conditions/Q{i}.png"])
    
    filter_complex = []

    # for i in range(len(pos_start)):
    #     if i==0:
    #         filter_complex.append(f"[{(2*i)+1}:v]scale=iw*0.6:ih*0.6[overlaypos{i}];[0:v][overlaypos{i}]overlay=x=(main_w/overlay_w)/2:y=105:enable='between(t,{pos_start[i]},{whole_end[i]})' [overlaycompletepos{i}];")
    #         filter_complex.append(f"[{(2*i)+2}:v]scale=iw*0.6:ih*0.6[overlayneg{i}];[overlaycompletepos{i}][overlayneg{i}]overlay=x=(main_w/overlay_w)/2:y=(main_w - overlay_w) - 105:enable='between(t,{neg_start[i]},{whole_end[i]})' [overlaycompleteneg{i}];")
    #     else:
    #         filter_complex.append(f"[{(2*(i+1))+1}:v]scale=iw*0.6:ih*0.6[overlaypos{i}];[overlaycompleteneg{i-1}][overlaypos{i}]overlay=x=(main_w/overlay_w)/2:y=105:enable='between(t,{pos_start[i]},{whole_end[i]})' [overlaycompletepos{i}];")
    #         filter_complex.append(f"[{(2*(i+1))}:v]scale=iw*0.6:ih*0.6[overlayneg{i}];[overlaycompletepos{i}][overlayneg{i}]overlay=x=(main_w/overlay_w)/2:y=(main_w - overlay_w) - 105:enable='between(t,{neg_start[i]},{whole_end[i]})' [overlaycompleteneg{i}];")

    for i in range(len(pos_start)):
        pos_start[i] += 1
        neg_start[i] += 1
        slideanimationPos = f'if(gte(t,{pos_start[i]}+0.1), (main_w-overlay_w)/2, W*(1 - (t-{pos_start[i]})/0.1))'
        slideanimationNeg = f'if(gte(t,{neg_start[i]}+0.1), (main_w-overlay_w)/2, W*(1 - (t-{neg_start[i]})/0.1))'

        if i == 0:    
            filter_complex.append(
                f"[{(2*i)+1}:v]scale=iw*0.6:ih*0.6[overlaypos{i}];"
                f"[0:v][overlaypos{i}]overlay=x='{slideanimationPos}':y=105:enable='between(t,{pos_start[i]},{whole_end[i] + 3.5})'[overlaycompletepos{i}];"
                f"[{(2*i)+2}:v]scale=iw*0.6:ih*0.6[overlayneg{i}];"
                f"[overlaycompletepos{i}][overlayneg{i}]overlay=x='{slideanimationNeg}':y=main_h-overlay_h-105:enable='between(t,{neg_start[i]},{whole_end[i] + 3.5})'[overlaycompleteneg{i}];"
            )
        else:
            filter_complex.append(
                f"[{(2*i)+1}:v]scale=iw*0.6:ih*0.6[overlaypos{i}];"
                f"[overlaycompleteneg{i-1}][overlaypos{i}]overlay=x='{slideanimationPos}':y=105:enable='between(t,{pos_start[i]},{whole_end[i] + 3.5})'[overlaycompletepos{i}];"
                f"[{(2*i)+2}:v]scale=iw*0.6:ih*0.6[overlayneg{i}];"
                f"[overlaycompletepos{i}][overlayneg{i}]overlay=x='{slideanimationNeg}':y=main_h-overlay_h-105:enable='between(t,{neg_start[i]},{whole_end[i] + 3.5})'[overlaycompleteneg{i}];"
            )


    filter_complex_string = "".join(filter_complex)

        
    command_img.extend([
        "-filter_complex", filter_complex_string,
        "-map", f"[overlaycompleteneg{len(pos_start) - 1}]",
        "-map", "0:a",
        "-c:v", "libx264", "-c:a", "aac",
        f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_OUTPUT.mp4'
    ])
    
    subprocess.run(command_img)


#ImageAdd(pos_start=pos_start, neg_start=neg_start, whole_end=whole_end, gennumber=0)

def FinalTouches(pos_start, neg_start, whole_end, gennumber):

    commandFinal = [
        'ffmpeg', '-y',
        '-i', f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_OUTPUT.mp4',
        '-i', f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/VidElements/Overlay.png',
        '-i', f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/VidElements/Timer.mov',
    ]

    filter_complex = []
    filter_complex.append(f"[0:v][1:v]overlay=x=0:y=0:enable='between(t, 0, ({pos_start[0]} - 1))'[OpeningTitleDone];")

    for i in range(len(whole_end)):
        if i == 0:
            filter_complex.append(
                f"[2:v]scale=iw*0.55:ih*0.55[scaledtimer];"
                f"[scaledtimer]setpts=PTS+{whole_end[i]}/TB[overlay_delayed{i}];"
                f"[OpeningTitleDone][overlay_delayed{i}]overlay=x=((main_w-overlay_w)/2)+11:y=((main_h-overlay_h)/2)-2:enable='between(t, {whole_end[i]}, {whole_end[i]} + 3.5)'[timer{i}];"
            )
        else:
            filter_complex.append(
                f"[2:v]scale=iw*0.55:ih*0.55[scaledtimer];"
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

    print(pospercent)

    vf_command = []

    for i in range(len(whole_end)):
        vf_command.append(
        (   f"drawtext=text='\t{pospercent[i]}%\nVOTED YES':expansion=none:"
            f"fontfile=/Users/haziq/Library/Fonts/Oswald-VariableFont_wght.ttf:"
            f"fontcolor=black:fontsize=250:"
            f"x=(w-text_w)/2:y=(100):"
            f"enable='between(t,{whole_end[i]} + 3.6, {whole_end[i]} + 6)',"
            f"drawtext=text='\t{100 - pospercent[i]}%\nVOTED NO':expansion=none:"
            f"fontfile=/Users/haziq/Library/Fonts/Oswald-VariableFont_wght.ttf:"
            f"fontcolor=black:fontsize=250:"
            f"x=(w-text_w)/2:y=((h-text_h)) - 230:"
            f"enable='between(t,{whole_end[i]} + 3.6, {whole_end[i]} + 6)',"
        )
    ) 

    
    vf_command_str = "".join(vf_command)
    command_percent.extend([
        '-vf', vf_command_str,
        '-codec:a', 'copy',
        f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_FINALOUT.mp4'
    ])


    subprocess.run(commandFinal)
    subprocess.run(command_percent)
    os.remove(f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_PREFINAL.mp4')
    os.remove(f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_AUDIO.mp4')
    os.remove(f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_OUTPUT.mp4')

pos_start = [4 , 29.5,44.9]
neg_start = [9.7, 32.8,46.8]
whole_end = [21.6,37.1,51.4]
audio_replace(gennumber=1, pos_start=pos_start, neg_start=neg_start, whole_end=whole_end)
ImageAdd(pos_start=pos_start, neg_start=neg_start, whole_end=whole_end, gennumber=1)
FinalTouches(pos_start=pos_start, neg_start=neg_start, whole_end=whole_end, gennumber=1)