from moudles import browser


def test_browser():
    print(1)
    res = browser.goto('https://www.baidu.com')
    print(res)
    # print(res)