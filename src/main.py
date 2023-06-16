from enums import Role
from handlers import Shell
from llm import GPTAgent
from session import Session
from tools import BaiduBaike

# 新建会话窗口
session = Session()
# 添加输出终端
session.add_handler(Shell())
# 初始化工具
tools = [
    BaiduBaike
]
# 创建代理
agent = GPTAgent.from_tools(
    tools=tools,
    session=session
)
# 创建消息
message = {
    'role': Role.USER.value,
    'content': '蔡徐坤是谁'  # 在这输入第一个问题
}
# 添加到会话窗口
session.add_message(message)
# 启动代理
agent.run()
