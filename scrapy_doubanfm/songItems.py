import scrapy

class SongItem(scrapy.Item):
    # 歌名
    song_name = scrapy.Field()
    # 歌手
    singer = scrapy.Field()