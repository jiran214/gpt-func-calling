from utils.enums import Role
from handlers import Shell
from llm import GPTAgent
from session import Session
from src.tools import (
    WangYiNews,
    BaiduBaike,
    CSDN,
    JueJin,
    GoogleSearch,
    BingSearch,
)

# 新建会话窗口
session = Session()
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
# 创建消息
message = {
    'role': Role.USER.value,
    'content': 'bing上搜索人工智能是什么?'  # 在这输入第一个问题
}
# 添加到会话窗口
session.add_message(message)
# 启动代理
agent.run()
