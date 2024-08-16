import sys
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time
import os
import base64
from dotenv import load_dotenv
load_dotenv()

def ButtonFetch(numofquestions):
    url = "https://willyoupressthebutton.com/"
    Plus = []
    Minus = []
    for i in range(numofquestions):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        ResContent = soup.find(id='cond')
        Plus.append(ResContent.get_text())
        CondContent = soup.find(id='res')
        Minus.append(CondContent.get_text())
    
    return Plus, Minus


SentencePrompt = """Turn the following sentences into a one liner that i can input into a text to image and get an image that is related to the sentence. Here are some instructions to follow: \n Your response should just be the one liners one by one and nothing else, dont give me any explanation of your response or anything just give me the one liners ONLY, make sure you give a clean sentence that doesn't have any profanities or anything wrong in it. Dont number the sentences and add an end line after each sentence\n If there are any individuals like celebrities or celebrity groups in the sentences, change them into something they are known for, for example, instead of naming an actor, describe a role they are known for. \nDont depict anything religious in your one liner, instead if the sentence as religious context, do your best to describe it without mentioning religion in your prompt.\nEach new line is a new sentence, ignore punctuation at the end of the sentences\nREMEMBER THAT YOU ARE WRITING ONE LINERS FOR A TEXT TO IMAGE AI THAT IS NOT GREAT SO IT CANT UNDERSTAND NAMES OF PEOPLE, DISEASES ETC SO I NEED YOU TO DESCRIPTIVELY DESCRIBE A COMMON SCENE THAT IS VAGUELY RELATED TO THE SENTENCE. TEXT TO IMAGE AI ALSO CANT GENERATE TEXT IN THEIR IMAGES SO AVOID ANY DESCRIPTIONS THAT REQUIRE TEXT TO BE DISPLAYED IN THE IMAGE\nHere is some context that might help you understand the results im looking for. I want these images for a series called 'Will you press the button?' so each pair of two sentences describe something that will occur if you press the button, with the first thing being the positive and the second being the negative. I will be reading out each of these sentences but I want an image that will be displayed while i'm reading therefore I dont need the images to be too detailed but I just need them to vaguely make sense to with what I'm saying. However while your one liner can be vaguely related to my sentence, I need it to be descriptive as text to image AI's don't perform well with abstract prompts. REFRAIN from asking prompts where people's faces can be seen, trying specifying that its a backview and not front with the face. ALSO SPECIFY AN ART STYLE FOR THE PROMPT THAT IS NOT PHOTOREALISTIC.\n Finally here are the sentences:\n"""


def FetchImageDescriptions(Plus, Minus):

    Prompt = SentencePrompt
    PlusImg = []
    MinusImg = []

    for pluses, minuses in zip(Plus, Minus):
        Prompt += pluses + "\n" + minuses + '\n'

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        url = 'https://toolbaz.com/writer/ai-story-generator'
        page.goto(url, timeout=60000)
        page.wait_for_timeout(5000)
        page.select_option("select#model", "Llama-3-70B")
        page.fill('textarea#input', Prompt)
        page.wait_for_timeout(5000)          
        page.click('button#main_btn')
        page.wait_for_timeout(20000)

        output_div = page.query_selector('#output')
        if output_div:
            p_tags = output_div.query_selector_all('p')
            for i, p in enumerate(p_tags):
                if "Here" in p.text_content() and "liner" in p.text_content() and ":" in p.text_content():
                    continue
                else:
                    if (i % 2) == 0:
                        PlusImg.append(p.text_content())
                    else:
                        MinusImg.append(p.text_content())

    return PlusImg, MinusImg



def FetchImages(gennumber, ImgP, ImgN):

    os.makedirs(f"/Users/haziq/Desktop/TikTokGenerator/PressTheButton/Images/GenNumber{gennumber}/Results", exist_ok=True)
    os.makedirs(f"/Users/haziq/Desktop/TikTokGenerator/PressTheButton/Images/GenNumber{gennumber}/Conditions", exist_ok=True)

    engine_id = "stable-diffusion-v1-6"
    api_host = os.getenv('API_HOST', 'https://api.stability.ai')
    api_key = os.getenv("STABILITY_API_KEY")

    if api_key is None:
        raise Exception("Missing Stability API key.")
    
    if len(ImgP) != len(ImgN):
        return sys.exit("ERROR: RESULT N CONDITIONS LENGTHS DIFFERENT")

    for i in range(len(ImgP)):
        print(i)
        print(ImgP[i])
        response = requests.post(
            f"{api_host}/v1/generation/{engine_id}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "text_prompts": [
                    {
                        "text": ImgP[i]
                    }
                ],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 30,
            },
        )

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        data = response.json()

        for j, image in enumerate(data["artifacts"]):
            with open(f"/Users/haziq/Desktop/TikTokGenerator/PressTheButton/Images/GenNumber{gennumber}/Results/Q{i}.png", "wb") as f:
                f.write(base64.b64decode(image["base64"]))

        print(ImgN[i])
        response2 = requests.post(
            f"{api_host}/v1/generation/{engine_id}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "text_prompts": [
                    {
                        "text": ImgN[i]
                    }
                ],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 30,
            },
        )

        if response2.status_code != 200:
            raise Exception("Non-200 response: " + str(response2.text))

        data2 = response2.json()

        for k, image in enumerate(data2["artifacts"]):
            with open(f"/Users/haziq/Desktop/TikTokGenerator/PressTheButton/Images/GenNumber{gennumber}/Conditions/Q{i}.png", "wb") as f:
                f.write(base64.b64decode(image["base64"]))

        time.sleep(10)

