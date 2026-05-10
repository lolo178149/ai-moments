import streamlit as st
import requests
import json

# 页面设置
st.set_page_config(
    page_title="AI朋友圈文案生成器",
    page_icon="✨"
)

# 标题
st.title("✨ AI朋友圈文案生成器")

st.caption("输入你的状态，让 AI 帮你组织表达。")

# 用户输入
topic = st.text_area(
    "你今天想表达什么？",
    placeholder="例如：今晚第一次把AI网页跑起来了，有点累但挺开心。"
)

# 风格选择
style = st.selectbox(
    "你更想表达什么感觉？",
    [
        "克制自然",
        "有成就感",
        "轻松随意",
        "有点情绪"
    ]
)

# 生成按钮
if st.button("🚀 生成朋友圈文案"):

    # Prompt
    prompt = f"""
你是一个很懂中文表达的人。

用户现在想发一条朋友圈。

【用户内容】
{topic}

【用户想表达的感觉】
{style}

请按照以下感觉去表达：

1. 像一个真实的人在记录某个瞬间
2. 语气自然，不刻意高级
3. 允许有停顿、口语感和留白
4. 可以有一点画面感
5. 可以有轻微隐喻、自嘲或小幽默
6. 不要突然讲大道理
7. 不要像营销号或公众号
8. 情绪像真实生活里的状态
9. 控制在60~120字
10. 可以有一点轻松幽默或自嘲感
11. 偶尔带一点“状态在慢慢变好”的感觉
12. 不要刻意炫耀

请输出3个不同感觉的版本：

① 更克制一点
② 更有生活感一点
③ 更有情绪张力一点

直接输出结果，不要解释。
"""

    # 你的 DeepSeek API Key
    api_key = "sk-6e232d3669c94b0e9b9b0633f165134b"

    # API 地址
    url = "https://api.deepseek.com/chat/completions"

    # 请求头
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # 请求数据
    data = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    # 发送请求
    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(data)
    )

    # 返回结果
    if response.status_code == 200:

        result = response.json()['choices'][0]['message']['content']

        st.success("生成成功！")

        st.write(result)

    else:
        st.error(f"请求失败：{response.text}")
