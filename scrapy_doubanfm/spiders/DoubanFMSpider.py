import scrapy
from scrapy import Request
from scrapy import FormRequest
import json
from scrapy_doubanfm.songItems import SongItem

class DoubanFMSpider(scrapy.Spider):
    # 设置name
    name = "douban"
    # 设定域名
    allowed_domains = ["douban.fm"]
    # http头
    headers = {
        'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'douban.fm',
        'Origin': 'https://accounts.douban.com',
        'Referer': 'https://douban.fm/mine/hearts',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    # cookie
    cookies = {
        'bid': 'lLnjl6Xx3CQ',
        '_pk_id.100002.6447': 'aee28010fe10157a.1482231566.1.1482231566.1482231566.',
        '_vwo_uuid_v2': '26EA69680039C9434A4176D3D9264C13|617f928ef8c1dd8837a5821d0944c129',
        'flag': '"ok"',
        'ac': '"1488175402"',
        '_ga': 'GA1.2.872193095.1482212405',
        '_gat': '1',
        'dbcl2': '"75387024:eGvJcwefVXk"',
        'ck': 'D5Nf'
    }
    # 填写爬取地址
    start_urls = [
        "https://douban.fm/j/v2/redheart/basic",
        "https://douban.fm/j/v2/redheart/songs"
    ]

    def start_requests(self):
        return [Request(self.start_urls[0], callback=self.parse, cookies=self.cookies, headers=self.headers)]

    def parse(self, response):
        # print(response.body)
        basicRes = json.loads(response.body.decode('utf-8'))
        sidList = []
        songs = basicRes['songs']
        for song in songs:
            sidList.append(song['sid'])
        sids = '|'.join(sidList)
        # POST请求表单数据
        formdata = {
            'sids': sids,
            'kbps': '128',
            'ck': 'D5Nf'
        }
        yield FormRequest(self.start_urls[1], method='POST', callback=self.parse_followers, formdata=formdata, cookies=self.cookies, headers=self.headers)

    def parse_followers(self, response):
        songRes = json.loads(response.body.decode('utf-8'))
        for song in songRes:
            item = SongItem()
            item['song_name'] = song['title']
            item['singer'] = song['artist']
            yield item