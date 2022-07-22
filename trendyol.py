from requests import get
from bs4 import BeautifulSoup
from pandas import DataFrame, concat
from time import sleep

print("""required libraries:
requests
bs4
pandas
""")

url = input("Enter URL: ")
page_num = int(input("Enter how many pages you want to scrape (integer): "))
time = float(input("Enter how many seconds to sleep between GET requests (float): "))

if "?pi=" in url:
    url = url[:url.find("?pi=")]

table = DataFrame(columns=("brand","model","price"))
for rep in range(1, page_num + 1):
    soup = BeautifulSoup(get(url + "?pi=" + str(rep)).content, "html.parser")
    products = soup.find("div", {"class" : "prdct-cntnr-wrppr"}).find_all("div", {"class" : "prdct-desc-cntnr-wrppr"})
    for num, value in enumerate(products):
        brand = value.find("span", {"class":"prdct-desc-cntnr-ttl"}).text
        model = value.find("span", {"class":"prdct-desc-cntnr-name"}).text
        price = value.find("div", {"class":"prc-box-dscntd"}).text
        table = concat([table, DataFrame([[brand, model, price]], columns=("brand","model","price"))])
    print("Page " + str(rep))
    sleep(time)

print("All pages are scrapped")

table = table.reset_index()
table.to_csv("trendyol.csv")

print("CSV file is created")
input("Please Enter to Exit...")
