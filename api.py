import time
import requests
import json
import os
import dotenv


# 다루는 방식 dotenv 채택함
dotenv.load_dotenv()
client_id = os.getenv("ci")
client_secret = os.getenv("cs")


class RTZR:
  def __init__(self,client_id, client_secret):
    self.client_id = client_id
    self.client_secret = client_secret
    self.access_token = ""
    self.stt_id = ""
    
    self.get_access_token()
    self.get_stt_id(self.access_token)
  
  def get_access_token(self):
    resp = requests.post(
        'https://openapi.vito.ai/v1/authenticate',
        data={'client_id': client_id,
            'client_secret': client_secret}
    )
    resp.raise_for_status()
    access_token = resp.json()
    self.access_token = access_token['access_token']
  
  def get_stt_id(self,access_token):
    # 옵션들
    config = {
      "use_itn": False,
      "use_disfluency_filter": False,
      "use_profanity_filter": False,
      "use_paragraph_splitter": True,
    }

    resp = requests.post(
        'https://openapi.vito.ai/v1/transcribe',
        headers={'Authorization': 'bearer '+ access_token},
        data={'config': json.dumps(config)},  #
        files={'file': open('sample.mp3', 'rb')} #파일
    )
    resp.raise_for_status()
    stt_id = resp.json()
  
    self.stt_id = stt_id['id']
    
  def get_scrpit(self):
    while True:
      resp = requests.get(
        'https://openapi.vito.ai/v1/transcribe/'+self.stt_id,
        headers={'Authorization': 'bearer '+ self.access_token},)
      resp.raise_for_status()
      script = resp.json()
      time.sleep(10)
      if (script["status"] == "completed"):
        with open("script.json","w",encoding='UTF-8-sig') as f:
            json.dump(script,f,ensure_ascii = False)
        break
      elif (script["status"] == "transcribing"):
        print("변환중")
      elif(script["status"] == "failed"):
        print("변환 실패!")
        
    
rt = RTZR(client_id,client_secret)
# 객체가 선언되면 stt_id랑 access_token이 결정. 이후 스크립트는 해당 객체에만 함수를 사용하여 대본을 확보.
# 출력을 해보고 null이면 5초 기다렸다가 다시 하고 해서 출력 하기 전까지 무한으로 돌리자.
script = rt.get_scrpit()
 