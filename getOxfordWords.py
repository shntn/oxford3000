import requests
import lxml.html
import json

def fetchHtml(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise
    return response.text

def readHtml(url):
    with open("3000.html", "r") as f:
        html = f.read()
    return html

def getItem(item_html):
    word = {}
    item = lxml.html.fromstring(item_html)
    word['hw'] = item.xpath('normalize-space(//li/@data-hw)')
    word['word'] = item.xpath('//li/span/text()')[0]
    word['pos'] = item.xpath('normalize-space(//li/span[@class="pos"]/text())')
    ox3000 = item.xpath('normalize-space(//li/@data-ox3000)')
    word['ox5000'] = item.xpath('normalize-space(//li/@data-ox5000)')
    # belongto = item.xpath('normalize-space(//li/div/span[@class="belong-to"]/text())')
    if len(ox3000) != 0:
        word['ox3000'] = ox3000
    return word

def parseHtml(html):
    element = lxml.html.fromstring(html)
    collect = element.xpath('//div[@id="wordlistsContentPanel"]/ul[@class="top-g"]/li')
    ox_words = []
    for item in collect:
        item_string = lxml.html.tostring(item)
        word = getItem(item_string)
        ox_words.append(word)
        # print('hw: {}, word: {}, pos: {}, ox3000: {}, ox5000: {}'
        #         .format(word['hw'], word['word'], word['pos'], word['ox3000'], word['ox5000']))
    return ox_words

def convertToJson(words):
    # json_words = json.dumps(words)
    # json_words = json.dump(words, ensure_ascii=False, indent=4, separators=(',', ': '))
    with open('oxford_words.json', 'w') as f:
        json.dump(words, f, ensure_ascii=False, indent=4, separators=(',', ': '))

def main():
    # fetch html
    url = 'https://www.oxfordlearnersdictionaries.com/wordlists/oxford3000-5000'
    html = fetchHtml(url)
    # html = readHtml(url)

    # parse html
    words = parseHtml(html)

    # save json
    convertToJson(words)

if __name__ == '__main__':
    main()
