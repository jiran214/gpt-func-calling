import requests
from parsel import Selector
from pydantic import Field

import config
from base import ToolModel
from config import google_settings
from moudles import session


class GoogleSearch(ToolModel):
    search_input: str = Field(description='谷歌搜索输入')

    def use(self):
        url = f"""https://www.googleapis.com/customsearch/v1?key={google_settings['key']}&cx={google_settings['cx']}&q={self.search_input}"""
        r = session.get(url, proxies=config.proxies)
        if not r:
            return '未找到相关结果'
        json_list = r.json()['items'][:4]
        results = []
        for json_data in json_list:
            data_dict = {
                'title': json_data['title'],
                'link': json_data['link'],
                'snippet': json_data['snippet'],
                'html_snippet': json_data['htmlSnippet']
            }
            results.append(data_dict)
        return str(results)

    class Meta:
        name = "get_google_search_results"
        description = (
            "A wrapper around Google Search. "
            "Useful for when you need to answer questions about current events. "
        )


class BingSearch(ToolModel):

    search_input: str = Field(description='bing搜索输入')

    def use(self):
        url = f"""https://cn.bing.com/search?q={self.search_input}&aqs=edge.2.69i64i450l8.175106209j0j1&FORM=ANAB01&PC=HCTS"""
        r = session.get(url)
        if not r:
            return '未找到相关结果'
        html = r.text
        sl = Selector(text=html)
        items = sl.xpath("""//li[@class='b_algo']""")
        results = []
        for item in items:
            data_dict = {
                'title': ' '.join(item.xpath("""./div[1]//h2//text()""").getall()),
                'link': item.xpath("""./div[1]//a/@href""").get(),
                'snippet': ' '.join(item.xpath("""./div[2]//p//text()""").getall()),
                # 'html_snippet': json_data['htmlSnippet']
            }
            results.append(data_dict)

            if len(results) == 7:
                break
        return str(results)

    class Meta:
        name = "get_bing_search_results"
        description = "通过必应的智能搜索，可以更轻松地快速查找所需内容并获得奖励。"
