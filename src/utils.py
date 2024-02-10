import os
import re
import sys
from time import sleep
import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()
CONSUMER_URL = os.getenv('CONSUMER_URL')
ANALYSIS_URL = os.getenv('ANALYSIS_URL')
DEBUG = os.getenv('DEBUG') == 'True'
VARIABLE_NAME = os.getenv('VARIABLE_NAME')

def remove_special_characters(text):
    return re.sub(r'[^a-zA-Z0-9_/]', '_', text)

def generate_file_name(item):
    try:
        first_part = item.split(';')[0]
        parts = first_part.split('.')
        if len(parts) != 3:
            raise ValueError("Expected 3 parts, got {}".format(len(parts)))
        [name, _, issue] = parts
        names = name.split(',')
        issue.split(' ')
        for i in range(len(names)):
            names[i] = names[i].lower().strip()
        itemName = ''.join(names) + ''.join(issue)
        return f'files/{remove_special_characters(itemName)}'
    except:
        return f'files/{remove_special_characters(item.lower().strip())}'

def check_items(items):
    for item in items:
        dir_name = generate_file_name(item)
        if os.path.exists(dir_name):
            print(f'Item: \n{item} has a PDF file.')
        else:
            print(f'Item: \n{item} does not have a PDF file.')

def print_input(item):
    print('.\n'.join(item))

def parse_input(input=sys.stdin.read()):
    parsed = input.split('.\n')
    return [item.strip() for item in parsed]

def create_http_session():
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries, pool_connections=10, pool_maxsize=20)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def handle_http_response(session, url):
    try:
        response = session.get(url, headers={'Accept': 'application/pdf'})
        response.raise_for_status()
        return response
    except requests.exceptions.RetryError as e:
        if DEBUG:
            print(f"Max retries error: {e}")
    except requests.exceptions.HTTPError as e:
        if DEBUG:
            print(f"HTTP error: {e}")
    except requests.exceptions.ConnectionError as e:
        if DEBUG:
            print(f"Connection error: {e}")
    except requests.exceptions.Timeout as e:
        if DEBUG:
            print(f"Timeout error: {e}")
    except requests.exceptions.RequestException as e:
        if DEBUG:
            print(f"Error: {e}")
    except Exception as e:
        if DEBUG:
            print(f"Unknown error: {e}")
    sleep(10)
    return None

def find_all_links(text):
    return re.findall(r'<a\s+[^>]*href="([^"]*)"[^>]*>.*?</a>', text)

def obtain_links_from_item(text):
    html_components = find_all_links(text)
    links = set()
    [link for link in html_components if link.startswith('https://') and link not in links and link.endswith('.pdf') and not links.add(link)]
    return links

def response_is_valid_and_pdf(response):
    return response is not None and response.status_code == 200 and 'application/pdf' in response.headers.get('Content-Type', '')

def create_file(name, content):
    with open(f'{name}', 'wb') as file:
        file.write(content)
