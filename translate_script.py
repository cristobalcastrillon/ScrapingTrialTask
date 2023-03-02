from bs4 import BeautifulSoup

def translate_html_doc(filename, path=None):
    # try:
    if path is None:
        html_file = open(filename, 'r')
    else:
        html_file = open(f'{path}/{filename}', 'r')

    # html_original = str(BeautifulSoup(html_file, 'html.parser'))
    html_original = BeautifulSoup(html_file, 'html.parser')

    html_file.close()

    html_hindi = split_and_request(html_original)
    new_file = open('new.html', 'w')
    new_file.write(html_hindi)
    new_file.close()
    
    # except:
    #     print(f'File {filename} does not exist in specified path {path}.')

def split_and_request(soup):
    str_soup = str(soup)
    # TODO: Check for last '>' in interval text[0,5000] or text[0,len(...)], and use that index as 'discarded'
    for string in soup.strings:
        
        trans_string = 'I\'m not paying for translation'
        
    return str_soup

# def split_and_request(text):
#     # TODO: Check for last '>' in interval text[0,5000] or text[0,len(...)], and use that index as 'discarded'
#     translated_text = ''
#     while(len(text) != 0):
#         # discarded is set to a length less than or equal to 5000
#         if len(text) < 5000:
#             discarded = len(text)
#         else:
#             discarded = 5000
#         to_be_concat = text[:discarded]
#         index = to_be_concat.rindex('</')
#         to_be_concat = to_be_concat[:index]

#         # translated_text += translate_hindi(to_be_concat)
#         translated_text += to_be_concat

#         text = text[index:]

#     return translated_text

translate_html_doc('index.html')