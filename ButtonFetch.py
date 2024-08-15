import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import torch
from diffusers import StableDiffusion3Pipeline
import os

def ButtonFetch(numofquestions):
    url = "https://willyoupressthebutton.com/"
    Result = []
    Condition = []
    for i in range(numofquestions):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        ResContent = soup.find(id='cond')
        Result.append(ResContent.get_text())
        CondContent = soup.find(id='res')
        Condition.append(CondContent.get_text())
    
    return Result, Condition


SentencePrompt = """Turn the following sentences into a one liner that i can input into a text to image and get an image that is related to the sentence. Here are some instructions to follow: \n Your response should just be the one liners one by one and nothing else, dont give me any explanation of your response or anything just give me the one liners ONLY, make sure you give a clean sentence that doesn't have any profanities or anything wrong in it. Dont number the sentences and add an end line after each sentence\n If there are any individuals like celebrities or celebrity groups in the sentences, change them into something they are known for, for example, instead of naming an actor, describe a role they are known for. \nDont depict anything religious in your one liner, instead if the sentence as religious context, do your best to describe it without mentioning religion in your prompt.\nEach new line is a new sentence, ignore punctuation at the end of the sentences\nREMEMBER THAT YOU ARE WRITING ONE LINERS FOR A TEXT TO IMAGE AI THAT IS NOT GREAT SO IT CANT UNDERSTAND NAMES OF PEOPLE, DISEASES ETC SO I NEED YOU TO DESCRIPTIVELY DESCRIBE A COMMON SCENE THAT IS VAGUELY RELATED TO THE SENTENCE. TEXT TO IMAGE AI ALSO CANT GENERATE TEXT IN THEIR IMAGES SO AVOID ANY DESCRIPTIONS THAT REQUIRE TEXT TO BE DISPLAYED IN THE IMAGE\nHere is some context that might help you understand the results im looking for. I want these images for a series called 'Will you press the button?' so each pair of two sentences describe something that will occur if you press the button, with the first thing being the positive and the second being the negative. I will be reading out each of these sentences but I want an image that will be displayed while i'm reading therefore I dont need the images to be too detailed but I just need them to vaguely make sense to with what I'm saying. However while your one liner can be vaguely related to my sentence, I need it to be descriptive as text to image AI's don't perform well with abstract prompts.\n Finally here are the sentences:\n"""


def FetchImageDescriptions(Result, Condition):

    Prompt = SentencePrompt
    ResultImg = []
    CondImg = []

    for results, conditions in zip(Result, Condition):
        Prompt += results + "\n" + conditions + '\n'

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
        page.wait_for_timeout(10000)

        output_div = page.query_selector('#output')
        if output_div:
            p_tags = output_div.query_selector_all('p')
            for i, p in enumerate(p_tags):
                if i == 0:
                    continue
                else:
                    if (i % 2) == 0:
                        CondImg.append(p.text_content())
                    else:
                        ResultImg.append(p.text_content())

    return ResultImg, CondImg

TestR, TestC = ButtonFetch(4)
ImgR, ImgC = FetchImageDescriptions(TestR, TestC)

print(f'RESULT | {ImgR} : CONDITION | {ImgC}')


def FetchImages(gennumber, ImgR, ImgC):

    os.makedirs(f"/Users/haziq/Desktop/TikTokGenerator/PressTheButton/GenNumber{gennumber}", exist_ok=True)

    pipe = StableDiffusion3Pipeline.from_pretrained("stabilityai/stable-diffusion-3-medium-diffusers", torch_dtype=torch.float16)
    pipe = pipe.to("cuda")

    for i in range(len(ImgR)):
        image = pipe(
            ImgR[i],
            negative_prompt="",
            num_inference_steps=28,
            guidance_scale=7.0,
        ).images[0]
        os.save
