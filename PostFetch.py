import praw
import re
import sys
import os
from dotenv import load_dotenv
load_dotenv()

# Replace these with your own credentials
client_id = os.environ['REDDIT_CLIENTID']
client_secret = os.environ['REDDIT_CLIENT_SECRET']
user_agent = os.environ['REDDIT_USER']

# Initialize the Reddit instance
reddit = praw.Reddit(
    client_id= client_id,
    client_secret= client_secret,
    user_agent=user_agent
)

done_URLS = []

replacement_dict = {
    "aita": "A.I.T.A",
    "fuck": "flip",
    "fucking": "firetrucking",
    "fucked": "flipped",
    "kill": "unalive",
    "killed":"unalived",
    "shit":"poo",
    "shitting": "pooing",
    "asshole": "buttocks",
    r"\\'": "'",
    "gun": "pew pew",
    "guns": "pew pews",
    "aitah": "A.I.T.A",
    "death": "unaliving",
    "dead": "unalived",
    "sex": "S.X",
    "drugs":"medicine",
    "sexual":"S.X",
    "murderer":"unaliver",
    "murder":"unaliving",
    "murdered":"unalived",
    "motherfucker": "firetrucker",
    "motherfuckers":"firetruckers",
    "assholes":"buttockses"
}

def replace_integer_with_dot(text):
    # Define the regex pattern to find an integer followed by F or M
    pattern = r'(\d+)\s*([FfMm])'  # \d+ matches one or more digits; \s* allows for optional spaces
    
    def replacement(match):
        return f"{match.group(1)}.{match.group(2).upper()}"

    modified_text = re.sub(pattern, replacement, text)
    
    return modified_text

def replace_words(text, replacements): #Function to make the dictionary case-insensitive
    def replace(match):
        # Get the original word from the match and check its case
        word = match.group(0)
        # Use the original casing of the matched word
        replacement = replacements[match.group(0).lower()]
        # Preserve the original case of the matched word
        if word.isupper():
            return replacement.upper()
        elif word[0].isupper():
            return replacement.capitalize()
        else:
            return replacement
    
    exclude_boundary = r"\\'"
    
    boundary_keys = [key for key in replacements.keys() if key != exclude_boundary]
    boundary_pattern = r'\b(' + '|'.join(re.escape(key) for key in boundary_keys) + r')\b'

    # Create a regex pattern for the keys in the replacements dictionary
    #pattern = re.compile('|'.join(re.escape(key) for key in replacements.keys()), re.IGNORECASE)

    if exclude_boundary:
        non_boundary_pattern = re.escape(exclude_boundary)
        pattern = re.compile(boundary_pattern + '|' + non_boundary_pattern, re.IGNORECASE)
    else:
        pattern = re.compile(boundary_pattern, re.IGNORECASE)



    # Substitute the matches in the text
    return pattern.sub(replace, text)

def fetch(total_posts, subreddit='AmITheAsshole', time='year', url_file=None):

    Title = []
    Final_Titles = []
    Post = []
    Script = []
    fetched_posts = 0

    if url_file == None:
        subreddit1 = reddit.subreddit(subreddit)

        while fetched_posts < total_posts:
            submission = subreddit1.top(time_filter=time, limit = 1)
            if 'UPDATE' in submission_post.title or 'update' in submission_post.title:
                continue
            else:
                Title.append(submission.title)
                Post.append(submission.selftext)
            
    else:
        with open("/Users/haziq/Desktop/TikTokGenerator/PostManagement/CompletedPosts.txt", 'r') as done_file:
            check_url = set(line.strip() for line in done_file)
            done_file.close()

        with open(url_file, 'r') as file:
            while fetched_posts < total_posts:
                    url = file.readline().strip()
                    if url == "":
                        sys.exit("No more URLs in file")
                    url_slice = url[24:]
                    slash_index = url_slice.find('/')
                    subreddit = url_slice[:slash_index]
                    index_ID = 40 + len(subreddit)
                    if url in check_url:
                        continue
                    else:
                        post_ID_slice = url[index_ID:]
                        slash_index = post_ID_slice.find('/')
                        post_ID = post_ID_slice[:slash_index]
                        submission_post = reddit.submission(id=post_ID)
                        if 'UPDATE' in submission_post.title or 'update' in submission_post.title:
                            continue
                        else:
                            if 'AITA?' in (submission_post.selftext.lower()):
                                position = submission_post.selftext.find("AITA?")
                                post_text = (submission_post.selftext[:position + len("AITA?")])
                            
                            if (len(post_text) + len(submission_post.title) >= 3000):
                                continue
                            else:
                                print(f'Post length: {(len(post_text) + len(submission_post.title))}')
                                Title.append(submission_post.title)
                                Post.append(post_text)
                                with open("/Users/haziq/Desktop/TikTokGenerator/PostManagement/CompletedPosts.txt", 'a') as done_file:
                                    done_file.write(f'{url}\n')
                                fetched_posts += 1
                                print(f'{fetched_posts} / {total_posts}    Fetched')
                
    for title, post in zip(Title, Post):
        new_title = replace_words(title, replacement_dict)
        new_post = replace_words(post, replacement_dict)
        post_edit = replace_integer_with_dot(new_post)
        final_title = replace_integer_with_dot(new_title)

        Final_Titles.append(final_title)
        Script.append(f'{final_title} :_: {post_edit}')


    return Script, Final_Titles
    