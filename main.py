import re
import time
from typing import Counter
import pandas as pd
import streamlit as st
import api
import qwen
import matplotlib.pyplot as plt


class stream:
  def __init__(self) -> None:
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
        container1.text_area("대본 내용(원본)", rtzr.script, height=400)

    # 두 번째 열에 컨테이너와 텍스트 영역 추가
    self.qw = qwen.Qwen()
    with col2:
        container2 = st.container()
        container2.markdown("## 발표 피드백")  # 두 번째 제목
        container2.text_area("대본 내용(태깅됨)", "여기에는 태깅된 대본", height=400)
    
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

    # Streamlit의 기본 bar_chart를 사용하여 시각화
    st.bar_chart(data.set_index('단어'))
        
    st.write(self.qw.make_text(rtzr.script))


if __name__ == "__main__":
  stl = stream()
  stl.side_bar()
  
#   rt = api.RTZR(client_id,client_secret)
# # 객체가 선언되면 stt_id랑 access_token이 결정. 이후 스크립트는 해당 객체에만 함수를 사용하여 대본을 확보.
# # 출력을 해보고 null이면 5초 기다렸다가 다시 하고 해서 출력 하기 전까지 무한으로 돌리자.
#   script = rt.get_scrpit()
 

