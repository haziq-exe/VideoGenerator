import os 
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
import pickle


CLIENT_SECRETS_FILE = '/Users/haziq/Desktop/TikTokGenerator/PressTheButton/client_secrets.json'
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_authenticated_service():
    creds = None
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print("Failed to refresh token: ", e)
                os.remove('token.pickle')
                return get_authenticated_service()
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build(API_SERVICE_NAME, API_VERSION, credentials=creds)


def upload_video(gennumber, pos_prompt, neg_prompt, title="WILL YOU PUSH THE BUTTON???", description="Decide wether you will accept the conditions and still push the button 😈\n\n\n",tags=['wouldyourather'], category_id='24', sped=False):
    
    newdescription = f'EPISODE {gennumber}: ' + description
    description = newdescription

    for posprompt, negprompt in zip(pos_prompt, neg_prompt):
        description += posprompt + ' but ' + negprompt + '😱😱😱\n\n'

    description += '\n\n' + '#redvsblue #wouldyourather #wouldyourathergame #willyoupushthebutton #buttongame #redbutton'

    youtube = get_authenticated_service()
    service = youtube

    if sped == False:
        file = f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_DESC.mp4'
    else:
        file = f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/FinalVid/Gen{gennumber}_SPED__FINAL.mp4'
        
    request_body = {
        'snippet': {
            'title': f'{title} #{gennumber}',
            'description': description,
            'categoryId': category_id,
            'tags': tags
        },
        'status': {
            'privacyStatus': 'public'
        }
    }

    media = MediaFileUpload(file, chunksize=-1, resumable=True, mimetype='video/mp4')

    request = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media
    )

    response = request.execute()
    return response


# def split(file_name, video_length, week_number, speed_factor=1.5):

#     os.makedirs(f'/Users/haziq/Desktop/TikTokGenerator/FinalVideos/week{week_number}/Shorts', exist_ok=True)

#     output_pattern = f'/Users/haziq/Desktop/TikTokGenerator/FinalVideos/week{week_number}/Shorts/{file_name}_%03d.mp4'
#     num_segments = 0

#     command_split1 = [
#         'ffmpeg', '-y',
#         '-i', f'/Users/haziq/Desktop/TikTokGenerator/tempaudios/ShortsSpedVid.mp4',
#         '-c', 'copy',
#         '-map', '0',
#         '-f', 'segment',
#         '-segment_time', str(60),
#         '-segment_format', 'mp4',
#         output_pattern
#     ]

#     command_split2 = [
#         'ffmpeg', '-y',
#         '-i', f'/Users/haziq/Desktop/TikTokGenerator/FinalVideos/week{week_number}/{file_name}_FINAL.mp4',
#         '-c', 'copy',
#         '-map', '0',
#         '-f', 'segment',
#         '-segment_time', str(60),
#         '-segment_format', 'mp4',
#         output_pattern
#     ]

#     if (video_length % 60) < 15:
#         command_sped = [
#             'ffmpeg', '-y',
#             '-i', f'/Users/haziq/Desktop/TikTokGenerator/FinalVideos/week{week_number}/{file_name}_FINAL.mp4',
#             '-filter:v', f'setpts=PTS/{speed_factor}',
#             '-filter:a', f'atempo={speed_factor}',
#             f'/Users/haziq/Desktop/TikTokGenerator/tempaudios/ShortsSpedVid.mp4'
#         ]

#         subprocess.run(command_sped)
#         subprocess.run(command_split1)

#     else:
#         if(video_length > 60):
#             subprocess.run(command_split2)
    
#     segment_files = [f for f in os.listdir(f'/Users/haziq/Desktop/TikTokGenerator/FinalVideos/week{week_number}/Shorts/') if f.startswith(file_name)]
#     num_segments = len(segment_files)

#     return num_segments
