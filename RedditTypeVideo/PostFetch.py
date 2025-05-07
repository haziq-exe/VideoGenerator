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
    "fuck": "frick",
    "fucking": "firetrucking",
    "fucked": "fricked",
    "kill": "unalive",
    "killed":"unalived",
    "shit":"poo",
    "shitting": "pooing",
    "asshole": "buttocks",
    "ass": "buttocks",
    r"\\'": "'",
    "gun": "pew pew",
    "guns": "pew pews",
    "aitah": "A.I.T.A",
    "death": "unaliving",
    "dead": "unalived",
    "sex": "S.E.X",
    # "drugs":"medicine",
    "sexual":"S.E.X",
    "murderer":"unaliver",
    "murder":"unaliving",
    "murdered":"unalived",
    "motherfucker": "firetrucker",
    "motherfuckers":"firetruckers",
    "assholes":"buttockses",
    "tifu":'today I messed up',
    "porn": "corn",
    "dick": "penis",
    "cum": "goon",
    "cummed": "gooned",
    "orgasm":"climax",
    "orgasms": "climaxes",
    "orgasmed":"climaxed",
    "peg": "p.e.g",
    "pegging": "p.e.g.ing",
    "bondage": "bandage",
    "lube": "lotion",
    "rape": "grape",
    "kidnap" : "take",
    "kidnapped": "taken",
    "raped": "graped",
    # "suicide": "self-unalive",
    "r*ped":"graped",
    "r*pe":"grape",
    "r*pists":"grapers",
    "rapist":"graper",
    "rapists":"grapers",
}

def remove_after_word(text, word):
    # Convert both text and word to lowercase for case-insensitive comparison
    lower_text = text.lower()
    lower_word = word.lower()

    # Check if the word is in the text
    if lower_word in lower_text:
        # Split the string at the specified word (using the original case text)
        split_index = lower_text.index(lower_word)
        return text[:split_index].strip()
    else:
        # If the word isn't found, return the original text
        return text
    
def split_into_chunks(input_string, chunk_size=15000):
    words = input_string.split()
    chunks = []
    current_chunk = ""
    
    for word in words:
        # If adding the next word would exceed the chunk size, start a new chunk
        if len(current_chunk) + len(word) + 1 > chunk_size:
            chunks.append(current_chunk)
            current_chunk = word
        else:
            if current_chunk:
                current_chunk += " " + word
            else:
                current_chunk = word
    
    # Add the last chunk
    if current_chunk:
        if len(current_chunk) < 500:
            chunks[len(chunks) - 1] = chunks[len(chunks) - 1] + " " + current_chunk
        else:
            chunks.append(current_chunk)
    
    return chunks

def remove_links(text):
    # Regex pattern to match URLs
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    # Substitute URLs with an empty string
    return re.sub(url_pattern, '', text)


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

def fetch(total_posts, subreddit=['AmITheAsshole'], time='year', post_id=None):

    Title = []
    Final_Titles = []
    Posttemp = []
    Post = []
    Subreddit = []
    fetched_posts = 0
    count = 0
    with open("/Users/haziq/Desktop/TikTokGenerator/RedditTypeVideo/PostManagement/CompletedPosts.txt", 'r') as done_file:
        check_url = set(line.strip() for line in done_file)
        done_file.close()

    if post_id == None:

        for sub in subreddit:
            fetched_posts = 0
            while fetched_posts < total_posts:
                subreddit1 = reddit.subreddit(sub)
                submissions = subreddit1.top(time_filter=time, limit = count + 1)
                for submission in submissions:
                    if 'UPDATE' in submission.title or 'update' in submission.title or len(submission.selftext) > 5000 or submission.url in check_url or len(submission.title) > len(submission.selftext) or len(submission.selftext) < 500:
                        count += 1
                        continue
                    else:
                        Posttemp.append(submission)

                        fetched_posts += 1
                        count += 1

        highestupvote = [0] * total_posts
        topposts = [None] * total_posts
        for submission in Posttemp:
            if any(submission.score > upvote for upvote in highestupvote):
                topposts[total_posts - 1] = submission
                highestupvote[total_posts - 1] = submission.score
                topposts.sort(reverse=True)
                highestupvote.sort(reverse=True)
    else:
        topposts = []
        submission = reddit.submission(id=post_id)
        topposts.append(submission)


    for post in topposts:
        Title.append(post.title)
        Post.append(post.selftext)
        Subreddit.append(str(post.subreddit))
        print(post.url)
        Post[0] = remove_after_word(text = Post[0], word='edit:')
        if len(Post[0]) > 2300:
            Part = split_into_chunks(Post[0])  
        else:
            Part = [Post[0]]
        with open("/Users/haziq/Desktop/TikTokGenerator/RedditTypeVideo/PostManagement/CompletedPosts.txt", 'a') as done_file:
            done_file.write(f'{post.url}\n')
                
    # else: FOLLOWING CODE IS REDUNDANT, IT TAKES URLs IN FROM A .txt FILE THAT HAD REDDIT POSTS ON IT I HAND PICKED
    #     with open("/Users/haziq/Desktop/TikTokGenerator/PostManagement/CompletedPosts.txt", 'r') as done_file:
    #         check_url = set(line.strip() for line in done_file)
    #         done_file.close()

    #     with open(url_file, 'r') as file:
    #         while fetched_posts < total_posts:
    #                 url = file.readline().strip()
    #                 if url == "":
    #                     sys.exit("No more URLs in file")
    #                 url_slice = url[24:]
    #                 slash_index = url_slice.find('/')
    #                 subreddit = url_slice[:slash_index]
    #                 index_ID = 40 + len(subreddit)
    #                 if url in check_url:
    #                     continue
    #                 else:
    #                     post_ID_slice = url[index_ID:]
    #                     slash_index = post_ID_slice.find('/')
    #                     post_ID = post_ID_slice[:slash_index]
    #                     submission_post = reddit.submission(id=post_ID)
    #                     if 'UPDATE' in submission_post.title or 'update' in submission_post.title:
    #                         continue
    #                     else:
    #                         if 'AITA?' in (submission_post.selftext.lower()):
    #                             position = submission_post.selftext.find("AITA?")
    #                             post_text = (submission_post.selftext[:position + len("AITA?")])
                            
    #                         if (len(post_text) + len(submission_post.title) >= 3000):
    #                             continue
    #                         else:
    #                             print(f'Post length: {(len(post_text) + len(submission_post.title))}')
    #                             Title.append(submission_post.title)
    #                             Post.append(post_text)
    #                             with open("/Users/haziq/Desktop/TikTokGenerator/PostManagement/CompletedPosts.txt", 'a') as done_file:
    #                                 done_file.write(f'{url}\n')
    #                             fetched_posts += 1
    #                             print(f'{fetched_posts} / {total_posts}    Fetched')
                
    # for title, post in zip(Title, Post):
    #     new_title = replace_words(title, replacement_dict)
    #     new_post = replace_words(post, replacement_dict)
    #     post_edit = replace_integer_with_dot(new_post)
    #     edit_title = replace_integer_with_dot(new_title)
    #     final_title = remove_links(edit_title)
    #     final_post = remove_links(post_edit)
    new_title = replace_words(Title[0], replacement_dict)
    edit_title = replace_integer_with_dot(new_title)
    final_title = remove_links(edit_title)
    
    for i in range(len(Part)):
        Part[i] = replace_words(Part[i], replacement_dict)
        Part[i] = replace_integer_with_dot(Part[i])
        Part[i] = remove_links(Part[i])

        Final_Titles.append(final_title)
        # Script.append(f'{final_title} :_: {final_post}')


    return Part, Final_Titles, Subreddit
    