import time
import streamlit as st
import api

class stream:
  def __init__(self) -> None:
     pass
   
  def side_bar(self) -> dict:
    st.sidebar.title("발표 영상 업로드")
    
    client_id = st.sidebar.text_input("RTZR API CLIENT_ID 입력") # RTZR 토큰 획득
    client_secret = st.sidebar.text_input("RTZR API CLIENT_SECRET 입력")# RTZR 시크릿 획득
    
    # 사이드바에 파일 업로드 기능 추가
    uploaded_video = st.sidebar.file_uploader("발표 영상을 업로드하세요", type=["mp4", "mov", "avi", "mkv","mp3"])
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
    
    # 하나의 컨테이너에 대본 출력
    container = st.container()
    container.markdown("## 음성 변환 대본")  # 제목 추가
    
    # 대본 내용을 텍스트 영역으로 출력
    container.text_area("대본 내용", rtzr.script, height=400)

if __name__ == "__main__":
  stl = stream()
  stl.side_bar()
#   rt = api.RTZR(client_id,client_secret)
# # 객체가 선언되면 stt_id랑 access_token이 결정. 이후 스크립트는 해당 객체에만 함수를 사용하여 대본을 확보.
# # 출력을 해보고 null이면 5초 기다렸다가 다시 하고 해서 출력 하기 전까지 무한으로 돌리자.
#   script = rt.get_scrpit()
 

