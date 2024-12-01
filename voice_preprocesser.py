import os
import subprocess
import tempfile
from pydub import AudioSegment

def process_audio_with_ffmpeg(uploaded_video, volume_choice):
    try:
        # 업로드된 MP3 파일을 임시 디렉토리에 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_input_file:
            temp_input_file.write(uploaded_video.read())
            input_file_path = temp_input_file.name

        # 볼륨 조정: ffmpeg 명령어로 볼륨 조정
        volume_map = {"큼": "-20dB", "작음": "20dB", "중간": "0dB"}
        volume_option = volume_map.get(volume_choice, "0dB")

        # 출력 파일 경로
        output_file_path = os.path.join(tempfile.gettempdir(), "processed_audio.mp3")

        # ffmpeg 명령어 실행 (볼륨 조정)
        ffmpeg_command = [
            "ffmpeg", "-i", input_file_path, "-filter:a", f"volume={volume_option}", output_file_path
        ]
        subprocess.run(ffmpeg_command, check=True)

        # 대역 필터 적용 (고역 및 저역 필터)
        filtered_file_path = os.path.join(tempfile.gettempdir(), "filtered_audio.mp3")
        
        # 고역 필터와 저역 필터를 ffmpeg 명령어로 적용
        filter_command = [
            "ffmpeg", "-i", output_file_path,
            "-filter:a", "highpass=f=300, lowpass=f=3400",
            filtered_file_path
        ]
        subprocess.run(filter_command, check=True)

        # 필터링된 MP3 파일을 읽어오기
        with open(filtered_file_path, "rb") as f:
            processed_audio = f.read()

        # 임시 파일 정리
        os.remove(input_file_path)  # 입력 파일 삭제
        os.remove(output_file_path)  # 볼륨 조정된 파일 삭제
        os.remove(filtered_file_path)  # 필터링된 파일 삭제

        return processed_audio

    except Exception as e:
        print(f"오류 발생: {e}")
        return None
