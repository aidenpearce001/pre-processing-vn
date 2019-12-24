from bs4 import BeautifulSoup
import requests
import itertools
import re
import string

NGRAM = 5

# r  = "https://vnexpress.net/"
# r =("https://vnexpress.net/kinh-doanh/chien-luoc-canh-tranh-bang-chat-luong-cong-nghe-cua-kymdan-4028678.html")

with open("vnexpress.txt") as f: 
    for line in f: 
    res = requests.get(line)
    html_page = res.content

    soup = BeautifulSoup(html_page, 'html.parser')

    article_text = ''
    article = soup.findAll('p')
    for element in article:
        article_text += ''.join(element.findAll(text = True))
    page = soup.find('p').getText()
    origin_text = article_text.split('.')
    # print(article_text.split('.'))
    # for link in soup.find_all('a'):
    #     page = link.get('href')
    #     if "vnexpress" in page:
    #         print(page)
    #         res1 = requests.get(page)
    #         page_link = res1.content

    #         soup1 = BeautifulSoup(page_link, 'html.parser')
    #         article_text = ''
    #         article = soup1.findAll('p')
    #         for element in article:
    #             article_text += ''.join(element.findAll(text = True))
    #         # page = soup.find('p').getText()
    #         print(article_text.split('.'))

    def extract_phrases(text):
        return re.findall(u'\w[\w ]+', text, re.UNICODE)


    phrases = itertools.chain.from_iterable(extract_phrases(text) for text in origin_text)
    phrases = [p.lower().strip() for p in phrases]

    def gen_ngrams(words, n=3):
        if isinstance(words, (str, unicode)):
            words = re.split('\s+', words.strip())
        
        if len(words) < n:
            padded_words = words + ['\x00'] * (n - len(words))
            yield tuple(padded_words)
        else:
            for i in range(len(words) - n + 1):
                yield tuple(words[i: i+n])

    # for i in phrases:
    #     print(remove_accent(i))
    ngrams = itertools.chain.from_iterable(gen_ngrams(p, NGRAM) for p in phrases)
    ngrams = list(set(' '.join(t) for t in set(ngrams)))

    # def extract_phrases(text):
    #     return re.findall(u'\w[\w ]+', text, re.UNICODE)

    accented_chars = {
        'a': u'a á à ả ã ạ â ấ ầ ẩ ẫ ậ ă ắ ằ ẳ ẵ ặ',
        'o': u'o ó ò ỏ õ ọ ô ố ồ ổ ỗ ộ ơ ớ ờ ở ỡ ợ',
        'e': u'e é è ẻ ẽ ẹ ê ế ề ể ễ ệ',
        'u': u'u ú ù ủ ũ ụ ư ứ ừ ử ữ ự',
        'i': u'i í ì ỉ ĩ ị',
        'y': u'y ý ỳ ỷ ỹ ỵ',
        'd': u'd đ',
    }

    plain_char_map = {}
    for c, variants in accented_chars.items():
        for v in variants.split(' '):
            plain_char_map[v] = c


    def remove_accent(text):
        return u''.join(plain_char_map.get(char, char) for char in text)
