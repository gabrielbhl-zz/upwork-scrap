import requests
from bs4 import BeautifulSoup
from seleniumwire import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
import time
from time import sleep 
import datetime
import unicodedata
import urllib
from urllib.parse import urlencode, urlparse, parse_qs
import html
from lxml.html import fromstring
import json 

url = "https://www.upwork.com/ab/account-security/login" 
username = "YOUR EMAIL"
password = "YOUR PASSWORD"
keyword = "mobile-development"  ##change parameter as needed
page_limit = 10

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())  ##or put path to your geckodriver.exe
sleep(2)

# Set the request header using the 'header_overrides' attribute
driver.header_overrides = {
    'Referer': 'referer_string',
}

#faz login no site upwork.com
driver.get(url)
sleep(3)

fp = webdriver.FirefoxProfile()  ##modify accordly
path_modify_header = r'C:\Users\Gabriel\Desktop\helloWorld\modify_headers-0.7.1.1-fx.xpi'  ##change
fp.add_extension(path_modify_header)
fp.set_preference("modifyheaders.headers.count", 1)
fp.set_preference("modifyheaders.headers.action0", "Will")
fp.set_preference("modifyheaders.headers.name0", "FFOX") 
fp.set_preference("modifyheaders.headers.value0", "20.2") 
fp.set_preference("modifyheaders.headers.enabled0", True)
fp.set_preference("modifyheaders.config.active", True)
fp.set_preference("modifyheaders.config.alwaysOn", True)


driver.find_element_by_name("login[username]").send_keys(username)
sleep(1.5)
driver.execute_script("window.document.getElementById('username_password_continue').click()")
sleep(5)
driver.header_overrides = {
    'Referer': 'referer_string',
}

fp = webdriver.FirefoxProfile()
fp.add_extension(path_modify_header)
fp.set_preference("modifyheaders.headers.count", 1)
fp.set_preference("modifyheaders.headers.action0", "Will")
fp.set_preference("modifyheaders.headers.name0", "FFOX") 
fp.set_preference("modifyheaders.headers.value0", "20.2") 
fp.set_preference("modifyheaders.headers.enabled0", True)
fp.set_preference("modifyheaders.config.active", True)
fp.set_preference("modifyheaders.config.alwaysOn", True)


page = 1
pageline = []
  

#comeca o scrap para web development
while (page <= page_limit):
    new_url = "https://www.upwork.com/o/jobs/browse/?"+"page="+str(page)+"&q="+keyword+"&sort=recency"
    driver.get(new_url)
    time.sleep(9)
        
    html = driver.execute_script("return document.documentElement.outerHTML")
    upwork_soup = BeautifulSoup(html, 'html.parser')
    website = upwork_soup.findAll('section', {'class':'air-card air-card-hover job-tile-responsive ng-scope'})
               
    for data in website:  
                        
        link = data.findAll('a', {'class':'job-title-link'})
            

        for job_link in link:
            if job_link.has_attr('href'):
                half_link = job_link['href']
                job_page_link = "https://upwork.com" + half_link
                driver.get(job_page_link)
                time.sleep(4)
                    
                    
                html = driver.execute_script("return document.documentElement.outerHTML")
                job_page_soup = BeautifulSoup(html, 'html.parser')
                    
                    
                def getByCss(selector):
                    text = driver.find_element_by_css_selector(selector).text
                    print(text)
                    return text
                    
                job_title = getByCss('header h2')
                job_posted_time = job_page_soup.findAll('span', {'class':'inline'})[0].text.strip(" \n\t\r")
                job_detail = job_page_soup.findAll('section', {'class':'break mb-0'})[0].text.strip(" \n\t\r")
                job_features = getByCss('.job-features')
                job_type = getByCss('.list-unstyled span')
                job_level = data.findAll('strong', {'class':'js-contractor-tier'})[0].text.strip(" - \n\t\r")
                try:
                    job_estimated_time = data.findAll('strong', {'class':'js-duration'})[0].text.strip("Est. Time -  : \n\t\r ")
                except:
                    job_estimated_time = "No Data"
                try:
                    job_skill = job_page_soup.findAll('span', {'class':'o-tag disabled m-0-left m-0-top m-xs-bottom'})[0].text.strip(" - \n\t\r")
                except:
                    job_skill = "No Data"
                try:
                    job_country = data.findAll('strong', {'class':'primary'})[0].text
                except:
                    job_country = "No Data"   

                        
            page_line = {
                "Title": job_title,
                "Posted": job_posted_time,
                "Type": job_type,
                "Level": job_level,
                "Estimated Time": job_estimated_time,
                "Skill": job_skill,
                "Detail": job_detail,
                "Job Page Link": job_page_link                
            }

            pageline.append(page_line)    
            
    page += 1

with open('upwork_data.json', 'w') as outfile:  
    json.dump(pageline, outfile, indent=4)