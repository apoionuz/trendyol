#!/usr/bin/python

from requests import get
from bs4 import BeautifulSoup
from pandas import DataFrame, concat
import threading
import time


class TrendyolScrapper:
    def __init__(self):
        self.page_table = DataFrame(columns=("brand", "model", "price"))

    def download_pages(self, page_url: str, page_count: int):
        threads = []

        try:
            for page_index in range(1, page_count + 1):
                threads.append(threading.Thread(target=self.download_page, args=(page_url, page_index,)))
        except:
            print("Unable to create threads")

        try:
            for thread in threads:
                thread.start()
        except:
            print("Unable to start threads")

        try:
            for thread in threads:
                thread.join()
        except:
            print("Unable to join threads")

    def download_page(self, page_url: str, page_index: int):
        raw_page = get(page_url + "?pi=" + str(page_index))
        soup = BeautifulSoup(raw_page.content, "html.parser")

        products = soup \
            .find("div", {"class": "prdct-cntnr-wrppr"}) \
            .find_all("div", {"class": "prdct-desc-cntnr-wrppr"})

        for num, value in enumerate(products):
            brand = value.find("span", {"class": "prdct-desc-cntnr-ttl"}).text
            model = value.find("span", {"class": "prdct-desc-cntnr-name"}).text
            price = value.find("div", {"class": "prc-box-dscntd"}).text
            self.page_table = concat([self.page_table, DataFrame([[brand, model, price]],
                                                             columns=("brand", "model", "price"))])

    def save(self):
        self.page_table = self.page_table.reset_index()
        self.page_table.to_csv("trendyol.csv")


if __name__ == "__main__":
    page_url = input("Enter Product Url: ")
    page_num = int(input("Enter how many pages of data you want (integer): "))

    scrapper = TrendyolScrapper()
    scrapper.download_pages(page_url, page_num)
    scrapper.save()

    print("Csv file is created")
    input("Please Enter to Exit...")
