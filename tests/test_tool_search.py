import os

import config
from tools.search_engine import GoogleSearch

os.environ["http_proxy"] = f'http://{config.proxy}/'
os.environ["https_proxy"] = f'http://{config.proxy}/'


def test_google():
    res = GoogleSearch(search_input='蔡徐坤').use()
    print(res)
    assert len(res) > 200