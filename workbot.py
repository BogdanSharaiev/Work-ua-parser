import requests
from bs4 import BeautifulSoup
import time
import telebot
bot_token = '7295767226:AAE7PxwYrCyjHAoBRlctG-uPzgiypAyNNAY'
channel_username = '@UAWorkHelper'

url = f'https://api.telegram.org/bot{bot_token}/getChat?chat_id={channel_username}'

response = requests.get(url)
data = response.json()
print(data)
chat_id = -1002160501617

TOKEN = "7295767226:AAE7PxwYrCyjHAoBRlctG-uPzgiypAyNNAY"
bot = telebot.TeleBot(TOKEN)
def get_info(job_cards):
    for el in job_cards:
        # Extract job name
        name_tag = el.find('h2', class_="my-0")
        name = name_tag.text.strip() if name_tag else "No job name found"
        a = name_tag.find('a')
        url = "https://work.ua" + a.get("href")
        # Extract company name
        company_tag = el.find('div', class_="mt-xs")
        if company_tag:
            company_name_tag = company_tag.find('span', class_="strong-600")
            company = company_name_tag.text.strip() if company_name_tag else "No company name found"
        else:
            company = "No company tag found"

        # Extract salary
        salary_tag = el.find('span', class_="strong-600")
        if salary_tag:
            salary_text = salary_tag.text.strip()
            # Check if the first two characters are digits to determine if it's a salary
            if len(salary_text) >= 2 and salary_text[0].isdigit() and salary_text[1].isdigit():
                salary = salary_text
            else:
                salary = "None"
        else:
            salary = "None"
        time = el.find('time')
        if time:
            time = time.text.strip()
        else:
            time = " "
        # Print job details
        result = "Name: " + name + "\n" + "Company: " + company + "\n" + "Salary: " + salary + "\n" + "Time: " + time + "\n" + "Url: " + url
        bot.send_message(chat_id,result)
# URL to scrape

def work(link):
    # Headers with User-Agent
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }

    # Sending the request
    response = requests.get(link, headers=headers)

    # Parse the response content
    soup = BeautifulSoup(response.text, 'lxml')

    # Find all job cards
    job_cards_alt = soup.find_all('div', class_="card card-hover card-search card-visited wordwrap job-link js-job-link-blank js-hot-block")
    get_info(job_cards_alt)
    job_cards = soup.find_all('div', class_="card card-hover card-search card-visited wordwrap job-link js-job-link-blank")
    get_info(job_cards)

#link = "https://www.work.ua/jobs-remote-industry-it/?student=1&days=122"
#link = "https://www.work.ua/jobs-odesa/"
link = "https://www.work.ua/jobs-kyiv-it/?student=1"
while True:
    work(link)
    time.sleep(3600)