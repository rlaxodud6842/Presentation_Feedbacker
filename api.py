import requests


class RTZR:
    def __init__(self):
        self.url = "https://openapi.vito.ai/v1/transcribe"       # API URL
        self.token = "YOUR_JWT_TOKEN"  # 여기에 실제 JWT 토큰을 입력
    
    def get_file_path(self):
        # 파일 경로
        file_path = "sample.wav"
        # 이건 나중에 핸들러 만들어서 분리할것.
    
    def get_header(self):
        # 요청 헤더
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        return headers
    
    def get_files(self):
        # 요청 데이터
        files = {
            "file": open(self.get_file_path(), "rb"),
            "config": ('', '{"model_name": "sommers"}'),  # config는 문자열로 전송
        }
        return files
    
    def post(self):
    # POST 요청
        response = requests.post(self.url, headers=self.get_headers(), files=self.get_files())
        # 응답 확인
        if response.status_code == 200:
            print("Transcription successful:")
            print(response.json()) # 응답 결과
        else:
            #실패 코드
            print(f"Error {response.status_code}: {response.text}")
        
