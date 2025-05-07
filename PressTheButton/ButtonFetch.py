import sys
from bs4 import BeautifulSoup
import requests
import subprocess
import random
from playwright.sync_api import sync_playwright
import time
import os
from PIL import Image
import shutil
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


SentencePrompt = """Turn the following sentences into a one that i can input into a text to image and get an image that is related to the sentence. Here are some instructions to follow: \n Your response should just be the one prompts one by one and nothing else, dont give me any explanation of your response or anything just give me the one liners ONLY, make sure you give a clean sentence that doesn't have any profanities or anything wrong in it. Number the sentences\n If there are any individuals like celebrities or celebrity groups in the sentences, change them into something they are known for, for example, instead of naming an actor, describe a role they are known for. \nDont depict anything religious in your one prompt, instead if the sentence as religious context, do your best to describe it without mentioning religion in your prompt.\nEach new line is a new prompt, ignore punctuation at the end of the sentences\n ALSO SPECIFY A CREATIVE, UNIQUE ART STYLE FOR THE PROMPT THAT IS NOT PHOTOREALISTIC.\n Finally here are the sentences:\n"""
ShortenPrompt = """Give me a shortened version of each sentence that is MAXIMUM OF 75 CHARACTERS\nHere is some context to help you:\nI want these shortened version for a series called 'Will you press the button?' so each pair of two sentences describe something that will occur if you press the button, with the first thing being the positive and the second being the negative. I will be reading out each of these sentences but I want shortened text that will be displayed after i'm done reading therefore I need the shortened version to fully encompass what each sentence entails.\nyour response should just be the shortened sentences one by one and nothing else, dont give me any explanation of your response or anything just give me the shortened sentence ONLY, make sure you give a clean sentence that doesn't have any profanities or anything wrong in it.\nNumber the sentences. The format of your response should be positive sentence, one line gap, negative sentence, one line gap, etc..\nignore punctuation at the end of the sentences\nREMEMBER THE FORMAT AND THAT EACH SHORTENED VERSION SHOULD BE A MAXIMUM OF 75 CHARACTERS. MAKE SURE THE DESCRIPTIONS ARE CLEAN AND DONT GET FLAGGED FOR INAPPROPRIATE CONTENT\nFinally, here are the sentences:\n\n"""
#ShortenPrompt = """Shorten each sentence to MAXIMUM OF 60 CHARACTERS, If sentence already less than 60 characters then don't change it. Number your sentences\n"""


def GetShortenedDesc(Plus, Minus):

    if len(Plus) != len(Minus):
        sys.exit("ERROR: PROMPTS NOT EVEN")

    PlusDes = []
    MinusDes = []
    uselessline = False
    Prompt = ShortenPrompt
    for plus, minus in zip(Plus, Minus):
        Prompt += plus + "\n" + minus + '\n'
    with sync_playwright() as p: #Dont want to pay for gpt4o use so go to this website which allows unlimited uses and scrape answer
        browser = p.chromium.launch(headless=True) #While free, this does considerably increase runtime (wait for site to load)
        page = browser.new_page()
        url = 'https://toolbaz.com/writer/ai-story-generator'
        # url = 'https://writify.ai/tool/ai-chat/'

        page.goto(url, wait_until="domcontentloaded")
        # page.wait_for_timeout(2000)
        # cdp_session = page.context.new_cdp_session(page)
        # cdp_session.send("Page.stopLoading")
        # page.reload()
        page.wait_for_timeout(8000)
        page.select_option("select#model", "Gemini-2.5-Flash 🆕")
        page.click('textarea#input')
        page.wait_for_timeout(100)
        page.keyboard.type(Prompt[0:40])
        page.wait_for_timeout(5000)
        page.keyboard.type(Prompt[40:-1])
        page.click('button#main_btn')
        page.wait_for_selector('div[id="output"]', timeout=30000)

        print("Getting Image desc...")
        li_elements = page.locator("#output > ol > li")
        if li_elements:
            for i in range(li_elements.count()):
                text = li_elements.nth(i).text_content()
                if ("Here" in text and "liner" in text and ":" in text): #or "Let me know if these meet" in p.text_content():
                    uselessline = True
                    continue
                else:
                    if uselessline == False:
                        if (i % 2) == 0:
                            PlusDes.append(text)
                        else:
                            MinusDes.append(text)
                    else:
                        if (i % 2) == 0:
                            MinusDes.append(text)
                        else:
                            PlusDes.append(text)  

        time.sleep(1)
        page.click('textarea#input')
        page.locator('textarea#input').fill("")
        PlusImg = []
        MinusImg = []
        # for i in range(len(Prompt) + 10):
        #     page.keyboard.press("Backspace")
        #     page.keyboard.press("Delete")
        
        Prompt = SentencePrompt
        for pluses, minuses in zip(Plus, Minus):
            Prompt += pluses + "\n" + minuses + '\n'
        page.wait_for_timeout(100)
        page.keyboard.type(Prompt[0:40])
        page.wait_for_timeout(5000)
        page.keyboard.type(Prompt[40:-1])
        page.click('button#main_btn')
        time.sleep(10)
        page.wait_for_selector('div[id="output"]', timeout=30000)

        print("Getting Image prompts...")
        li_elements = page.locator("#output > ol > li")
        if li_elements:
            for i in range(li_elements.count()):
                text = li_elements.nth(i).text_content()
                if ("Here" in text and "liner" in text and ":" in text): #or "Let me know if these meet" in p.text_content():
                    uselessline = True
                    continue
                else:
                    if uselessline == False:
                        if (i % 2) == 0:
                            PlusImg.append(text)
                        else:
                            MinusImg.append(text)
                    else:
                        if (i % 2) == 0:
                            MinusImg.append(text)
                        else:
                            PlusImg.append(text)                        

                    
    return PlusDes, MinusDes, PlusImg, MinusImg

# GetShortenedDesc(['You become a shapeshifter', 'You get the lead role in a movie, and you get paid $2,000,000 for it.'], ['You endure the pain of your very flesh being ripped off and every bone breaking in your body each time you change', 'It is instantly well-known as worst movie of all time and you are hated by everyone.'])
# def FetchImageDescriptions(Plus, Minus):

#     Prompt = SentencePrompt
#     uselessline = False
#     retries = 0

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page()
#         url = 'https://toolbaz.com/writer/ai-story-generator'

#         page.goto(url, wait_until="domcontentloaded")

#         # page.wait_for_timeout(2000)
#         # cdp_session = page.context.new_cdp_session(page)
#         # cdp_session.send("Page.stopLoading")
#         # page.reload()
#         page.wait_for_timeout(8000)
#         page.select_option("select#model", "G-2.0-F-Thinking 🆕")
        
#     return PlusImg, MinusImg

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











def NewFetchImages(gennumber, ImgP, ImgN):
    subprocess.run(
        ['curl', '-sSf', 'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt', '-o', 'proxy-list.txt'],
        check=True
    )
    with open('proxy-list.txt', 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]

    proxy = random.choice(proxies)
    # shutil.rmtree("/Users/haziq/Desktop/TikTokGenerator/user_data")
    os.makedirs(f"/Users/haziq/Desktop/TikTokGenerator/PressTheButton/Images/GenNumber{gennumber}/Results", exist_ok=True)
    os.makedirs(f"/Users/haziq/Desktop/TikTokGenerator/PressTheButton/Images/GenNumber{gennumber}/Conditions", exist_ok=True)
    UBLOCK_ORIGIN_PATH = "/Users/haziq/Downloads/Ublock.crx"

    retries = 0
    with sync_playwright() as p:
        extension_path = os.path.splitext(UBLOCK_ORIGIN_PATH)[0]
        os.system(f"unzip -o {UBLOCK_ORIGIN_PATH} -d {extension_path} > /dev/null 2>&1")
        # browser = p.chromium.launch(headless=False)
        browser = p.chromium.launch_persistent_context(
            user_data_dir="./user_data",  # Specify a user data directory
            headless=False,  # Extensions work only in non-headless mode
            args=[
                f"--disable-extensions-except={extension_path}",
                f"--load-extension={extension_path}",
            ],
            proxy={"server": f"http://{proxy}"}
        )
        # context = browser.new_context()
        browser.clear_cookies()
        browser.add_init_script("indexedDB.deleteDatabase('your-db'); localStorage.clear();")
        page = browser.new_page()
        url = 'https://deepai.org/machine-learning-model/text2img'

        while retries < 2:
            try:
                page.goto(url, wait_until="domcontentloaded")
            except:
                retries +=1
                time.sleep(5)
            else:
                break

        # page.wait_for_timeout(2000)
        # cdp_session = page.context.new_cdp_session(page)
        # cdp_session.send("Page.stopLoading")
        # page.reload()
        page.wait_for_timeout(2000)
        
        page.click('button[id="modelHdButton"]')
        page.click('button[id="modelQualityButton"]')
        for i in range(len(ImgP)):
            page.click('textarea[class="model-input-text-input dynamic-border"]')
            page.keyboard.type(ImgP[i])
            page.click('button[id="modelSubmitButton"]')
            page.wait_for_timeout(5000)
            imgArea = page.query_selector('div[class="try-it-result-area"]')
            imgArea.wait_for_selector('img[class="placeholder-image"]', state="detached")
            imgArea = page.query_selector('div[class="try-it-result-area"]')
            img = imgArea.query_selector("img")
            img_url = img.get_attribute("src")
            response = requests.get(img_url)

            if response.status_code == 200:
                with open(f"/Users/haziq/Desktop/TikTokGenerator/PressTheButton/Images/GenNumber{gennumber}/Results/Q{i}.png", "wb") as file:
                    file.write(response.content)
            else:
                exit(-1)

            image = Image.open(f"/Users/haziq/Desktop/TikTokGenerator/PressTheButton/Images/GenNumber{gennumber}/Results/Q{i}.png")
            resized_image = image.resize((1024, 1024), Image.LANCZOS)
            resized_image.save(f"/Users/haziq/Desktop/TikTokGenerator/PressTheButton/Images/GenNumber{gennumber}/Results/Q{i}.png")
            
            page.wait_for_timeout(5000)
            page.click('textarea[class="model-input-text-input dynamic-border"]')
            for i in range(len(ImgP[i])):
                page.keyboard.press("Backspace")
                page.keyboard.press("Delete")
        
        browser.close()

    shutil.rmtree("/Users/haziq/Desktop/TikTokGenerator/user_data")
    retries = 0
    proxy = random.choice(proxies)
    with sync_playwright() as p:
        extension_path = os.path.splitext(UBLOCK_ORIGIN_PATH)[0]
        os.system(f"unzip -o {UBLOCK_ORIGIN_PATH} -d {extension_path} > /dev/null 2>&1")
        # browser = p.chromium.launch(headless=False)
        browser = p.chromium.launch_persistent_context(
            user_data_dir="./user_data",  # Specify a user data directory
            headless=False,  # Extensions work only in non-headless mode
            args=[
                f"--disable-extensions-except={extension_path}",
                f"--load-extension={extension_path}",
            ],
            proxy={"server": f"http://{proxy}"}
        )
        browser.clear_cookies()
        browser.add_init_script("indexedDB.deleteDatabase('your-db'); localStorage.clear();")
        page = browser.new_page()
        url = 'https://deepai.org/machine-learning-model/text2img'

        while retries < 2:
            try:
                page.goto(url, wait_until="domcontentloaded")
            except:
                retries +=1
                time.sleep(5)
            else:
                break

        # page.wait_for_timeout(2000)
        # cdp_session = page.context.new_cdp_session(page)
        # cdp_session.send("Page.stopLoading")
        # page.reload()
        page.wait_for_timeout(2000)
        
        page.click('button[id="modelHdButton"]')
        page.click('button[id="modelQualityButton"]')
        
        for i in range(len(ImgN)):
            page.click('textarea[class="model-input-text-input dynamic-border"]')
            page.keyboard.type(ImgN[i])
            page.click('button[id="modelSubmitButton"]')
            page.wait_for_timeout(5000)
            imgArea = page.query_selector('div[class="try-it-result-area"]')
            imgArea.wait_for_selector('img[class="placeholder-image"]', state="detached", timeout=1200000)
            imgArea = page.query_selector('div[class="try-it-result-area"]')
            img = imgArea.query_selector("img")
            img_url = img.get_attribute("src")
            response = requests.get(img_url)

            if response.status_code == 200:
                with open(f"/Users/haziq/Desktop/TikTokGenerator/PressTheButton/Images/GenNumber{gennumber}/Conditions/Q{i}.png", "wb") as file:
                    file.write(response.content)
            else:
                exit(-1)
            image = Image.open(f"/Users/haziq/Desktop/TikTokGenerator/PressTheButton/Images/GenNumber{gennumber}/Conditions/Q{i}.png")
            resized_image = image.resize((1024, 1024), Image.LANCZOS)
            resized_image.save(f"/Users/haziq/Desktop/TikTokGenerator/PressTheButton/Images/GenNumber{gennumber}/Conditions/Q{i}.png")
            page.wait_for_timeout(5000)
            page.click('textarea[class="model-input-text-input dynamic-border"]')
            for i in range(len(ImgN[i])):
                page.keyboard.press("Backspace")
                page.keyboard.press("Delete")
        
    shutil.rmtree("/Users/haziq/Desktop/TikTokGenerator/user_data")