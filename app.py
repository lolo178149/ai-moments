import streamlit as st
import requests
import json

st.set_page_config(page_title="AI 朋友圈生成器", page_icon="🌸")
st.title("🌸 AI 朋友圈文案生成器")

# 在侧边栏让用户输入自己的 Key，保护你的钱包
with st.sidebar:
    st.header("安全设置")
    user_api_key = st.text_input("输入 DeepSeek API Key", type="password")
    st.info("💡 如果你想免费给别人用，也可以在这里写死你的 Key，但风险自担哦！")

topic = st.text_input("你想发什么内容？")
style = st.selectbox("想要什么风格？", ["幽默搞笑", "文艺清新", "凡尔赛", "高端职场"])

if st.button("🚀 立即生成"):
    # 优先使用用户输入的 Key，如果没有则报错
    api_key = user_api_key if user_api_key else "sk-6e232d3669c94b0e9b9b0633f165134b"
    
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": f"主题：{topic}。风格：{style}。请生成朋友圈文案。"}]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        # 这里就是你问的“改哪里”：精准提取 content
        result = response.json()['choices'][0]['message']['content']
        st.success("生成完毕！")
        st.write(result)
    else:
        st.error(f"失败了：{response.text}")