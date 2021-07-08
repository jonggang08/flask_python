import requests
from bs4 import BeautifulSoup

def get_last_page(url):
  result = requests.get(url)
  soup = BeautifulSoup(result.text, "html.parser")
  pages= soup.find("div", {"class":"s-pagination"}).find_all("a")
  last_page = pages[-2].get_text(strip=True) #-1 is the next button and -2 is the largest button #.string will give you none 
  return int(last_page)

def extract_job(html):
  title = html.find("h2", {"class": "mb4"}).find("a")["title"]
  company, location = html.find("h3", {"class": "fc-black-700"}).find_all("span", recursive = False) #recursive makes sure finding of span doesnt go deep (첫단계인 span만 가져오기)
  company = company.get_text(strip=True)
  
  location = location.get_text(strip=True)
  job_id=html['data-jobid']
  return {'title': title, 'Company': company, 'Location': location, "apply_link": f"https://stackoverflow.com/jobs/{job_id}"}

def extract_jobs(last_page, url):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping SO: Page: {page}")
    result = requests.get(f"{url}&pg={page+1}") 
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class":"-job"}) #find class
    for result in results:
      job = extract_job(result)
      #print(job)(to check everything works)
      jobs.append(job)
  return jobs

def get_jobs(word):
  url = f"https://stackoverflow.com/jobs?q={word}"
  last_page = get_last_page(url)
  jobs = extract_jobs(last_page,url)
  return jobs

def get_info(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    joblist=[]
    rows = soup.find_all("div",{"class":"item_recruit"})
    for row in rows:
        title = row.find("a")["title"]
        loc = row.find("div",{"class":"job_condition"}).find("span").text
        date = row.find("div",{"class":"job_date"}).find("span").text
        jobinfo = {"title":title, "location":loc, "Date":date}
        joblist.append(jobinfo)
    return joblist

def get_infos(word):
    jobs=[]
    for page in range(1,9):
        result = get_info(f"https://www.saramin.co.kr/zf_user/search/recruit?&searchword={word}&recruitPage={page}")
        jobs.append(result)
    return jobs