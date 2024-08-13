from playwright.sync_api import sync_playwright
from Prompts import DrugPrompt, RageBaitPrompt, WritingPrompt, WorkIssuePrompt, TragicLoversStory, TragicManhoodPrompt, LostTeenageBoy, AskRedditType, DifferentMemoryPrompt, DudeUplifting, LongDistance, FamilySecretPrompt, LetsNotMeetSubreddit, RedWritingPrompt
import numpy as np
from dotenv import load_dotenv
import praw
import os

load_dotenv()

client_id = os.environ['REDDIT_CLIENTID']
client_secret = os.environ['REDDIT_CLIENT_SECRET']
user_agent = os.environ['REDDIT_USER']

reddit = praw.Reddit(
    client_id= client_id,
    client_secret= client_secret,
    user_agent=user_agent
)


NumofPrompts = 13

Prompts = {
        "AskReddit" :[AskRedditType, 0.35],
        "WritingPrompt" : [RedWritingPrompt, 0.35],
        "Drugs" : [DrugPrompt, (0.3 /(NumofPrompts - 2))], #Hard coded yes but what can you do, [Prompt, Prompt_Probability]
        "RageBait" : [RageBaitPrompt, (0.3 /(NumofPrompts - 2))], 
        "WorkIssue" : [WorkIssuePrompt, (0.3 /(NumofPrompts - 2))],
        "TragicLover" : [TragicLoversStory, (0.3 /(NumofPrompts - 2))],
        "TragicManhood" : [TragicManhoodPrompt, (0.3 /(NumofPrompts - 2))],
        "LostTeenageBoy" : [LostTeenageBoy, (0.3 /(NumofPrompts - 2))],
        "DifferentMemory" :[DifferentMemoryPrompt, (0.3 /(NumofPrompts - 2))],
        "DudeUplifting" : [DudeUplifting, (0.3 /(NumofPrompts - 2))],
        "LongDistance" : [LongDistance,  (0.3 /(NumofPrompts - 2))],
        "FamilySecret" : [FamilySecretPrompt, (0.3 /(NumofPrompts - 2))],
        "LetsNotMeetPrompt" : [LetsNotMeetSubreddit, (0.3 /(NumofPrompts - 2))]}

def replace_words(texts, replacement_dict):
    replaced_texts = []
    for text in texts:
        words = text.split()
        replaced_words = [replacement_dict.get(word, word) for word in words]
        replaced_texts.append(" ".join(replaced_words))
    return replaced_texts


def CompleteRedditPrompt():

    Unique = False

    with open("/Users/haziq/Desktop/TikTokGenerator/PostManagement/CompletedPosts.txt", 'r') as done_file:
        check_url = set(line.strip() for line in done_file)
        done_file.close()
    
    while Unique == False:
        subreddit = reddit.subreddit("WritingPrompts")
        submissions = subreddit.top(time_filter='year', limit = 1)

        for submission in submissions:
            if submission.url in check_url or '[WP]' not in submission.title:
                continue
            else:
                finalprompt = RedWritingPrompt + submission.title
                Unique = True
                with open("/Users/haziq/Desktop/TikTokGenerator/PostManagement/CompletedPosts.txt", 'a') as done_file:
                    done_file.write(f'{submission.url}\n')
        
    return finalprompt



def FetchStory(prompt_type=None, numberofposts=2):

    prompts_L = []

    
    if prompt_type != None:
        if len(prompt_type) != numberofposts:
            print("ERROR: elements in prompt_type must match number of posts")
        for i in range(len(prompt_type)):
            if Prompts[prompt_type[i]][0] == RedWritingPrompt:
                newprompt = CompleteRedditPrompt()
                prompts_L.append(newprompt)
            else:
                prompts_L.append(Prompts[prompt_type[i]][0])
    else:
        ListPrompts = np.array(list(Prompts.values()))
        elements = ListPrompts[:, 0]
        probabilities = ListPrompts[:, 1]
        probabilities = np.array(probabilities, dtype=float)
        for i in range(numberofposts):
            randprompt = np.random.choice(elements, p=probabilities)
            if randprompt == RedWritingPrompt:
                newprompt = CompleteRedditPrompt()
            else: 
                prompts_L.append(randprompt)


    Script = []
    Title = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        url = 'https://toolbaz.com/writer/ai-story-generator'

        for prompt in prompts_L:
            page.goto(url, timeout=60000)
            page.wait_for_timeout(5000)
            page.fill('textarea#input', prompt)
            print(prompt)
            page.wait_for_timeout(5000)          
            page.click('button#main_btn')
            page.wait_for_timeout(20000)

            output_div = page.query_selector('#output')
            if output_div:
                p_tags = output_div.query_selector_all('p')
                ScriptTemp = [p.text_content() for p in p_tags]
                ScriptTemp = replace_words(ScriptTemp)
                ScriptWords = " ".join(ScriptTemp)

                Title.append(ScriptTemp[0])
                Script.append(ScriptWords)

        browser.close()
        
    return Script, Title


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
    "assholes":"buttockses",
    "prostitute": "BOP",
    "prostitutes":"BOPS",
    "Hitler":"Angry German Man",
}