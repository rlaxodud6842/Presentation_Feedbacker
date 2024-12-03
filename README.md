# Presentation_Feedbacker
발표에 대한 피드백을 AI가 객관적으로 해주는 웹 어플리케이션

## 프로젝트 목표
RTZR_Sommers, Kobert, Qwen 2.5 모델 등을 활용하여 사용자에게 발표에 대한 피드백을 해주는 웹 기반 어플리케이션.
반복어, 간투어 등을 기반으로 피드백 해주며, Qwen 2.5 모델이 발표에 대한 피드백을 생성하여 사용자에게 출력.

## 프로젝트 사진
![image](https://github.com/user-attachments/assets/5f95a475-a63b-4b34-affa-c5fe1c47ab51)

### 기대효과 
> AI의 객관적인 피드백과 더불어 간투어나 반복어에 대한 인지를 통해 발표 기술 향상.

## 아키텍처
![image](https://github.com/user-attachments/assets/0e56a33c-e473-4e79-a0da-42ed7cacfe26)

## 개발 스택
> Python, Pytorch, Streamlit, Flask<br> 

## 핵심 기능 
>
> 발표 영상 텍스트화 = STT(Speach To text)<br>
> 텍스트화 된 스크립트에 대한 피드백<br>
> Kobert 모델에 의해 간투어, 반복어 태깅.<br>
> Streamlit으로 웹 구현, Kobert환경 서버에 Spooling 방식으로 15초 마다 Request.<br>
> Qwen 2.5 모델을 통한 피드백 생성.
