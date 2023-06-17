from utils.enums import Role
from handlers import Shell
from llm import GPTAgent
from sessions import Session, InteractiveSession
from tools import (
    WangYiNews,
    BaiduBaike,
    CSDN,
    JueJin,
    GoogleSearch,
    BingSearch,
)

# 新建会话窗口
session = InteractiveSession()
# 添加输出终端
session.add_handler(Shell())
# 初始化工具
tools = [
    WangYiNews,  # 网易新闻
    BaiduBaike,  # 百度百科
    CSDN,  # csdn
    JueJin,  # 掘金
    GoogleSearch,  # 谷歌 需要在config.ini -> google 配置api，详见 https://zhuanlan.zhihu.com/p/174666017
    BingSearch,  # Bing
    # 持续开发中...
]
# 创建代理
agent = GPTAgent.from_tools(
    tools=tools,
    session=session
)
# 添加到会话窗口
session.get_input()
# 启动代理
agent.forever_run()
