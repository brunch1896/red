import openai
import streamlit as st
import os

from bs4 import BeautifulSoup
import requests
import re

# html_code = """
# <div class="post_body">
#     <p id="246FH0Q9"><strong>财联社9月22日讯（编辑 史正丞）</strong>当地时间周四，美国科技公司微软在纽约举办秋季发布会，除了常规的Surface硬件升级外，今天的重头戏依然是AI。</p>
#     <p class="f_center"><img src="https://nimg.ws.126.net/?url=http%3A%2F%2Fdingyue.ws.126.net%2F2023%2F0922%2Ffda5674ej00s1co1o000mc000f600dyg.jpg&thumbnail=660x2147483647&quality=80&type=jpg"/><br/></p>
#     <p class="f_center"><img src="https://nimg.ws.126.net/?url=http%3A%2F%2Fdingyue.ws.126.net%2F2023%2F0922%2Fe3a04b2cj00s1co1o001ic000x300gpg.jpg&thumbnail=660x2147483647&quality=80&type=jpg"/><br/></p>
# </div>
# <div class="post_statement">
#     <span class="bg"></span>
#     <p>特别声明：以上内容(如有图片或视频亦包括在内)为自媒体平台“网易号”用户上传并发布，本平台仅提供信息存储服务。</p>
#     <p>Notice: The content above (including the pictures and videos if any) is uploaded and posted by a user of NetEase Hao, which is a social media platform and only provides information storage services.</p>
# </div>
# """



def get_completion_from_messages(messages, 
                 model="gpt-3.5-turbo", 
                 temperature=0, 
                 max_tokens=1000):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens,
    )
    # return response.choices[0].message["content"]
    return response

# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
#     "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
#     "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
#     "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"


st.title("👸 红楼梦总结器")
# openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

images = [
        "1.png",
        "2.png",
        # "image3.jpg",
        # "image4.jpg",
        # "image5.jpg"
    ]

    # 初始化轮播索引
index = 0

# 创建轮播图区域
image_area = st.sidebar.empty()

image_area.image(images[index])


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "请输入你想总结的新闻网址"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    # if not openai_api_key:
    #     st.info("Please add your OpenAI API key to continue.")
    #     st.stop()

    # openai.api_key = openai_api_key

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }
    url = prompt
    text = str(requests.get(url, headers=header).text)

    soup = BeautifulSoup(text, 'html.parser')

    # 找到正文内容所在的标签
    content_tag = soup.find("div", id="content")

    # 提取正文内容
    # 使用正则表达式去掉非中文字符


    # 使用正则表达式只保留中文字符和标点符号
    pattern = re.compile(r'[\u4e00-\u9fa5，。、；：“”‘’！？]+')
    content = ''.join(pattern.findall(content_tag.text))



    openai.api_key = os.getenv('OPENAI_API_KEY') 
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    # response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    response = get_completion_from_messages([
  {"role":"system","content": """用生动的写法将下面的文章总结为一个含有不多于8句话的段落，注意，只能写8句话以内，最多8句话。"""},
  {"role":"user","content": content}
  ])
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content)