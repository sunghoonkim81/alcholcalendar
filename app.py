import streamlit as st
import pandas as pd
import calendar
from datetime import datetime
import os

# 파일 저장 설정
DATA_FILE = "health_log.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["date", "alcohol", "coffee"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

st.set_page_config(page_title="달력 체크", layout="wide")

# CSS로 모바일에서 더 예쁘게 보이게 설정
st.markdown("""
    <style>
    .stCheckbox { margin-bottom: -15px; }
    div[data-testid="column"] { padding: 5px; border: 1px solid #f0f2f6; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📅 월간 음주 & 커피 기록")

# 날짜 선택기
today = datetime.now()
col_y, col_m = st.columns(2)
with col_y:
    year = st.selectbox("연도", range(2024, 2030), index=2) # 2026년 기준
with col_m:
    month = st.selectbox("월", range(1, 13), index=today.month - 1)

df = load_data()

# 달력 생성
cal = calendar.monthcalendar(year, month)
days = ["월", "화", "수", "목", "금", "토", "일"]

# 요일 표시
cols = st.columns(7)
for i, day_name in enumerate(days):
    cols[i].write(f"**{day_name}**")

# 달력 날짜 칸 생성
for week in cal:
    cols = st.columns(7)
    for i, day in enumerate(week):
        if day == 0:
            cols[i].write("")
        else:
            date_str = f"{year}-{month:02d}-{day:02d}"
            
            # 기존 데이터 가져오기
            existing = df[df['date'] == date_str]
            alc_val = bool(existing.iloc[0]['alcohol']) if not existing.empty else False
            cof_val = bool(existing.iloc[0]['coffee']) if not existing.empty else False
            
            # 날짜 칸 구성
            with cols[i]:
                st.write(f"**{day}**")
                new_alc = st.checkbox("🍺", value=alc_val, key=f"alc_{date_str}")
                new_cof = st.checkbox("☕", value=cof_val, key=f"cof_{date_str}")
                
                # 변경 시 자동 저장
                if new_alc != alc_val or new_cof != cof_val:
                    if not existing.empty:
                        df.loc[df['date'] == date_str, ['alcohol', 'coffee']] = [new_alc, new_cof]
                    else:
                        new_row = pd.DataFrame([{"date": date_str, "alcohol": new_alc, "coffee": new_cof}])
                        df = pd.concat([df, new_row], ignore_index=True)
                    save_data(df)
                    st.rerun()

st.divider()
st.info("💡 체크박스를 클릭하면 즉시 저장됩니다. PC와 모바일에서 동일하게 확인하세요!")