import time
import pandas as pd
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from fake_useragent import UserAgent
from logger_func import logger

class sutochno_parser():
    @logger
    def __init__(self):
        options = webdriver.ChromeOptions()

        options.add_argument('--log-level=3') 
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')

        ua = UserAgent()
        options.add_argument(f'user-agent={ua.random}')
        options.add_argument('--proxy-server=120.232.115.57:17981')

        # --- ОТКЛЮЧАЕМ КАРТИНКИ ДЛЯ ЭКОНОМИИ ВРЕМЕНИ (скопировал с ии, но тема вполне полезная)---
        prefs = {
            # 2 — это режим "блокировать". Блокируем картинки
            "profile.managed_default_content_settings.images": 2,
        }
        options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(options=options)

        self.links_list = []
        self.info_list = []
        self.driver.get('https://sutochno.ru/front/searchapp/search?guests_adults=1&occupied=2026-10-30;2026-10-31&term=%D0%9A%D0%B0%D0%BC%D1%87%D0%B0%D1%82%D1%81%D0%BA%D0%B8%D0%B9+%D0%BA%D1%80%D0%B0%D0%B9&SW.lat=48.695403231714&SW.lng=152.05073012499992&NE.lat=66.24193467093268&NE.lng=177.89057387499994&id=19851&type=region&price&price&is_apartment=1')

    @logger
    def accept_cookies(self):
        clickable_element = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.ID, "modal-cookies-accept"))
        )
        clickable_element.click()
        return "Файлы куки приняты успешно"

    @logger
    def get_links_on_the_page(self):

        #контрим ленивую подгрузку
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.card-content'))
        )
        

        self.driver.execute_script("window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });")
        
        # Даем бесплатному прокси и скроллу 2 секунды доехать до низа и прогрузить верстку
        time.sleep(2)


        elements = self.driver.find_elements(By.CSS_SELECTOR, "a.card-content")

        for element in elements:
            self.links_list.append(element.get_attribute('href'))
        return f"Ссылки со страницы собраны успешно. Ссылок в списке: {len(self.links_list)}"

    @logger
    def go_to_the_next_page(self):
        selector = "ul > li.navigation:last-child div.pagination-arrow"
        
        try:
            clickable_element = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            self.driver.execute_script("arguments[0].click();", clickable_element)

            return "Переход на следующую страницу совершен успешно"
            
        except TimeoutException:
            return False

    @logger
    def get_info(self):
        for link in self.links_list:
            self.driver.get(link)

            time.sleep(2)

            #section-aside > aside > div > div.sc-detail-aside-price > div > span.sc-detail-aside-price__cost
            price_element = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#section-aside > aside > div > div.sc-detail-aside-price > div > span.sc-detail-aside-price__cost"))
            )

            elements = self.driver.find_elements(By.CSS_SELECTOR, "span.sc-detail-params__item")

            guest = "N/A"
            bed = "N/A"
            room = "N/A"
            k = 0
            for el in elements:
                text = el.text.lower()
                if "гост" in text:
                    digits = "".join(char for char in el.text if char.isdigit())
                    guest = int(digits) if digits else 0
                    k+=1
                elif "кроват" in text:
                    digits = "".join(char for char in el.text if char.isdigit())
                    bed = int(digits) if digits else 0
                    k+=1
                elif "спальн" in text:
                    digits = "".join(char for char in el.text if char.isdigit())
                    room = int(digits) if digits else 0
                    k+=1
                if k == 3:
                    break

            #  span.sc-detail-map__location
            address_element = self.driver.find_element(By.CSS_SELECTOR, "span.sc-detail-map__location-address")
            address = address_element.text.strip()

            #section-aside > aside > div > div.sc-detail-aside-price > div > span.sc-detail-aside-price__cost
            price_clean = "".join(char for char in price_element.text if char.isdigit())
            price = int(price_clean) if price_clean else 0

            self.info_list.append({
                "Адрес" : address,
                "RUB/сут." : price,
                "Кол-во гостей" : guest, 
                "Кол-во спален" : room,
                "Кол-во кроватей" : bed, 
                "Ссылка" : link
            })
        return f"Информация из каждой ссылки успешно собрана в список словарей. Словарей: {len(self.info_list)}"

    @logger
    def to_csv(self):
        df = pd.DataFrame(self.info_list)
        df.to_csv("sutochno_results.csv", index=False, encoding="utf-8-sig", sep=";")

        return("Информация успешно переведена в csv")
