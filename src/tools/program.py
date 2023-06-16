from enum import Enum
from pprint import pprint

import requests
from parsel import Selector
from pydantic import Field

from utils.string_process import filter_html
from base import ToolModel

headers = {
    'User-Agent': """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43""",
    # 'referer': """https://blog.csdn.net/""",
    'cookie': """Hm_lvt_e5ef47b9f471504959267fd614d579cd=1685848574; https_waf_cookie=af5fc8c6-fc81-4038bab001f5bb3900573931669bb9158ef2; uuid_tt_dd=10_19421407380-1686948782541-741135; dc_session_id=10_1686948782541.324157; dc_sid=b2a67b61c1e3cd4d4c7edd1f0de87920; https_ydclearance=fadabedfa3cac060ee94487d-ba96-4aa5-8192-3d71b72e5bfc-1686956026"""
}


class CSDN(ToolModel):
    search_input: str = Field(description='CSDN论坛搜索输入')

    def use(self):
        url = f"https://so.csdn.net/api/v3/search?q={self.search_input}&t=blog&p=1&s=0&tm=0&lv=-1&ft=0&l=&u=&ct=-1" \
              f"&pnt=-1&ry=-1&ss=-1&dct=-1&vco=-1&cc=-1&sc=-1&akt=-1&art=-1&ca=-1&prs=&pre=&ecc=-1&ebc=-1&ia=1&dId" \
              f"=&cl=-1&scl=-1&tcl=-1&platform=pc&ab_test_code_overlap=&ab_test_random_code="
        r = requests.get(url, headers=headers)
        next_url = r.json()['result_vos'][0]['url']
        if not next_url:
            return '未找到相关结果'
        r = requests.get(next_url, headers=headers)
        sl = Selector(text=r.text)
        text_list = sl.xpath("""//div[@id='article_content']//text()""").getall()
        if not text_list:
            raise '遇到反爬'
        return filter_html(text_list)

    class Meta:
        name = "get_csdn_blog_info"
        description = "CSDN是全球知名中文IT技术交流平台,包含原创博客、精品问答、技术论坛等产品服务,提供原创、优质、完整内容的专业IT技术开发社区."


class JueJin(ToolModel):
    search_input: str = Field(description='掘金论坛搜索输入')

    def use(self):
        url = f"""https://api.juejin.cn/search_api/v1/search?spider=0&query={self.search_input}&id_type=0&cursor=0&limit=20&search_type=0&sort_type=0&version=1"""
        r = requests.get(url)
        article_id = r.json()['data'][0]['result_model']['article_id']
        next_url = f'https://juejin.cn/post/{article_id}'
        if not next_url:
            return '未找到相关结果'
        r = requests.get(next_url)
        sl = Selector(text=r.text)
        text_list = sl.xpath("""//div[@itemprop="articleBody"]/div/*[position()>2]//text()""").getall()
        if not text_list:
            raise '遇到反爬'
        return filter_html(text_list)

    class Meta:
        name = "get_juejin_blog_info"
        description = "掘金是面向全球中文开发者的技术内容分享与交流平台。我们通过技术文章、沸点、课程、直播等产品和服务，打造综合类技术社区。"
