import streamlit as st
import pandas as pd
import calendar
from datetime import datetime

# 1. 구글 스프레드시트 연결 설정 (본인의 시트 주소로 교체하세요!)
# 시트의 "공유" 설정을 "링크가 있는 모든 사용자 - 편집자"로 꼭 바꿔야 합니다.
GSHEET_ID = "여기에_아까_복사한_ID를_넣으세요"
GSHEET_URL = f"https://docs.google.com/spreadsheets/d/1pbodbvWOsfpZzuNhHpizzOHV5CvUf17BCB3TEBNXte0/gviz/tq?tqx=out:csv"

# 데이터를 구글 시트에 저장하는 기능은 'st.connection'이나 복잡한 인증이 필요하지만,
# 가장 쉬운 방법은 'gsheetsdb' 대신 아래의 방식을 쓰는 것입니다.
# 하지만 여기서는 '누구나 편집 가능'한 링크를 활용한 저장 방식을 안내해 드립니다.

def load_data():
    try:
        # 시트에서 데이터 읽어오기
        return pd.read_csv(GSHEET_URL)
    except:
        return pd.DataFrame(columns=["date", "alcohol", "coffee"])

# 저장 기능 (구글 시트 API 설정 없이 가장 간단하게 하는 법은 사실 수동 저장 형식이지만, 
# 여기서는 웹앱의 편리함을 위해 'st.connection' 설정을 권장합니다.)
# 일단은 화면 구성을 먼저 업데이트해 드릴게요.