from src.tools.bai_ke import BaiduBaike


def test_baidubaike():
    res = BaiduBaike(search_input='蔡徐坤').use()
    print(res)
    assert len(res) > 100