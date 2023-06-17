import requests
from parsel import Selector
from pydantic import Field

from base import ToolModel
from moudles import session
from utils.string_process import filter_html


headers = {
    'User-Agent': """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43""",
}


class WangYiNews(ToolModel):
    search_input: str = Field(description='网易新闻内容搜索输入')

    def use(self):
        url = f"""https://www.163.com/search?keyword={self.search_input}"""
        r = session.get(url, headers=headers)
        sl = Selector(text=r.text)
        next_url = sl.xpath("""//div[@class="keyword_list "]/div[1]//div[@class="keyword_img"]/a/@href""").get()
        if not next_url:
            return '未找到相关结果'
        r = session.get(next_url, headers=headers)
        sl = Selector(text=r.text)
        test_list = sl.xpath("""//div[@class="post_body"]//text()""").getall()
        return filter_html(test_list)

    class Meta:
        name = "get_163_news_results"
        description = (
            "网易是中国领先的互联网技术公司，为用户提供免费邮箱、游戏、搜索引擎服务，开设新闻、娱乐、体育等30多个内容频道，及博客、视频、论坛等互动交流，网聚人的力量。"
        )

