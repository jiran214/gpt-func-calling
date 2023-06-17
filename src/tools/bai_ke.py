from enum import Enum
import requests
from parsel import Selector
from pydantic import Field

from moudles import session
from utils.string_process import filter_html
from base import ToolModel


class TemperatureUnit(str, Enum):
    celsius = 'celsius'
    fahrenheit = 'fahrenheit'


headers = {
    'User-Agent': """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43""",
    'cookie': """zhishiTopicRequestTime=1686930411657; BAIKE_SHITONG=%7B%22data%22%3A%220f0cbad1e8052f10878993106a4bd1cc2b15888dc99fba71b59334d6494023de22a35fc6aa9a2804e9d63dec196399f86245fb7018b1614827aac90d56d32a5eacab26d5043e8f718a3be37e087b7d5d307ead060ab590ab2847e9615f7211d8%22%2C%22key_id%22%3A%2210%22%2C%22sign%22%3A%2260fcc606%22%7D; BAIDUID=713CB59BDB474EE9AFCC4E0CCEF4EFDF:FG=1; BIDUPSID=713CB59BDB474EE9AFCC4E0CCEF4EFDF; PSTM=1684554678; newlogin=1; BAIDUID_BFESS=713CB59BDB474EE9AFCC4E0CCEF4EFDF:FG=1; ZFY=fNTO5QaO8MX8m1r49ef3AzbGZd4uFmZHDMCXcxBHMbE:C; __bid_n=18837241abd266edd64207; BAIDU_WISE_UID=wapp_1684662096824_212; BDUSS=gtS2p-d2hlNm1vbVFSfm40MHVlanhmUDRKbVdrRWo2SkZHMXJRRi10ZUZ4cDVrRVFBQUFBJCQAAAAAAAAAAAEAAADKfHhasKGwobbuztLIpcilAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIU5d2SFOXdkST; BDUSS_BFESS=gtS2p-d2hlNm1vbVFSfm40MHVlanhmUDRKbVdrRWo2SkZHMXJRRi10ZUZ4cDVrRVFBQUFBJCQAAAAAAAAAAAEAAADKfHhasKGwobbuztLIpcilAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIU5d2SFOXdkST; FPTOKEN=H/bnHT3J9MbygOPx3ofikribhOYmoHVzKqCzq/IGsybItDzqzSjWhez2lu7sHXD27iCsK06eQRxxZv9a/PQ5in7ln6QQpHho7Su8MQcA+lbRQuWaNCvkSIyQhEhmLidlBgMrXcNduftoBvAn09+H2Wp/ktl33j5CUo89C1DCA/dqD6ekrVEAnyBjxTR7n9WKC5aujx9ikgYgwB9z2Byjg3FzSHpTAKb/MPBuZaR3/0Igu9i3KPXA1lywFWKNKohkhhbYoB4IphZluBa85n/pK972HLyhzV3za7XnptqfR1tuW2J65gcYsFtJmsRVH2f1VsD1pibb/LCzKjM99ZzMruRYYlbLVPLyd/RHa4rakixaY9q7gwSPPzEUqeL0jAVAYrF90BJ6Myvg8F15ShzAJg==|9zXV1+87HTmz/CABUmTR38iSsf/eXf1+QqrNMbhB7dQ=|10|cb4a17febd4adba622cbbfd12afe1553; Hm_lvt_55b574651fcae74b0a9f1cf9c8d7c93a=1686845869,1686927810; zhishiTopicRequestTime=1686927813308; BCLID=12201278950458286643; BDSFRCVID=XL-OJeC626QNXsrfZhMnhwS0QqmGvpRTH6_vGfi489_Mbk2FNcQBEG0PDU8g0KA-8pxBogKKKgOTHICF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=fRAfoC-Mf-JEJb51q4o-bJD8KpOJK4J3HDo-LIv9BT6cOR5Jj6K-0fCRKp5hXtvuaDbfbKJl-R6nf4J-3MA-BnK1bxuJqTcdBCrWoqQkKMjIsq0x0MOle-bQyPLLqnOO0DOMahvc5h7xOhTJQlPK5JkgMx6MqpQJQeQ-5KQN3KJmfbL9bT3YjjISKx-_J6kJfRRP; BCLID_BFESS=12201278950458286643; BDSFRCVID_BFESS=XL-OJeC626QNXsrfZhMnhwS0QqmGvpRTH6_vGfi489_Mbk2FNcQBEG0PDU8g0KA-8pxBogKKKgOTHICF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=fRAfoC-Mf-JEJb51q4o-bJD8KpOJK4J3HDo-LIv9BT6cOR5Jj6K-0fCRKp5hXtvuaDbfbKJl-R6nf4J-3MA-BnK1bxuJqTcdBCrWoqQkKMjIsq0x0MOle-bQyPLLqnOO0DOMahvc5h7xOhTJQlPK5JkgMx6MqpQJQeQ-5KQN3KJmfbL9bT3YjjISKx-_J6kJfRRP; BK_SEARCHLOG=%7B%22key%22%3A%5B%22win10%20%E5%85%B3%E9%97%AD%E8%80%81%E6%9D%BF%E9%94%AE%22%2C%22%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%22%2C%22%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E7%AE%97%E6%B3%95sww%22%2C%22%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E7%AE%97%E6%B3%95%22%2C%22%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E7%AE%97%E6%B3%95a%22%2C%22%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E9%98%BF%E8%90%A8%22%5D%7D; X_ST_FLOW=0; baikeVisitId=ecd738fe-c4b5-41b8-9959-088057c1ead6; Hm_lpvt_55b574651fcae74b0a9f1cf9c8d7c93a=1686930698; ab_sr=1.0.1_OWNlNDVhZTIxY2IzMzgyMjExNzg5MjYwOWZlYzFjZWU5NDA0MGI1ODE0MWFlMDNjMjhmZTQxZWUwYTNjMWUzMDAzN2FjODZhNGRiYTA3YjdlOTIwODkyM2Y5OGIzYzhhMDVmNDA5OGI0MGE3OTEwOTdjMDc3ZmIzN2RhMThiOWNjNDZiYzM3Yjk5YTIwZTA1NTg0OTkzOTIxMzY2ZWRjN2RlNzgzZWJkYjVkZDE0OWNmODJkYzczMjM5OGM0MGE5; RT="z=1&dm=baidu.com&si=125fd020-cb08-46c9-ad46-dae9eab25096&ss=liyp9d4b&sl=11&tt=1611&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=1q1v4&ul=1q7o4\""""
}


class BaiduBaike(ToolModel):
    search_input: str = Field(description='百度百科搜索输入')

    def use(self):
        url = f"https://baike.baidu.com/api/searchui/suggest?wd={self.search_input}&enc=utf8"
        r = session.get(url)
        data_list = r.json()['list']
        if not data_list:
            return '未找到相关结果'
        lemma_title = data_list[0]['lemmaTitle']
        lemma_id = data_list[0]['lemmaId']
        new_url = f"https://baike.baidu.com/item/{lemma_title}/{lemma_id}"
        r = session.get(new_url, headers=headers)
        sl = Selector(text=r.text)
        text_list = sl.xpath("""//div[@class='main-content J-content']//text()""").getall()
        if not data_list:
            return '遇到反爬'
        return filter_html(text_list[59:])

    class Meta:
        name = "get_baidu_baike_info"
        description = "百度百科是一部内容开放、自由的网络百科全书，旨在创造一个涵盖所有领域知识，服务所有互联网用户的中文知识性百科全书。"


