from src.tools import BaiduBaike


def test_baidubaike():
    res = BaiduBaike(search_input='机器学习').use()
    assert res > 100