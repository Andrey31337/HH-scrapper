import requests
from bs4 import BeautifulSoup

URL = 'https://stackoverflow.com/jobs?q=system+anlysys'

def extract_max_page():
  request = requests.get(URL)
  soup = BeautifulSoup(request.text,"html.parser")
  pages = soup.find("div",{"class":"s-pagination"}).find_all("a")
  last_page = int(pages [-2].get_text(strip=True))
  return last_page


def extract_job(html):
  title= html.find('h2').find('a').text
  company_raw = html.find('h3').find_all('span',reqursive= False)
  company = company_raw[0].get_text(strip=True)
  location = company_raw[1].get_text(strip=True)
  job_id = html['data-jobid']
  link = f'https://stackoverflow.com/jobs?id={job_id}'

  return {'title': title, 'company':company , 'location': location, 'link': link}

 
def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"SO парсинг страницы {page}")
    result = requests.get(f'{URL}&page{page+1}')
    soup = BeautifulSoup(result.text,"html.parser")
    results = soup.find_all('div', {'class':'-job'})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs

def get_jobs():
    max_page = extract_max_page()
    jobs = extract_jobs(max_page)
    return jobs 
