from dotenv import load_dotenv
import praw
import os
import re

load_dotenv()

client_id = os.environ['REDDIT_CLIENTID']
client_secret = os.environ['REDDIT_CLIENT_SECRET']
user_agent = os.environ['REDDIT_USER']

reddit = praw.Reddit(
    client_id= client_id,
    client_secret= client_secret,
    user_agent=user_agent
)

def replace_with_dict(text, replace_dict):
    pattern = re.compile('|'.join(re.escape(key) for key in replace_dict.keys()), re.IGNORECASE)
    
    return pattern.sub(lambda match: replace_dict[match.group(0).lower()], text)


def load_comments(numofcomments):

    Comments = []
    Question = []
    UrlFound = False

    with open('/Users/haziq/Desktop/TikTokGenerator/PostManagement/CompletedPosts.txt', 'r') as complete_fileR:
        complete = complete_fileR.readlines()

    with open('/Users/haziq/Desktop/TikTokGenerator/PostManagement/SlideshowPosts.txt', 'r') as slideshow_file:
        url = slideshow_file.readline()
        while UrlFound == False:
            if url not in complete:
                print(url)
                UrlFound = True
                submission = reddit.submission(url=url)
                submission.comment_sort = 'top'
                submission.comments.replace_more(limit=numofcomments)
                Question.append(submission.title)
                top_comments = submission.comments.list()[:numofcomments]
                for comment in top_comments:
                    Comments.append(comment.body)
                with open('/Users/haziq/Desktop/TikTokGenerator/PostManagement/CompletedPosts.txt', 'a') as complete_fileW:
                    complete_fileW.write(url + "\n")
            else:
                url = slideshow_file.readline()
            if url == "":
                return print("NO MORE NEW QUESTIONS IN FILE")
    

    while "[deleted]" in Comments:
        Comments.remove("[deleted]")

    for i in range(len(Comments)):
        text = Comments[i]
        cleantext = replace_with_dict(text, replacement_dict)
        Comments[i] = cleantext

    return Question, Comments
    


replacement_dict = {
    "fuck": "f**k",
    "shit":"sh*t",
    "asshole":"as*hole",
    "retard" : "ret**d",
    "bitch": "b**tch",
    "rape":"r**e",
    # "kill":"k*ll",
    "murder":"m**der",
    "sexually":"s*xually",
    "assaulted": "as**ulted"
}










# post_id = '6qi5mb'
# post = reddit.submission(id=post_id)
# content = post.selftext

# urls = re.findall(r'(https?://[^\s]+)', content)
# cleaned_urls = [url.rstrip(')') for url in urls]

# for url in urls:
#     url = url[:len(url) - 1]
#     with open('/Users/haziq/Desktop/TikTokGenerator/PostManagement/SlideshowPosts.txt', 'a') as write_file:
#         write_file.write(url + '\n')

