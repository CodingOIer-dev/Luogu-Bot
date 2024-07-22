# Luogu-Bot

基于洛谷的机器人。

<br />

<p align="center">
  <a href="https://www.luogu.com.cn/chat?uid=754324">
    <img src="https://fecdn.luogu.com.cn/luogu/logo.png" alt="Logo" height="80">
  </a>
  <h3 align="center">洛谷机器人</h3>
  <p align="center">
    为你的在洛谷的 OI 生活增加一份乐趣
    <br />
    <a href="https://github.com/CodingOIer/Luogu-Bot"><strong>探索本项目的文档 »</strong></a>
    <br />
    <br />
    <a href="https://www.luogu.com.cn/chat?uid=754324">查看 Demo</a>
    ·
    <a href="https://github.com/CodingOIer/Luogu-Bot/issues">报告 Bug</a>
    ·
    <a href="https://github.com/CodingOIer/Luogu-Bot/issues">提出新特性</a>
  </p>

</p>


 本篇 README.md 面向开发者

### 上手指南

###### 开发前的配置要求

1. 在本地运行洛谷本地代理，仓库链接：[CodingOIer/Luogu-Proxy (github.com)](https://github.com/CodingOIer/Luogu-Proxy)
2. 安装依赖 `pip install requests, openai, loguru`。

###### **安装步骤**

1. 准备一台云服务器。

2. 获取一个 DeepSeek API Key。（[DeepSeek 开放平台](https://platform.deepseek.com)）

3. 克隆本仓库。

   ```shell
   git clone https://github.com/CodingOIer/Luogu-Bot.git
   cd Luogu-Bot/src
   ```

4. 编写 `settings.json` 形如：

   ```json
   {
       "_uid": 754324,
       "__client_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
       "deepseek-key": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
       "max_token": 4096,
       "command": {
           ":on": "~ 已开启自动回复",
           ":off": "~ 已关闭自动回复",
           ":clear": "~ 已清除上下文",
           ":help": "~ 帮助文档位于 https://luogu.codingoier.work/bot/help.pdf"
       },
       "tips": "你好 {username}，我是 {root}，我现在在信息学社区洛谷和你进行对话，我会保持必要的礼节，适当的拒绝不必要的请求。"
   }
   ```

   > [!TIP]
   >
   > `tips` 中的 `{username}` 会被替换为正在对话的用户，`{root}` 会被替换为当前的机器人用户名。

5. 运行。

   ```shell
   python server.py
   ```

   

### 部署

暂无

### 使用到的框架

暂无

#### 如何参与开源项目

目前本项目仍处于开发初期，所以暂时不接受 PR，但是你可以提出 issue。

### 版本控制

该项目使用 `Git` 进行版本管理。您可以在 `repository` 参看当前可用版本。

### 作者

wanghongtiancodingoier@outlook.com

洛谷：[CodingOIer](https://www.luogu.com.cn/)

 *您也可以在贡献者名单中参看所有参与该项目的开发者。*

### 版权说明

该项目签署了 GNU GPLv3 授权许可，详情请参阅 [LICENSE.txt](https://github.com/CodingOIer/Luogu-Bot/blob/main/LICENSE.txt)

### 鸣谢


- [Luogu](https://www.luogu.com.cn)
