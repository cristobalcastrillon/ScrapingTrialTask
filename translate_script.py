from google.cloud import translate_v2 as translate
from bs4 import BeautifulSoup

translate_client = translate.Client()

def translate_hindi(text):
    translated = translate_client.translate(text, target_language='es')
    return translated['translatedText']

def translate_html_doc(filename, path=None):
    # try:
    if path is None:
        html_file = open(filename, 'r')
    else:
        html_file = open(f'{path}/{filename}', 'r')

    html_original = str(BeautifulSoup(html_file, 'html.parser'))
    html_file.close()

    html_hindi = split_and_request(html_original)
    new_file = open('new.html', 'w')
    new_file.write(html_hindi)
    new_file.close()
    
    # except:
    #     print(f'File {filename} does not exist in specified path {path}.')

def split_and_request(text):
    # TODO: Check for last '>' in interval text[0,5000], and use that index as 'discarded'
    translated_text = ''
    while(len(text) != 0):
        if len(text) < 5000:
            discarded = len(text)
        else:
            discarded = 5000
        translated_text += translate_hindi(text[:discarded])
        translated_text += text[:discarded]
        text = text[discarded:]
    return translated_text

translate_html_doc('index.html')