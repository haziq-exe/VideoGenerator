from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Prompts import DrugPrompt
import time


def FetchStory(prompt_type = "Drug", numberofposts=2):

    chromedriver_path = '/Users/haziq/Desktop/TikTokGenerator/chromedriver/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--no-sandbox')

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)


    Script = []
    Title = []
    for i in range(numberofposts):
        ScriptTemp = []

        if prompt_type == "Drug":
            prompt_type = DrugPrompt

        # Open the website
        driver.get('https://toolbaz.com/writer/ai-story-generator')

        WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located((By.TAG_NAME, 'textarea'))
        ) 

        # Find the <textarea> element and enter the text
        textarea = driver.find_element(By.TAG_NAME, 'textarea')
        textarea.click()
        textarea.send_keys(DrugPrompt)

        # Find the button with id="main_btn" and click it
        submit_button = driver.find_element(By.ID, 'main_btn')
        driver.execute_script("arguments[0].scrollIntoView();", submit_button)
        submit_button.click()

        # Wait for the response to be generated (adjust the time as needed)
        time.sleep(10)  # Adjust sleep time based on website's response time

        # Find all <p> tags containing the response
        output_div = driver.find_element(By.ID, 'output')
        p_tags = output_div.find_elements(By.TAG_NAME, 'p')

        # Extract and print the text from <p> tags
        responses = [p.text for p in p_tags]
        for response in responses:
            ScriptTemp.append(response)

        driver.quit()

        Script = " ".join(ScriptTemp)
        Title = ScriptTemp[0]
        print(Script, Title)
        ScriptTemp.clear()

        return Script, Title



FetchStory(numberofposts=1)