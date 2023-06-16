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
  session = Session()
  # 添加输出终端
  session.add_handler(Shell())
  # 初始化工具 
  tools = [
      BaiduBaike # 在这选择工具
      ... 
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

  ```
- 运行 >> `python main.py`

### 工具列表
- 百度百科
  <div align=center>
    <img src="https://github.com/jiran214/gpt-func-calling/blob/main/public/img.png" width="800" height="300"/><br/>
  </div>
- 正在开发中...
## 更新日志
## to do list
- [ ] playwright 引入
## Contact Me
- 请先star本项目~~
- **如果你遇到各种问题，请提issues，一般的问题不要加我，感谢理解！**
- 欢迎加我WX：yuchen59384 交流！

