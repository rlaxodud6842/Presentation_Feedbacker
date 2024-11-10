import json

path = "./script.json"
with open(path, "r", encoding="utf-8-sig") as json_file:
    json_data = json.load(json_file)  # 파일 내용을 파싱하여 딕셔너리 형태로 불러오기
    
for i in range(20): #json 특정 기준을 세워서 msg를 추출해야함.
    print(json_data['results']['utterances'][i]['msg'])
    
#json으로 관리를 해서 서버딴에서 스크립트 관리 -> 맞는건가

