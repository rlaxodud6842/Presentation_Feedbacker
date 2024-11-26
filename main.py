import altair as alt
import re
import time
from typing import Counter
import pandas as pd
import streamlit as st
import api
import qwen
import matplotlib.pyplot as plt
import streamlit.components.v1 as components


class stream:
  def __init__(self) -> None:
      self.feedback = ""
      st.set_page_config(layout="wide")
      st.title("Presentation Feedbacker")

  def side_bar(self) -> dict:
    st.sidebar.title("발표 영상 업로드")
    
    client_id = st.sidebar.text_input("RTZR API CLIENT_ID 입력",value="jX3PJkmd7apcTSvdnl1A") # RTZR 토큰 획득
    client_secret = st.sidebar.text_input("RTZR API CLIENT_SECRET 입력",value="3Dg0rt_CF_SD0EDKN1ZG38gm-18VQhQ04-oqFXI0")# RTZR 시크릿 획득
    
    # 사이드바에 파일 업로드 기능 추가
    uploaded_video = st.sidebar.file_uploader("발표 영상을 업로드하세요", type=["mp3"])
    if uploaded_video is not None:
      st.sidebar.video(uploaded_video)
      
    if st.sidebar.button("분석하기"):
      if client_id is not None and client_secret and not None and uploaded_video is not None:
        self.rtzr_api(client_id,client_secret,uploaded_video)
  
  def highlight_script(self,script):
    import re
    
    # 태그를 식별하는 정규식
    fil_tag = r"\[([^:\]]+):B-FIL\]"  # 간투어
    rep_tag = r"\[([^:\]]+):B-REP\](?:\s*\[([^:\]]+):I-REP\])*"  # 반복어 (B-REP 및 이어진 I-REP)

    # 하이라이트 스타일
    fil_style = 'background-color: pink;'
    rep_style = 'background-color: skyblue;'

    # 간투어 하이라이트
    script = re.sub(
        fil_tag, 
        r'<span style="' + fil_style + r'">\1</span><span style="font-size: 0.8em; color: gray;"> (간투어)</span>', 
        script
    )

    # 반복어 하이라이트
    def highlight_reps(match):
        words = match.groups()
        highlighted = ' '.join(f'<span style="{rep_style}">{word}</span>' for word in words if word)
        return f"{highlighted}<span style='font-size: 0.8em; color: gray;'> (반복어)</span>"

    script = re.sub(rep_tag, highlight_reps, script)

    # 나머지 태그 제거
    script = re.sub(r"\[.*?:[A-Z-]+\]", "", script)

    return script
  
  def rtzr_api(self, id, secret, uploaded_video):
    rtzr = api.RTZR(id, secret, uploaded_video)

    #로딩 표시
    with st.spinner("대본 생성중..."):
        while True:
            if rtzr.script != "":
                break
            else:
                rtzr.get_scrpit()
                time.sleep(3)  # 대본을 가져오는 동안 3초마다 재시도

    st.success("대본 생성 완료!")
    
        # 두 개의 열 생성
    col1, col2 = st.columns(2)

    # 첫 번째 열에 컨테이너와 텍스트 영역 추가
    with col1:
        container1 = st.container()
        container1.markdown("## 음성 변환 대본")  # 첫 번째 제목
        components.html(rtzr.script,height=400)

    # 두 번째 열에 컨테이너와 텍스트 영역 추가
    
    with col2:
        container2 = st.container()
        container2.markdown("## 문제점 포착")  # 두 번째 제목
        # Custom HTML 표시
        components.html(f"<div style='font-size: 16px;'>{self.highlight_script("""
                                                                [안녕:B-REP] [안녕하세요:I-REP] 저는 ai학과 20학 20학번 [강창:B-REP] [강창열입니다.:I-REP]
                                                                저는 cnn cnn에 대해 설명해보겠습니다.
                                                                cnn은 컨볼루 [컨볼루션:I-REP] 뉴럴 네트워크입니다.
                                                                [감사합:B-REP] [감사합니다.:I-REP]
                                                                [어:B-FIL] cnn은 아주 [어렵:B-REP] [어렵습니다.:I-REP]
                                                                저도 잘 모릅니 모릅니다. [어:B-FIL]
                                                                [음:B-FIL] [아:B-FIL] 감사합니다.
                                                                [음:B-FIL] 안녕하세요 저는 이금정 입니다 [만나서:I-REP] 반갑습 [아니:I-REP] [반갑습니다.:I-REP]
                                                                이 부분에 대해서는 [아:B-FIL] 저도 잘 모르는데요.
                                                                [하:B-REP] [질문받겠습니다.:I-REP]
                                                                그 부분에 대해서 설명드리 설명드리겠습니다.
                                                                제가 그 부분에 대해서 공부해봤 [공부해봤는데요.:I-REP]
                                                                죄송합니 죄송합니다. 잘 모르겠 모르겠습니다.
                                                                [아:B-FIL] [음:B-FIL] [어:B-FIL] [감사합:I-REP] [감사합니다.:I-REP]
                                                                 """)}</div>", height=400)
    
    words = re.findall(r'\b\w+\b', rtzr.script.lower())  # 단어 분리 및 소문자 변환
    word_counts = Counter(words)
    
        # 가장 많이 사용된 단어 상위 10개
    top_n = 10
    most_common = word_counts.most_common(top_n)
    words, counts = zip(*most_common)

    # 빈도수를 pandas DataFrame으로 변환
    data = pd.DataFrame({
        '단어': words,
        '빈도수': counts
    })

    # Altair 차트 생성
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('단어:N', title='단어', sort='-y'),
        y=alt.Y('빈도수:Q', title='빈도수'),
        color='빈도수:Q',
        tooltip=['단어', '빈도수']
    ).properties(
        width=1600,
        height=400,
        title="단어 빈도수 상위 10개"
    )
    st.altair_chart(chart)
    
    self.qw = qwen.Qwen()
    with st.spinner("AI 피드백 생성중..."):
        while True:
            if self.feedback != "":
                break
            else:
                self.feedback = self.qw.make_text(rtzr.script)
                time.sleep(15)  # 대본을 가져오는 동안 3초마다 재시도
    st.success("AI 피드백 완료")
    col3, = st.columns(1)
    with col3:
      container3 = st.container()
      container3.markdown("##"+self.feedback)  # 첫 번째 제목


if __name__ == "__main__":
  stl = stream()
  stl.side_bar()
  
#   rt = api.RTZR(client_id,client_secret)
# # 객체가 선언되면 stt_id랑 access_token이 결정. 이후 스크립트는 해당 객체에만 함수를 사용하여 대본을 확보.
# # 출력을 해보고 null이면 5초 기다렸다가 다시 하고 해서 출력 하기 전까지 무한으로 돌리자.
#   script = rt.get_scrpit()
 

