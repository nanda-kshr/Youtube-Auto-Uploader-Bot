#from selenium.webdriver.common.by import By
from time import sleep
from dotenv import load_dotenv
import os
from config.constants import pixabay_url, i_save_path, a_save_path, parent_path, v_save_path, driver_path
import requests
from PIL import Image
#from pydub import AudioSegment
from io import BytesIO
from mutagen.mp3 import MP3
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import json
import time
import librosa

from mutagen.id3 import ID3
class BotLogic:
    def __init__(self):
        load_dotenv()
        self.image_url = pixabay_url
        self.API_KEY = os.getenv("PIXABAY_API_KEY")
        self.TTS_API_KEY = os.getenv("TTS_API_KEY")
        self.driver = None 

    def login(self, username, password):
        self.browser.get("https://example.com/login")
        sleep(2)
        self.browser.find_element(By.NAME, "username").send_keys(username)
        self.browser.find_element(By.NAME, "password").send_keys(password)
        self.browser.find_element(By.NAME, "submit").click()

    def get_image_with_keyword(self, topic, no_of_imgs):
        params = {
            "key": self.API_KEY,
            "q": topic, 
            "lang": "en", 
            "image_type": "illustration",           
            "category": "science,nature,computer", 
            "colors": "blue,gray,white",  
            "editors_choice": "true",     
            "safesearch": "true",         
            "order": "popular",           
            "per_page": 10
        }
        def req_images():
            return requests.get(self.image_url, params=params)
        
        response = req_images()
        images = []
        if response.status_code == 200:
            data = response.json()
            data =  data["hits"]
            if data == [] or len(data) < no_of_imgs:
                params["image_type"] = "photos"
                del params["colors"]
                del params["order"]
                del params["category"]
                response = req_images()
                imgs = response.json()
                for img in imgs["hits"]:
                    data.append(img)
            if data == [] or len(data) < no_of_imgs:
                del params["lang"]
                del params["editors_choice"]
                response = req_images()
                imgs = response.json()
                for img in imgs["hits"]:
                    data.append(img)
            for i in  range(0,no_of_imgs):
                image_url_from_response = data[i]["largeImageURL"]
                response = requests.get(image_url_from_response, stream=True)
                image_full_path = i_save_path + topic+ str(i) +".jpg"
                img = Image.open(BytesIO(response.content)).convert("RGB")
                original_width, original_height = img.size
                target_ratio=(9, 16)
                target_width = 720
                target_height = 1280
                if target_height > original_height:
                    target_height = original_height
                    target_width = int(original_height * target_ratio[0] / target_ratio[1])
                left = (original_width - target_width) // 2
                top = (original_height - target_height) // 2
                right = left + target_width
                bottom = top + target_height
                cropped_img = img.crop((left, top, right, bottom))
                cropped_img.save(image_full_path)
                images.append(image_full_path)
            return images
        else:
            print(f"Error: {response.status_code}, {response.text}")
    
    def get_audio(self, topic, problem):
        headers = {
            "Content-Type": "application/json",
            "xi-api-key": self.TTS_API_KEY
        }
        url = f"https://api.elevenlabs.io/v1/text-to-speech/9BWtsMINqrJLrRacOk9x"
        payload = {
            "text": problem,
            "model_id": "eleven_turbo_v2"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            audio_path = a_save_path + topic+".mp3"
            with open(audio_path, "wb") as audio_file:
                audio_file.write(response.content)
            audio_data, sample_rate = librosa.load(audio_path)
            duration = librosa.get_duration(y=audio_data, sr=sample_rate)
            return audio_path, duration

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return {"status": "error", "error": str(e)}

    def make_video(self, topic, problem, audio, images, image_durations):
        video_clips = []       
        def normalize_image(image_path, target_resolution=(720, 1280)):
            img = Image.open(image_path).convert("RGB")
            img = img.resize(target_resolution)
            img.save(image_path)
        for i, image in enumerate(images):
            normalize_image(image)
            clip = ImageClip(image, duration=image_durations[i]).on_color(color=(0, 0, 0), col_opacity=1)
            video_clips.append(clip) 
        video = concatenate_videoclips(video_clips, method="compose")
        audio = AudioFileClip(audio)
        video = video.set_audio(audio)      
        output_file = v_save_path+topic+".mp4"
        video.write_videofile(output_file, fps=24, codec="libx264", audio_codec="aac", threads=4, preset="ultrafast")
        return output_file

    def upload_video(self, problem, video):
        self.driver.get("https://studio.youtube.com/channel/UCFalnaqk9Hw9_iPytBtjxww/videos?d=ud")
        time.sleep(5)
        file_input = self.driver.find_element(By.XPATH, "//input[@type='file']")
        time.sleep(3)
        file_input.send_keys(parent_path+video)
        time.sleep(3)
        set_title = self.driver.find_element(By.XPATH, "//div[@contenteditable='true']") 
        set_title.send_keys(problem)
        time.sleep(1)
        radio_button = self.driver.find_element(By.XPATH, "//tp-yt-paper-radio-button[@name='VIDEO_MADE_FOR_KIDS_NOT_MFK']//div[@id='radioContainer']")
        radio_button.click()
        time.sleep(1)
        next_button = self.driver.find_element(By.XPATH, '//*[@id="next-button"]/ytcp-button-shape/button')
        next_button.click()
        time.sleep(1)
        next_button = self.driver.find_element(By.XPATH, '//*[@id="next-button"]/ytcp-button-shape/button')
        next_button.click()
        time.sleep(1)
        next_button = self.driver.find_element(By.XPATH, '//*[@id="next-button"]/ytcp-button-shape/button')
        next_button.click()
        time.sleep(1)
        public_radio_button = self.driver.find_element(By.XPATH, "//tp-yt-paper-radio-button//div[text()='Public']")
        public_radio_button.click() 
        time.sleep(1)
        publish_button = self.driver.find_element(By.XPATH, '//*[@id="done-button"]/ytcp-button-shape/button')
        publish_button.click()
        time.sleep(30)

    
    def setup(self, cookies_file):
        def load_cookies(cookies_file):
            with open(cookies_file, "r") as file:
                cookies = json.load(file)
                for cookie in cookies:
                    if "sameSite" in cookie and cookie["sameSite"] == "no_restriction":
                        cookie["sameSite"] = None
                    self.driver.add_cookie(cookie)
        chrome_service = Service("/Users/nandakishore/Documents/work/auto_yt_poster/chromedriver")
        self.driver = webdriver.Chrome(service=chrome_service)
        self.driver.get("https://youtube.com")
        load_cookies("config/cookies.json")
        self.driver.get("https://studio.youtube.com/channel/UCFalnaqk9Hw9_iPytBtjxww/videos?d=ud")

        

