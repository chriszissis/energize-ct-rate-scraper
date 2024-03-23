#Scraper
import requests
import time
from bs4 import BeautifulSoup
from discord import SyncWebhook

# Use selenium to get page after JS has actually modified page
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


dict = {}

# energize CT URL
URL = "https://energizect.com/rate-board/compare-energy-supplier-rates?customerClass=1201&monthlyUsage=750&planTypeEdc=1191"

# Set options for selenium and scrape page
options = Options()
options.add_argument("--headless=new") #headless so we dont see the browser window
driver = webdriver.Chrome(options=options)
driver.get(URL)

time.sleep(2) #wait for the JS to actually do its thing

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.close()

all_list_items = soup.find_all(class_="list-item__content")

text = "Offer Rate"
text2 = "Plan Description"

# loop over all divs container supplier info
for divs in all_list_items:
    suppliername_container = divs.find(class_="list-item__title")
    suppliername = suppliername_container.next_element.next_element
    
    pricetag = divs.find(lambda tag: tag.name == "p" and text in tag.text)
    price = pricetag.next_sibling

    term_container = divs.find("p", string="Plan Description")
    term_type = term_container.next_sibling
    term_duration = term_container.next_sibling.next_sibling.next_sibling

    suppliername_formatted = suppliername.strip() + " - Term: " + term_type + " - Term Length: " + term_duration
    dict[suppliername_formatted] = float(price.replace('₵ per kWh', ''))
    

lowest_options = {k: v for k, v in dict.items() if v == min(dict.values())}

formatted_output = "**The lowest rate(s) is/are:** \n" + str(lowest_options)

#send to discord
#webhook = SyncWebhook.from_url("https://discordapp.com/api/webhooks/1220172794051170444/JIK4F1wuWzSlBEIfL6Ue3WNmJxwSLksvOjfaY7kDxPJ5z7cPzMlxoB86a9K5OBcxxFiw")
webhook = SyncWebhook.from_url("https://discordapp.com/api/webhooks/1220550641043378176/b8q4jrtB4AUtfxrHdive8gjbBvOYHeiRDMcfL4im_6GK9NZuL3ezmQ7e-hiVljDtQ5g3")
webhook.send(formatted_output)



