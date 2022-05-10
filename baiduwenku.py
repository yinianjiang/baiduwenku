import re
import json
import requests

session = requests.session()


# 发送请求 获取内容
def fetch_url(url):
    return session.get(url).content.decode('utf-8')


# 从url获取docId
def get_doc_id_by_url(url):
    return re.findall('view/(.*).html', url)[0]


# 获取docId
def get_doc_id(content):
    return re.findall(r"docInfo.*?showDocId\".*?\:.*?\"(.*?)\"\,", content)[0]


def parser_type(content):
    return re.findall(r"docInfo.*?fileType\".*?\:.*?\"(.*?)\"\,", content)[0]


def parser_title(content):
    return re.findall(r"docInfo.*?title\".*?\:.*?\"(.*?)\"\,", content)[0]


def parse_txt(doc_id):
    content_url = 'https://wenku.baidu.com/api/doc/getdocinfo?callback=cb&doc_id=' + doc_id
    content = fetch_url(content_url)
    md5 = re.findall('"md5sum":"(.*?)"', content)[0]
    pn = re.findall('"totalPageNum":"(.*?)"', content)[0]
    rsign = re.findall('"rsign":"(.*?)"', content)[0]
    contents_url = 'https://wkretype.bdimg.com/retype/text/' + doc_id + '?rn=' + pn + '&type=txt' + md5 + '&rsign=' + rsign
    print('contents_url' + contents_url)
    content = json.loads(fetch_url(contents_url))
    result = ''
    for item in content:
        for i in item['parags']:
            # result += i['c'].replace('\\r', '\r').replace('\\n', '\n')
            result += i['c']
    return result


# 保存文件
def save_file(fileName, content):
    with open(fileName, 'w', encoding='utf-8') as f:
        f.write(content)
        print('已保存文件名为' + fileName)


# 主函数
def main():
    # 示例url
    # https://wenku.baidu.com/view/7f3a549c0975f46526d3e125.html?fr=search-rec-5
    # https://wenku.baidu.com/view/f3798587ec3a87c24028c472.html?fixfr=6n73ELOP4KwZmsinGlJMng%253D%253D&fr=income2-search
    url = input("请输入下载的文库url: ")
    # 请求
    content = fetch_url(url)
    print(content)
    # 获取 docId
    doc_id = get_doc_id(content)
    print(doc_id)
    # 文档类型
    type = parser_type(content)
    print(type)
    # 标题
    title = parser_title(content)
    print(title)
    result = parse_txt(doc_id)
    save_file(title + '.txt', result)


main()
