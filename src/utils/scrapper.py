import os
import selenium
from selenium import webdriver
import time
from PIL import Image
import io
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from uuid import uuid4


class ImageScrapper:
    def __init__(self, search_term, output_folder):
        self.search_term = search_term
        self.output_path = os.path.join(os.getcwd(), output_folder)
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.search_url = 'https://www.google.com/search?q={q}&tbm=isch&ved=2ahUKEwjw0eiunsv9AhWLuKQKHQz0Au4Q2-cCegQIABAA&oq=phone+number&gs_lcp=CgNpbWcQAzIECAAQQzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABFAAWABgxgVoAHAAeACAAbACiAGwApIBAzMtMZgBAKoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=VOwHZPDXFYvxkgWM6IvwDg&bih=947&biw=1920&client=firefox-b-d'
        self.driver.get(self.search_url.format(q=search_term))
        self.img_urls = set()

    def __scroll_to_end(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        # Locate the images to be scraped from the current page
        img_results = self.driver.find_elements(By.XPATH, "//img[contains(@class,'Q4LuWd')]")
        total_results = len(img_results)

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

    def __save_image(self, url):
        file_name = f"{str(uuid4())}-scraped.jpg"
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
        except Exception as e:
            print(f"ERROR - COULD NOT SAVE {url} - {e}")

    def scrape(self):
        try:
            self.__scroll_to_end()
        finally:
            if len(self.img_urls):
                print("no images found to download try again")
                return
            os.makedirs(self.output_path)
            for url in self.img_urls:
                self.__save_image(url)
