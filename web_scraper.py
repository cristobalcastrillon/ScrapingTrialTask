from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import os
import time

# Absolute path to root directory
root_path = os.getcwd()

def scrape_html(url):
    try:
        driver.get(url)
        time.sleep(3)
        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_all_elements_located)
        
        print('Current URL: ', driver.current_url)
        
        page_html = BeautifulSoup(driver.page_source, 'html.parser')
        return str(page_html)
    except TimeoutException:
        print('Timeout exception occurred for URL: ', url)

def write_html_doc(href, html_str):
    '''
    This function is used for writing an HTML file
    It respects the directory hierarchy, so if an href argument's value implies subdirectories
    (i.e. if it contains '/' characters) it will attempt to create the file in the specified directory locally.
    
    If the directory already exists locally, it will create it there; 
    otherwise, it will first create the directory.
    '''
    href = href.replace(' ', '')
    tokenized_href = href.rsplit('/', 1)

    if len(tokenized_href) == 2:
        os.makedirs(tokenized_href[0], exist_ok=True)
        os.chdir(tokenized_href[0])

    try:
        if tokenized_href[-1] == '':
            html_file = open('index.html', 'w')
        else:
            html_file = open(f'{tokenized_href[-1]}.html', 'w')

        html_file.write(html_str)
        html_file.close()
    except:
        print(f'An error writing file for URL {href} has occurred.')
    
    if os.getcwd() != root_path:
        os.chdir(root_path)

def transformLinksArray(array):
    '''
    This function is used to transform every element in the links array 
    to a URL string, rather than a Web Element object
    '''
    for web_element in array:
        array[array.index(web_element)] = web_element.get_dom_attribute('href')

    return array

# Automatic install of chrome driver
driver = webdriver.Chrome(ChromeDriverManager().install())
base_url = 'https://www.classcentral.com'

# Scrape homepage's HTML and write it into a file
homepage_html_string = scrape_html(base_url)
write_html_doc('', homepage_html_string)

# URLs of any other page on the website either start with the base URL,
# or a '/'.
links_array = driver.find_elements(By.XPATH, f"//a[starts-with(@href, '/') or starts-with(@href, '{base_url}')]")
links_array.pop(0)
links_array = transformLinksArray(links_array)

# For each link to any *other* (not the base URL) page on the website, 
# perform the page's source HTML web scraping.
htmlDocs = []

for link in links_array:
    curr_ind = links_array.index(link)
    if not link.startswith('/'):
        htmlDocs.append(scrape_html(link))
        link = link.replace(base_url, '')
    else:
        htmlDocs.append(scrape_html(f"{base_url}{link}"))
    write_html_doc(link[1:], htmlDocs[curr_ind])