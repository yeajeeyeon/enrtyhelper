import streamlit as st
import google.generativeai as genai

# ================================
# 기본 설정
# ================================
st.set_page_config(page_title="엔트리 튜터", page_icon="🤖")

st.title("🤖 엔트리 코딩 도우미")
st.caption("정답 대신 힌트로 생각하는 힘을 길러줍니다! (Powered by Gemini)")

# ================================
# API 키 설정
# ================================
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.text_input("Google API Key를 입력하세요", type="password")

if not api_key:
    st.info("챗봇을 사용하려면 API 키가 필요합니다.")
    st.stop()

genai.configure(api_key=api_key)

# ================================
# 시스템 역할(페르소나) 정의
# ================================
system_instruction = """
당신은 초등학생과 중학생을 위한 친절한 '엔트리(Entry) 코딩 선생님'입니다.

[행동 지침]
1. 학생에게 정답 블록 코드를 절대로 직접 제공하지 않습니다.
2. 대신 단계별 힌트, 사고 과정, 블록 종류 안내 정도만 제공합니다.
3. '움직임', '흐름', '조건' 같은 엔트리 용어를 사용하여 안내합니다.
4. KNN 등 어려운 개념은 '유유상종', '비슷한 친구 찾기' 같은 쉬운 비유로 설명합니다.
5. 항상 존댓말을 사용하고 학생을 격려합니다.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

# ================================
# 대화 기록 초기화
# ================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# 기존 메시지 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ================================
# 사용자 입력 처리
# ================================
if prompt := st.chat_input("엔트리 코딩하다가 막힌 부분을 물어보세요!"):
    # 사용자 메시지 저장 및 출력
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # 최신 방식: generate_content() 사용
        response = model.generate_content(prompt)

        answer = response.text

        # AI 응답 출력 및 저장
        with st.chat_message("assistant"):
            st.write(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})

    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")
