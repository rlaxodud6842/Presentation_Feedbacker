import time
import requests
import json
import requests

#dotenv 쓰지않고 Streamlit 내에서 처리하고 끝냄

class RTZR:
  def __init__(self,client_id, client_secret,presentation_file):
    self.client_id = client_id
    self.client_secret = client_secret
    self.access_token = ""
    self.stt_id = ""
    self.script = ""
    self.presentation_file = presentation_file
    
    self.get_access_token()
    self.get_stt_id(self.access_token)
  
  
  def get_access_token(self):
    resp = requests.post(
        'https://openapi.vito.ai/v1/authenticate',
        data={'client_id': self.client_id,
            'client_secret': self.client_secret}
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
        files={'file': (self.presentation_file.name, self.presentation_file, self.presentation_file.type)} #파일
    )
    resp.raise_for_status()
    stt_id = resp.json()
  
    self.stt_id = stt_id['id']

    
  def get_scrpit(self):
    resp = requests.get(
      'https://openapi.vito.ai/v1/transcribe/'+self.stt_id,
      headers={'Authorization': 'bearer '+ self.access_token},)
    resp.raise_for_status()
    script = resp.json()
    string = ""
    if (script["status"] == "completed"):
      for i in range(len(script['results']['utterances'])):
        string += script['results']['utterances'][i]['msg']
      self.script = string


