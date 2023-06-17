import os

import requests
from requests import session

import config
from tools.search_engine import GoogleSearch, BaiduSearch, BingSearch

os.environ["http_proxy"] = f'http://{config.proxy}/'
os.environ["https_proxy"] = f'http://{config.proxy}/'


def test_google():
    res = GoogleSearch(search_input='蔡徐坤').use()
    print(res)
    assert len(res) > 200


def test_baidu():
    res = BaiduSearch(search_input='蔡徐坤').use()
    print(res)
    assert len(res) > 200


def test_bing():
    res = BingSearch(search_input='蔡徐坤').use()
    print(res)
    assert len(res) > 200