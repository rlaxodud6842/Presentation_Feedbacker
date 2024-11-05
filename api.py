import requests
import json
import requests

client_id = '[client id]'
client_secret = '[client secert]'

class RTZR:
  def __init__(self,client_id, client_secret):
    self.client_id = client_id
    self.client_secret = client_secret
  
  def get_access_token(self):
    resp = requests.post(
        'https://openapi.vito.ai/v1/authenticate',
        data={'client_id': client_id,
            'client_secret': client_secret}
    )
    resp.raise_for_status()
    access_token = resp.json()
    return access_token['access_token']
  
  def get_stt_token(self,access_token):
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
    return stt_id['id']
  
  def get_scrpit(self,stt_id,access_token):
    resp = requests.get(
        'https://openapi.vito.ai/v1/transcribe/'+stt_id,
        headers={'Authorization': 'bearer '+ access_token},
    )
    resp.raise_for_status()
    print(resp.json())
    
    
rt = RTZR(client_id,client_secret)


access_token = rt.get_access_token()
stt_id = rt.get_stt_token(rt.get_access_token())
script = rt.get_scrpit(stt_id,access_token)

 