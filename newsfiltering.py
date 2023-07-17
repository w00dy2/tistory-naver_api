import requests
from bs4 import BeautifulSoup
from konlpy.tag import Hannanum
from collections import Counter


def crawling():
    # 언론사별 id 값 리스트에 추가
    news_urls = ['081', '973', '123', '975', '972', '882', '932', '025', '920', '009', '023', '366', '914',
                 '079', '015', '974', '961', '539', '804', '002', '014', '008', '957', '812', '227', '810',
                 '922', '243', '941', '943', '921', '925', '018', '682', '809', '028', '968', '930', '690',
                 '826', '047', '963', '042', '970', '993', '016', '021', '823', '824', '120', '327', '038',
                 '954', '143', '803', '801', '971', '816', '687', '417', '964', '685', '969', '960', '944',
                 '013', '006', '913', '031', '005', '020', '368', '536', '022', '353', '942', '011', '032',
                 '959']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    # 텍스트를 저장할 변수
    text_data = ''

    # URL 순회
    for news in news_urls:
        url = f'https://newsstand.naver.com/include/page/{news}.html'
        response = requests.get(url, headers=headers)
        html = response.text

        # HTML 파싱
        soup = BeautifulSoup(html, 'html.parser')

        # 텍스트 추출
        text = soup.get_text()

        # 텍스트 데이터에 추가
        text_data += text

    # 텍스트 파일로 저장
    with open('combined_text.txt', 'w', encoding='utf-8') as file:
        file.write(text_data)

def countingwords():
    # konlpy로 최빈 단어 카운팅
    Hannanum = Hannanum()
    nouns = Hannanum.nouns(text_data)

    excluded_words = ['뉴스스탠드', '영상', '포토', '페이지', '기업', '이유', '뉴스', '영역', '논란'] #제외할 단어 설정
    filtered_nouns = [word for word in nouns if len(word) > 1 and word not in excluded_words] # 한글자 이하는 제외

    counted_words = Counter(filtered_nouns)

    # 상위 50개 단어 출력
    #print('Top 50 단어:')
    #for word, count in counted_words.most_common(50):
    #    print(f'{word}: {count}')
    #
    # 가장 많이 카운팅된 단어부터 10개 추가
    top_10 = [word for word, _ in counted_words.most_common(10)]
    print('Top 10 단어:', top_10)


import os
import sys
import urllib.request
import datetime
import time
import json

client_id = "네이버 api client id"
client_secret = "네이버 api 시크릿키 추가"

# [CODE 1]
def getRequestUrl(url):
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

# [CODE 2]
def getNaverSearch(node, srcText, start, display):
    base = "https://openapi.naver.com/v1/search"
    node = "/%s.json" % node
    parameters = "?query=%s&start=%s&display=%s&sort=sim" % (urllib.parse.quote(srcText), start, display)

    url = base + node + parameters
    responseDecode = getRequestUrl(url)  # [CODE 1]

    if (responseDecode == None):
        return None
    else:
        return json.loads(responseDecode)

# [CODE 3]
def getPostData(post, jsonResult, cnt):
    title = post['title']
    description = post['description']
    org_link = post['originallink']
    link = post['link']

    pDate = datetime.datetime.strptime(post['pubDate'], '%a, %d %b %Y %H:%M:%S +0900')
    pDate = pDate.strftime('%Y-%m-%d %H:%M:%S')

    jsonResult.append({'cnt': cnt, 'title': title, 'description': description,
                       'org_link': org_link, 'link': org_link, 'pDate': pDate})
    return

def save_json_to_file(json_data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)

result_list = []
folder_path = './news'
os.makedirs(folder_path, exist_ok=True)

# [CODE 0]
def main():
    for top10 in top_10:
        node = 'news'  # 크롤링 할 대상
        srcText = top10
        cnt = 0
        jsonResult = []
    
        jsonResponse = getNaverSearch(node, srcText, 1, 100)  # [CODE 2]
        total = jsonResponse['total']
    
        while ((jsonResponse != None) and (jsonResponse['display'] != 0)):
            for post in jsonResponse['items']:
                cnt += 1
                getPostData(post, jsonResult, cnt)  # [CODE 3]
    
            start = jsonResponse['start'] + jsonResponse['display']
            jsonResponse = getNaverSearch(node, srcText, start, 100)  # [CODE 2]
    
        print('전체 검색 : %d 건' % total)
    
        # JSON 데이터를 파일로 저장
        file_name = f'{srcText}_naver_{node}.json'
        file_path = os.path.join(folder_path, file_name)
        save_json_to_file(jsonResult, file_path)
    
        result_list.append(file_name)
    
        print("가져온 데이터 : %d 건" % (cnt))
        print('%s_naver_%s.json SAVED' % (srcText, node))




# 티스토리 작성

import requests
from bs4 import BeautifulSoup
from datetime import datetime

access_token = '티스토리 api 토큰'

def load_json_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    return json_data

def write_text_from_json(json_data):
    text = ''
    visited_links = set()  # 중복된 org_link를 제거하기 위한 set
    #number = 1  # 순차적으로 증가하는 번호
    
    for i in range(min(1, len(json_data))):
        item = json_data[i]
        title = item['title']
        org_link = item['org_link']
        pDate = item['pDate']
        
        # 중복된 org_link인 경우 건너뜀
        if org_link in visited_links:
            continue
        
        visited_links.add(org_link)  # org_link를 set에 추가
        #number += 1  # 번호 증가
        
        text += f'<h2 data-ke-size="size26">{title}</h2>\n'
        text += f'<p data-ke-size="size16">원본뉴스: <a href="{org_link}">{org_link}</a></p>\n'
        text += f'<p data-ke-size="size16">발행시간: {pDate}</p>\n\n'

    return text


def write_ti():
    base_url = 'https://www.tistory.com/apis/post/write'
    
    # 제목 설정
    title = f'{datetime.now().strftime("%Y-%m-%d")} - 네이버 뉴스스탠드 간추린 뉴스'
    
    # JSON 파일들의 내용을 가져와서 contents에 저장
    contents = ''
    for file_name in result_list:
        file_path = os.path.join(folder_path, file_name)
        json_data = load_json_from_file(file_path)
        text = write_text_from_json(json_data)
        
        contents += text + '\n'
    contents +=  '\n\n'
    contents += f'<p data-ke-size="size16">해당뉴스는 {datetime.now().strftime("%Y-%m-%d-%hh")} 기준</p>'
    contents += '<p data-ke-size="size16">네이버 뉴스스탠드의 79개 언론사를 기준으로 최빈단어를 카운트 한 후 작성한 글입니다.</p>\n\n'   
    
    parameters = {
        'access_token': access_token,
        'output': '{output-type}',
        'blogName': '티스토리 블로그 이름',
        'title': title,
        'content': contents,
        'visibility': '3',
        'category': '카테고리명',
        'tag': '해시태그 설정',
        'acceptComment': '1'
    }
    
    result = requests.post(base_url, params=parameters)
    result = BeautifulSoup(result.text)
    print(result.prettify())



if __name__ == '__main__':
    
    crawling()
    countingwords()
    main()
    print(result_list)
    write_ti()
