import requests
from bs4 import BeautifulSoup

ITEMS = 100
URL = f'https://hh.ru/search/vacancy?&st=searchVacancy&text=%D1%82%D0%B5%D1%85%D0%BD%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9+%D1%8D%D0%BB%D0%B5%D0%BA%D1%82%D1%80%D0%BE%D0%BD%D0%BD%D1%8B%D0%B9+%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%BE%D0%B1%D0%BE%D1%80%D0%BE%D1%82&industry=13&industry=47&items_on_page={ITEMS}'

headers = {
    "Host": "hh.ru",
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Accept":
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,ru-RU;q=0.8,ru;q=0.5,en;q=0.3",
    "Connection": "keep-alive"
}


def extract_max_page():
    hh_request = requests.get(URL, headers=headers)
    hh_soup = BeautifulSoup(hh_request.text, "html.parser")
    pages = []
    paginator = hh_soup.find_all("span",{"class": "pager-item-not-in-short-range"})
    for page in paginator:
        pages.append(int(page.find("a").text))
    print("Всего страниц", pages[-1])
    return pages[-1]


def extract_job(html):
    title = html.find('a').text
    link = html.find('a')["href"]

    company = html.find('div', {
        "class": "vacancy-serp-item__meta-info-company"
    }).text
    company_link_raw = html.find('div', {
        "class": "vacancy-serp-item__meta-info-company"
    }).find('a')["href"]
    company_link = f'https://hh.ru{company_link_raw}'
    company = company.strip()
    #location = location.partition(",")[0]
    company_www = extract_www (company_link)
    return {
        "title": title,
        "company": company,
        'company_www':company_www,
        #"location": location,
        "link": link   
    }

def extract_www(www):
  www_request = requests.get(www, headers=headers)
  soup = BeautifulSoup(www_request.text, "html.parser")
  company_www = soup.find("div",{"class": "employer-sidebar-content"})
  if company_www is None:
    return None
  else:
    company_www = company_www.find('a').text
  return  company_www

def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"HH парсинг страницы {page}")
        result = requests.get(f'{URL}&page={page}', headers=headers).text
        #print (result)
        soup = BeautifulSoup(result, "html.parser")
        results = soup.find_all("div", {"class": "vacancy-serp-item"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    max_page = extract_max_page()
    jobs = extract_jobs(max_page)
    return jobs
