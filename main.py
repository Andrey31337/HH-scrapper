import requests
from bs4 import BeautifulSoup
import lxml
import random
import re
from time import sleep
import csv

with open('test.csv',mode='w',encoding="cp1251") as file:
  writer = csv.writer(file,delimiter="|")
  writer.writerow (['link','title'])

NoneType = type(None)

hh_text = '(разработчик+or+developer)+and+(github.com+or+github.io+or+linkedin.com+or+%2B79+or+%2B37+or+Резюме+or+t.me+or+%40)'

URL = f'https://hh.ru/search/resume?logic=normal&pos=full_text&exp_period=all_time&text={hh_text}'

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

hh_request = requests.get(URL, headers=headers)
hh_soup = BeautifulSoup(hh_request.text,"lxml")


#Узнаем количество страниц с резюме
def extract_max_page():
  hh_request = requests.get(URL, headers=headers)
  hh_soup = BeautifulSoup(hh_request.text, "lxml")
  pages = []
  paginator = hh_soup.find_all("span",
                                 {"class": "pager-item-not-in-short-range"})
  for page in paginator:
    pages.append(int(page.find("a").text))
  return pages[-1]

#max_page = extract_max_page()
#Заглушка для max_page
max_page=40
#print(max_page)
#print(URL)

# собираем ссылки на резюме в list
def extract_resume_links(max_page):
  resume_list = []
  for page in range(max_page):
    print(f"HH парсинг страницы {page}")
    result = requests.get(f'{URL}&page={page}',headers=headers).text
    soup = BeautifulSoup(result, "lxml")
    results = soup.find_all("span", {"class": "bloko-header-section-3","data-qa":"bloko-header-3"})
    for item in results:
      tag_a =item.find("a")
      link_raw = tag_a.get('href')
      link = link_raw.rpartition('?')[0] 
      resume_link=f'https://hh.ru{link}'
      resume_list.append(resume_link)
      sleep(random.randrange(2, 4))
  return resume_list

resume_list = extract_resume_links(max_page)


for resume in resume_list:
  print("ССЫЛКА ",resume)
  r_request = requests.get(resume, headers=headers)
  r_soup = BeautifulSoup(r_request .text,"lxml")
  
  #Собираем название резюме
  title = r_soup.find("div",{"class":"bloko-column bloko-column_xs-4 bloko-column_s-5 bloko-column_m-6 bloko-column_l-9"}).find("span",{"data-qa":"resume-block-title-position"})
  if type(title) == NoneType:
    sleep(random.randrange(2, 4))
  else:
    title=title.text
  #sleep(random.randrange(2, 4))

  #Собираем из резюме компании должности, универ,курсы
  сompanys = r_soup.find_all("div",{"class":"bloko-column bloko-column_xs-4 bloko-column_s-6 bloko-column_m-7 bloko-column_l-10"})
  work_list = []
  for block in сompanys:
    work = block.find("span",{"class":"resume-block-container"})
    works = block.find_all("div",{"class":"bloko-text bloko-text_strong"})
    if type(works) == NoneType:
      sleep(random.randrange(2, 4))
    else:
      for work in works:
        company_text = work.text
        work_list.append(company_text)
  #sleep(random.randrange(2, 4))
  #собираем обо мне для последующего разбора
  resume_body = r_soup.find("div",{"class":"bloko-column bloko-column_container bloko-column_xs-4 bloko-column_s-8 bloko-column_m-9 bloko-column_l-12"}).find("div",{"class":"bloko-gap bloko-gap_top"}).find("div",{"class":"resume-block-container","data-qa":"resume-block-skills-content"})
  if type(resume_body) == NoneType:
    sleep(random.randrange(2, 4))
  else:
    resume_body=resume_body.text
    regularemail = r"[\w.-]+@[a-zA-Z.-]+"
    regulargit = r"[\w.-:/]+git[a-zA-Z0-9.-/]+"
    regulattelega =r"[\w.-:/]+t.me/[a-zA-Z0-9.-/]+"
    regularlogins = r"[@]+[a-zA-Z_.]+"
    regularlinked = r"[\w.-:/]+linked[a-zA-Z0-9-.-/%]+"
    regulartel =r"(?:\+|\d)[\d\-\(\) ]{9,}\d"
    email = re.findall(regularemail,resume_body)
    git = re.findall(regulargit,resume_body)
    logins = re.findall(regularlogins,resume_body)
    linked = re.findall(regularlinked,resume_body)
    tel = re.findall(regulartel,resume_body)
    telega = re.findall(regulattelega,resume_body)


  #sleep(random.randrange(2, 4))
  #Собираем из резюме возраст
  age = r_soup.find("div",{"class":"resume-header-title"}).find("span",{"data-qa":"resume-personal-birthday"}) 
  if type(age) == NoneType:
    sleep(random.randrange(2, 4))
  else:
      age = age.text

  #sleep(random.randrange(2, 4))
  #Собираем теги
  tags = r_soup.find("div",{"class":"bloko-tag-list"})
 #здесь ошибка
  if type(tags) == NoneType:
    sleep(random.randrange(2, 4))
  else:
    tags=tags.find_all("span")
    if type(tags) == NoneType:
      sleep(random.randrange(2, 4))
    else:
      tags_list=[] 
      for tag in tags:
        tag = tag.text
        tags_list.append(tag)

  #sleep(random.randrange(2, 4))

  #Собираем из резюме универ
  edu = r_soup.find("div",{"class":"bloko-text bloko-text_strong","data-qa":"resume-block-education-name"})
  if type(edu) == NoneType:
    sleep(random.randrange(2, 4))
  else:
    edu=edu.find("a")
    if type(edu) == NoneType:
      sleep(random.randrange(2, 4))
    else:
      edu=edu.text 
  #sleep(random.randrange(2, 4))     
 
 
  #Собираем зп резюме
  salary = r_soup.find("span",class_="resume-block__salary resume-block__title-text_salary")
  if type(salary) == NoneType:
    sleep(random.randrange(2, 4))
  else:
    salary=salary.text    
  #sleep(random.randrange(2, 4))

  #Собираем город проживания 
  city = r_soup.find("span",{"data-qa":"resume-personal-address"})
  if type(city) == NoneType:
    sleep(random.randrange(2, 4))
  else:
    city=city.text    
  #sleep(random.randrange(2, 4))

  #Подготавливаем данные для CSV
  csv_result=[]
  csv_result=[resume,title,city,salary,age,work_list,edu,tags_list,email,git,logins,linked,tel,telega]
  #print(csv_result)

  #Подготавливаем записываем данные в файл
  with open('test.csv',mode='a') as file:
    writer = csv.writer(file,delimiter="|")
    writer.writerow (csv_result)