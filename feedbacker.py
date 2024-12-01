import re

# REP 및 FIL 태그를 세는 함수
def count_tags(text):
    rep_count = len(re.findall(r'\[.*?:B-REP\]', text)) + len(re.findall(r'\[.*?:I-REP\]', text))
    fil_count = len(re.findall(r'\[.*?:B-FIL\]', text)) + len(re.findall(r'\[.*?:I-FIL\]', text))
    return rep_count, fil_count

# 발표 평가 함수
def evaluate_presentation(text):
    rep_count, fil_count = count_tags(text)
    
    # 발표 평가 기준
    if rep_count <= 2 and fil_count <= 2:
        evaluation = "잘된 발표"
    elif rep_count <= 4 and fil_count <= 3:
        evaluation = "괜찮은 발표"
    else:
        evaluation = "매끄럽지 않은 발표"
    
    return evaluation, rep_count, fil_count

def get_feedback(taged_script):
    evaluation, rep_count, fil_count = evaluate_presentation(taged_script)
    feedback = f"반복어 횟수 : {rep_count}번 간투어 횟수 : {fil_count}번 이번발표는 {evaluation}"
    return feedback
