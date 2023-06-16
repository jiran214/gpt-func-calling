from tools.program import CSDN, JueJin


def test_csdn():
    res = CSDN(search_input='python').use()
    print(res)
    assert len(res) > 100


def test_juejin():
    res = JueJin(search_input='python').use()
    print(res)
    assert len(res) > 100