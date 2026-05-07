import streamlit as st
import requests
import json

# 页面基础配置
st.set_page_config(page_title="AI朋友圈文案生成器", page_icon="🌸")
st.title("🌸 AI 朋友圈文案生成器")

# --- 从 Secrets 保险柜自动获取密钥 ---
try:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
except Exception:
    st.error("🔑 未在后台检测到密钥，请检查 Streamlit Secrets 设置。")
    st.stop()
# ----------------------------------

topic = st.text_input("你想发什么内容？", placeholder="例如：去爬山、吃大餐...")
style = st.selectbox("想要什么风格？", ["幽默搞笑", "文艺清新", "凡尔赛", "职场精英"])

if st.button("🚀 立即生成"):
    if not topic:
        st.warning("请先输入你想发的内容哦！")
    else:
        url = "https://api.deepseek.com/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": f"你是一个朋友圈文案大师，擅长写{style}风格的内容。"},
                {"role": "user", "content": f"请围绕这个主题写一段朋友圈：{topic}"}
            ]
        }

        with st.spinner("AI 正在深度思考中..."):
            try:
                response = requests.post(url, headers=headers, data=json.dumps(data))
                if response.status_code == 200:
                    result = response.json()['choices'][0]['message']['content']
                    st.success("✨ 生成成功！")
                    st.info(result)
                    st.caption("💡 提示：长按文字即可复制")
                else:
                    st.error(f"服务器返回错误：{response.status_code}")
            except Exception as e:
                st.error(f"连接出错了：{str(e)}")
