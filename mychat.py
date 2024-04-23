import os
from openai import OpenAI
import streamlit as st
import time
import speech_recognition as sr

os.environ['OPENAI_API_KEY'] = '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'

API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=API_KEY)

thread_id = "thread_TDg8kHueNxzH1173lunhFtgS"
assistant_id = "asst_eA6qZL3AHPoWqUGfGJQ46LFt"


st.header("RPA-KOREA의 GPT4")


recognizer = sr.Recognizer()

def load_messages():

    thread_messages = client.beta.threads.messages.list(thread_id)

    for msg in reversed(thread_messages.data):
        with st.chat_message(msg.role):
            st.write(msg.content[0].text.value)

load_messages()


if st.button('음성으로 입력하기'):
    with sr.Microphone() as source:
        st.write("음성인식 시작")
        audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio, language='ko-KR')
        st.session_state['recognized_text'] = recognized_text  # 인식된 텍스트를 세션 상태에 저장
    except sr.UnknownValueError:
        st.error("음성 인식에 실패했습니다. 다시 시도해주세요.")
    except sr.RequestError as e:
        st.error(f"음성 인식 서비스에 문제가 발생했습니다: {e}")


user_input = st.text_input(" ", value=st.session_state.get('recognized_text', ''), key='user_input')


submit_button = st.button("GPT에게 물어보기")

if submit_button and user_input:
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_input
    )


    with st.chat_message(message.role):
        st.write(message.content[0].text.value)


    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )


    while run.status != "completed":
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )


    messages = client.beta.threads.messages.list(thread_id)
    with st.chat_message(messages.data[0].role):
        st.write(messages.data[0].content[0].text.value)

  
    st.session_state['recognized_text'] = ''
    st.experimental_rerun()
