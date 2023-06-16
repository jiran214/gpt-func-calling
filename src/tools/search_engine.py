import requests
from pydantic import Field

from base import ToolModel
from config import google_settings


class GoogleSearch(ToolModel):
    search_input: str = Field(description='谷歌搜索输入')

    def use(self):
        url = f"""https://www.googleapis.com/customsearch/v1?key={google_settings['key']}&cx={google_settings['cx']}&q={self.search_input}"""
        r = requests.get(url)
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

