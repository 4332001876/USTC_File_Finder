import sys
sys.path.append('../')

from urllib.parse import urljoin
from config import Config
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
from tqdm import tqdm

'''
这个函数从web_list.json中逐个爬取网站信息
如果需要生成csv文件：
        Crawler().generate_file_csv()
如果要将爬虫部分集成到后续的数据库部分中，在：
        Crawler().generate_file_list()
        这一部分将会返回一个list，list中的每个元素是一个dict，dict中包含了爬取到的信息

如果你想要更新web_list.json，可以使用useless目录下的create_json.ipynb中的add_data函数。一个代码块代表着一个网站数据的添加

后续工作因为你们还没做，我就先这样拱手掌柜了，要改爬虫逻辑或者有什么可以优化的找fcx

可能在主函数中调用这个爬虫类，需要改一下158行的路径，我在crawler文件夹中改代码可以正确运行，我还不太清楚主函数的实现逻辑，所以也还没改
'''

class Crawler:
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

        # elif method == None:
        #     return None
        elif method == None:
            if args2 == 'text':
                return bs_result.text.strip()
            elif args2 == 'href':
                return urljoin(url, bs_result[args2])

    def fetch_file_list(self, url, encoding, html_locator, info_locator , source_name, file_type = None, file_type_2 = None):
        """Fetch file list from url. Return a list of dict."""

        # 极其特殊的先研院网站翻页机制
        if url == 'https://iat.ustc.edu.cn/iat/x161/index_1.html':
            url = 'https://iat.ustc.edu.cn/iat/x161/index.html'

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

            
            if result[i]['time'] == None or result[i]['time'] == '': 
                pass

            elif result[i]['time'].count('\n') == 1:
                parts = result[i]['time'].split('\n')
                result[i]['time'] = f'{parts[1]}-{parts[0]}'

            elif '发布时间' in result[i]['time']:
                result[i]['time'] = result[i]['time'][5:15]

            elif '[' == result[i]['time'][0]:
                result[i]['time'] = result[i]['time'][1:-1]

            elif result[i]['time'].count('年') == 1 and result[i]['time'].count('月') == 1 and result[i]['time'].count('日') == 1:
                result[i]['time'] = result[i]['time'].replace('年', '-').replace('月', '-').replace('日', '')

            # 检测时间末尾是否带有标题，如有，则去除时间中的标题。超算中心网站特性
            if result[i]['title'] in result[i]['time']:
                result[i]['time'] = result[i]['time'].replace(result[i]['title'], '').strip()[:-1]
            
            # 检测标题末尾是否有[xxxx-xx-xx]的时间信息，如有，在标题中去除，并将对应内容移动到时间处。时间处内容不包括括号(软件学院网站bug)
            if result[i]['title'][-11:-1].count('-') == 2:
                result[i]['time'] = result[i]['title'][-11:-1]
                result[i]['title'] = result[i]['title'][:-13]
            

            result[i]['source'] = source_name
            result[i]['file_type'] = file_type
            result[i]['file_type_2'] = file_type_2

        return result
    
    def generate_file_list(self):
        file_list = []
        with open('web_list.json', 'r') as json_file:
            data_list = json.load(json_file)

        for data in tqdm(data_list, desc='Processing', unit='item'):
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
    
    def generate_file_csv(self):
        file_list = self.generate_file_list()
        df = pd.DataFrame(file_list)
        df.to_csv('file_list.csv', index=False)
        return df
