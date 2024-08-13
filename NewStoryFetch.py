from playwright.sync_api import sync_playwright
from Prompts import DrugPrompt, RageBaitPrompt, WritingPrompt, WorkIssuePrompt, TragicLoversStory, TragicManhoodPrompt, LostTeenageBoy, AskRedditType, DifferentMemoryPrompt, DudeUplifting, LongDistance, FamilySecretPrompt
import numpy as np

Prompts = {
        "AskReddit" :[AskRedditType, 0.35],
        "WritingPrompt" : [WritingPrompt, 0.35],
        "Drugs" : [DrugPrompt, 0.03], #Hard coded yes but what can you do, [Prompt, Prompt_Probability]
        "RageBait" : [RageBaitPrompt, 0.03], 
        "WorkIssue" : [WorkIssuePrompt, 0.03],
        "TragicLover" : [TragicLoversStory, 0.03],
        "TragicManhood" : [TragicManhoodPrompt, 0.03],
        "LostTeenageBoy" : [LostTeenageBoy, 0.03],
        "DifferentMemory" :[DifferentMemoryPrompt, 0.03],
        "DudeUplifting" : [DudeUplifting, 0.03],
        "LongDistance" : [LongDistance, 0.03],
        "FamilySecret" : [FamilySecretPrompt, 0.03]}


def FetchStory(prompt_type=None, numberofposts=2):

    prompta = []

    
    if prompt_type != None:
        if len(prompt_type) != numberofposts:
            print("ERROR: elements in prompt_type must match number of posts")
        for i in range(len(prompt_type)):
            prompt.append(Prompts[prompt_type[i]][0])
    else:
        ListPrompts = np.array(list(Prompts.values()))
        elements = ListPrompts[:, 0]
        probabilities = ListPrompts[:, 1]
        probabilities = np.array(probabilities, dtype=float)
        for i in range(numberofposts):
            num = np.random.choice(elements, p=probabilities)
            prompta.append(num)


    Script = []
    Title = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        url = 'https://toolbaz.com/writer/ai-story-generator'

        for prompt in Prompts:
            page.goto(url)
            page.wait_for_timeout(2000)
            page.fill('textarea#input', prompt)
            page.wait_for_timeout(3000)          
            page.click('button#main_btn')
            page.wait_for_timeout(20000)

            output_div = page.query_selector('#output')
            if output_div:
                p_tags = output_div.query_selector_all('p')
                ScriptTemp = [p.text_content() for p in p_tags]
                print(ScriptTemp)
                ScriptWords = " ".join(ScriptTemp)
                Title.append(ScriptTemp[0])
                Script.append(ScriptWords)

        browser.close()
        
    return Script, Title