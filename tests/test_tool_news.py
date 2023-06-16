from tools import WangYiNews


def test_163():
    res = WangYiNews(search_input='明星').use()
    print(res)
    assert len(res) > 100