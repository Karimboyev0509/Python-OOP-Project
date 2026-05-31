import requests
import csv 
from bs4 import BeautifulSoup
import json
import logging
import time
from abc import ABC, abstractmethod

logging.basicConfig(filename="log.txt", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def retry(function):
    def wrapper(*args, **kwargs):
        attempts = 3
        for i in range(attempts):
            try:
                return function(*args, **kwargs)
            except requests.exceptions.RequestException as e:
                logging.error(f"Retry {i+1}: {e}")

                print(f"Retrying...{i+1}")
                time.sleep(2) 
            
        print("Failed after retries")

    return wrapper

class Scraper(ABC):
    def __init__(self, url):
        self.url = url
        self.data = []

    @abstractmethod
    def scrape(self):
        pass

    def save_csv(self):
        with open("data.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Title"])
            for item in self.data:
                writer.writerow([item])

        print("Csv saved")

    def save_json(self):
        with open("data.json", "w") as file:
            json.dump(self.data, file, indent=4)

        print("Json saved")

class NewScraper(Scraper):
    @retry
    def scrape(self):
        logging.info("NewScrapper Started")
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "lxml")
        headlines = soup.find_all("h2")
        for headline in headlines:
            text = headline.text.strip()
            self.data.append(text)

        logging.info("Newscrapper Finished")
        return self.data
    
class ProductScraper(Scraper):

    @retry
    def scrape(self):
        logging.info("ProductScraper Started")
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "lxml")
        products = soup.find_all("h2")
        for product in products:
            self.data.append(product.text.strip())

        logging.info("ProductScraper Finished")
        return self.data


class SocialScraper(Scraper):

    @retry
    def scrape(self):
        logging.info("SocialScraper Started")
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "lxml")

        posts = soup.find_all("p")
        for post in posts:

            self.data.append(post.text.strip())
        logging.info("SocialScraper Finished")

        return self.data


class DataCleaner:

    def clean_text(self, text):
       text = text.lower()
       text = text.replace("\n", "")
       text = text.strip()

       return text

    def clean_data(self, data):
        cleaned = []
        for item in data:
            cleaned.append(self.clean_text(item))

        return cleaned
    

class CLI:

    def __init__(self):

        self.scraper = None

    def run(self):

        while True:

            print("\n1. News Scraper")
            print("2. Product Scraper")
            print("3. Social Scraper")
            print("4. Exit")

            choice = input("Choose: ")


            if choice == "1":

                url = input("News URL: ")

                self.scraper = NewScraper(url)

                data = self.scraper.scrape()
                print(data)



            elif choice == "2":

                url = input("Product URL: ")

                self.scraper = ProductScraper(url)

                data = self.scraper.scrape()

                print(data)


            elif choice == "3":

                url = input("Social URL: ")

                self.scraper = SocialScraper(url)

                data = self.scraper.scrape()

                print(data)


            elif choice == "4":
                break


cli = CLI()
cli.run()

