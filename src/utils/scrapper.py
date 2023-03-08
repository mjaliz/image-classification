import io
import os
import time
from uuid import uuid4

import pandas as pd
import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class ImageScrapper:
    def __init__(self, search_term, output_folder):
        self.search_term = search_term
        self.output_path = os.path.join(os.getcwd(), output_folder)
        opts = webdriver.ChromeOptions()
        opts.headless = True
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),options=opts)
        self.search_url = 'https://www.google.com/search?q={q}&tbm=isch&ved=2ahUKEwjw0eiunsv9AhWLuKQKHQz0Au4Q2-cCegQIABAA&oq=phone+number&gs_lcp=CgNpbWcQAzIECAAQQzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABFAAWABgxgVoAHAAeACAAbACiAGwApIBAzMtMZgBAKoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=VOwHZPDXFYvxkgWM6IvwDg&bih=947&biw=1920&client=firefox-b-d'
        self.driver.get(self.search_url.format(q=search_term))
        self.img_urls = set()

    def __scroll_to_end(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        # Locate the images to be scraped from the current page
        img_results = self.driver.find_elements(By.XPATH, "//img[contains(@class,'Q4LuWd')]")
        total_results = len(img_results)
        print(f"{total_results} images found searching for urls...")

        try:
            for i in range(0, len(img_results)):
                img = img_results[i]
                try:
                    img.click()
                    time.sleep(2)
                    actual_images = self.driver.find_elements(By.CSS_SELECTOR, 'img.n3VNCb')
                    for actual_image in actual_images:
                        if actual_image.get_attribute('src') and 'https' in actual_image.get_attribute('src'):
                            img_url = actual_image.get_attribute('src')
                            self.img_urls.add(img_url)
                except:
                    print("err")
        finally:
            print(f"{i} urls found going to download....")

    def __save_image(self, url):
        images_list = []
        with open('downloaded.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                images_list.append(line.strip("\n"))
        file_name = f"{str(uuid4())}-scraped.jpg"
        if not os.path.isfile(os.path.join(self.output_path, file_name)) and url not in images_list:
            try:
                image_content = requests.get(url).content

            except Exception as e:
                print(f"ERROR - COULD NOT DOWNLOAD {url} - {e}")

            try:
                image_file = io.BytesIO(image_content)
                image = Image.open(image_file).convert('RGB')

                file_path = os.path.join(self.output_path, file_name)

                with open(file_path, 'wb') as f:
                    image.save(f, "JPEG", quality=85)

                print(f"SAVED - {url} - AT: {file_path}")
                with open('downloaded.txt', 'a') as f:
                    f.write(f'{url}\n')
            except Exception as e:
                print(f"ERROR - COULD NOT SAVE {url} - {e}")

    def __save_url(self, url):
        with open('urls.txt', 'a') as f:
            f.write(f'{url}\n')

    def scrape(self):
        try:
            self.__scroll_to_end()
        finally:
            if len(self.img_urls) == 0:
                print("no images found to download try again")
                return
            if not os.path.isdir(self.output_path):
                os.makedirs(self.output_path)
            for url in self.img_urls:
                self.__save_url(url)
                self.__save_image(url)
