# gpt-func-calling 

![](https://img.shields.io/badge/license-GPL-blue)

## 简介
利用ChatGPT最新的function-calling，实现类似LangChain Agent代理功能，通过tool补充上下文

## 安装
### 环境
- win 10
- python 3.8
- vpn全局代理
### pip安装依赖
```shell
git clone https://github.com/jiran214/gpt-func-calling
cd src
# 建议使用命令行或者pycharm创建虚拟环境，参考链接 https://blog.csdn.net/xp178171640/article/details/115950985
python -m pip install --upgrade pip pip
pip install -r .\requirements.txt
```
### 新建config.ini 
- src目录下重命名config.sample.ini为config.ini
- 更改api_key和proxy
## 快速开始
- 运行 >> `cd src`
- 修改 main.py 内容
  ```python 
  
  ...
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
  ```
- 运行 >> `python main.py`
- 在终端输入第一个问题

### 工具列表
- 百度百科
  <div align=center>
    <img src="https://github.com/jiran214/gpt-func-calling/blob/main/public/img.png" width="900" height="200"/><br/>
  </div>
- 网易新闻 
- 百度百科 
- csdn 
- 掘金 
- 谷歌
- Bing
- 正在开发中...

## 更新日志
## to do list
- [x] playwright 引入，简化爬虫
- [ ] 工具输出的内容长度自由选择
- [ ] 对工具输出做summary
- [ ] 交互式对话，保留一定窗口大小
- [ ] 前端界面
## Contact Me
- 请先star本项目~~
- **如果你遇到各种问题，请提issues，一般的问题不要加我，感谢理解！**
- 如果你有好的建议和想法，欢迎加我WX：yuchen59384 交流！

