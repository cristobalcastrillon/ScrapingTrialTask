from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_html(url):
    driver.get(url)
    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_all_elements_located)

    print('Current URL: ', driver.current_url)

    page_html = BeautifulSoup(driver.page_source, 'html.parser')
    return str(page_html)

def write_html_doc(index, html_str):
    '''
    This function is used for writing an HTML file
    It respects the directory hierarchy, so if a file's URL implies subdirectories
    (i.e. if it contains '/' characters) it will attempt to create the file in the specified directory locally.
    
    If the directory already exists locally, it will create it there; 
    otherwise, it will first create the directory.
    '''
    if type(index) is int:
        index += 1
    html_file = open(f'{index}.html', 'w')
    html_file.write(html_str)
    html_file.close()

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
write_html_doc('homepage', homepage_html_string)

# URLs of any other page on the website either start with the base URL,
# or a '/'.
# links_array = driver.find_elements(By.XPATH, f"//a[starts-with(@href, '/') or starts-with(@href, '{base_url}')]")
links_array = driver.find_elements(By.XPATH, f"//a[starts-with(@href, '/')]")
links_array.pop(0)
links_array = transformLinksArray(links_array)

# For each link to any *other* (not the base URL) page on the website, 
# perform the page's source HTML web scraping.
htmlDocs = []

for link in links_array:
    if not link.startswith('/'):
        htmlDocs.append(scrape_html(link))
    else:
        htmlDocs.append(scrape_html(f"{base_url}{link}"))
    curr_ind = links_array.index(link)
    write_html_doc(curr_ind, htmlDocs[curr_ind])