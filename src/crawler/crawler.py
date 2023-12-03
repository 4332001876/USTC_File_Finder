import sys
sys.path.append('../')
from urllib.parse import urljoin
from config import Config
import requests
from bs4 import BeautifulSoup
# import pandas as pd
import time
import json



class Crawler_2:
    def __init__(self) -> None:
        pass

    def fetch_data(self, url, encoding):
        """Fetch data from url. Return the content of the response."""
        time.sleep(Config.SLEEP_TIME)  # sleep for n second to avoid being blocked
        headers = {"User-Agent": Config.USER_AGENT, 'Cookie': Config.COOKIE}
        response = requests.get(url, headers=headers)
        if encoding:
            response.encoding = encoding
        return response.text
    
    def fetch_file(self, url, html_locator, encoding):
        """Fetch file from url. Return a list of bs4.element.Tag."""
        bs = BeautifulSoup(self.fetch_data(url, encoding), 'html.parser')

        for operation in html_locator:
            method = operation['method']
            args = operation['args']
            kwargs = operation.get('kwargs', None)

            if method == 'find':
                if kwargs:
                    bs = bs.find(args, **kwargs)
                else:
                    bs = bs.find(args)

            elif method == 'find_all':
                if kwargs:
                    bs = bs.find_all(args, **kwargs)
                else:
                    bs = bs.find_all(args)
            
            if bs == None:
                return None

        return bs
    
    def get_info(self, bs_result, url, method, args, kargs, args2):

        if method == 'find' and kargs == None:
            if args2 == 'text':
                return bs_result.find(args).text.strip()
            elif args2 == 'href':
                return urljoin(url, bs_result.find(args)[args2])
            else:
                return bs_result.find(args)[args2]

        elif method == 'find' and kargs != None:
            if args2 == 'text':
                return bs_result.find(args, **kargs).text.strip()
            elif args2 == 'href':
                return urljoin(url, bs_result.find(args, **kargs)[args2])
            else:
                return bs_result.find(args, **kargs)[args2]

        elif method == None:
            return None

    def fetch_file_list(self, url, encoding, html_locator, info_locator , source_name, file_type = None, file_type_2 = None):
        """Fetch file list from url. Return a list of dict."""
        bs_result = self.fetch_file(url, html_locator, encoding)

        if bs_result == None:
            return None
        
        result = []

        for i in range(len(bs_result)):
            result.append(dict())
            
            for operation in info_locator:
                info = operation['info']
                method = operation['method']
                args = operation['args']
                args2 = operation['args2']
                kargs = None

                if type(args) == list:
                    kargs = args[1]
                    args = args[0]

                result[i][info] = self.get_info(bs_result[i], url, method, args, kargs, args2)

            
            if result[i]['time'] != None and result[i]['time'].count('\n') == 1:
                parts = result[i]['time'].split('\n')
                result[i]['time'] = f'{parts[1]}-{parts[0]}'

            if '发布时间' in result[i]['time']:
                result[i]['time'] = result[i]['time'][5:15]

            result[i]['source'] = source_name
            result[i]['file_type'] = file_type
            result[i]['file_type_2'] = file_type_2

        return result
    
    def generate_file_list(self):
        file_list = []
        with open('data.json', 'r') as json_file:
            data_list = json.load(json_file)

        for data in data_list:
            url = data['url']
            encoding = data['encoding']
            html_locator = data['html_locator']
            info_locator = data['info_locator']
            source_name = data['title']
            file_type = data['dtype']
            file_type_2 = data['dtype2']
            flip = data['flip']
            
            if flip == False:
                file_list += self.fetch_file_list(url, encoding, html_locator, info_locator, source_name, file_type, file_type_2)

            else:
                for i in range(1, 100):
                    flip_url = url.replace('{page_num}', str(i))
                    flip_result = self.fetch_file_list(flip_url, encoding, html_locator, info_locator, source_name, file_type, file_type_2)
                    if flip_result == None or len(flip_result) == 0:
                        break
                    else:
                        file_list += flip_result

        return file_list