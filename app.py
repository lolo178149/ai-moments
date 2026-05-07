import streamlit as st
import requests
import json

# --- 1. 页面基础配置 ---
st.set_page_config(page_title="AI朋友圈文案生成器", page_icon="🌸")

# --- 2. 终极屏蔽魔法：隐藏右下角标志、顶部菜单和页脚 ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            /* 强制隐藏右下角部署按钮和状态组件 */
            div[data-testid="stStatusWidget"] {visibility: hidden;}
            .viewerBadge_container__1QS1Y {display: none !important;}
            .stAppDeployButton {display: none !important;}
            #stDecoration {display: none !important;}
            [data-testid="stFooter"] {display: none !important;}
            /* 移除底部留白 */
            .main .block-container {padding-bottom: 0rem;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("🌸 AI 朋友圈文案生成器")

# --- 3. 从后台 Secrets 保险柜自动获取密钥 ---
# 提示：请确保你已经在 Streamlit Cloud 的 Settings -> Secrets 里配置了 DEEPSEEK_API_KEY
try:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
except Exception:
    st.error("🔑 还没在后台保险柜放钥匙哦！请在 Streamlit Secrets 中配置 DEEPSEEK_API_KEY。")
    st.stop()

# --- 4. 界面输入部分 ---
topic = st.text_input("你想发什么内容？", placeholder="例如：今天吃到超好吃的龙虾...")
style = st.selectbox("想要什么风格？", ["幽默搞笑", "文艺清新", "凡尔赛", "职场精英", "小红书爆款"])

# --- 5. 生成逻辑 ---
if st.button("🚀 立即生成"):
    if not topic:
        st.warning("先写点什么吧，不然 AI 没法发挥哦！")
    else:
        url = "https://api.deepseek.com/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": f"你是一个朋友圈文案大师，擅长写{style}风格的内容，会恰当使用 emoji。"},
                {"role": "user", "content": f"请围绕这个主题写一段朋友圈：{topic}"}
            ]
        }

        with st.spinner("✨ AI 正在努力构思中..."):
            try:
                response = requests.post(url, headers=headers, data=json.dumps(data))
                if response.status_code == 200:
                    result = response.json()['choices'][0]['message']['content']
                    st.success("✨ 文案已送达！")
                    # 使用 info 框展示文案，看起来更高级
                    st.info(result)
                    st.caption("💡 提示：在手机上长按上方文字即可复制")
                else:
                    st.error(f"服务器有点小情绪，错误代码：{response.status_code}")
            except Exception as e:
                st.error(f"连接出错了，请检查网络：{str(e)}")
