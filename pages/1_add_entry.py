
import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="병사 정보 입력", layout="centered")
st.title("➕ 병사 위험 정보 입력 ")

# 세션 상태 초기화
if "logs" not in st.session_state:
    st.session_state.logs = {}

soldier_id = st.text_input("👤 병사 ID", value="SOLDIER_011")

sleep_hours = st.slider("🛌 수면 시간 (시간)", 0, 10, 6)
night_duty = st.checkbox("🌙 최근 야간 당직 여부")
training_intensity = st.selectbox("🏃 훈련 강도", ["low", "medium", "high"])
camping = st.checkbox("⛺ 숙영 훈련 여부")
temperature = st.slider("🌡️ 외부 기온 (°C)", 20.0, 40.0, 30.0, step=0.1)

def assess_risk(sleep_hours, night_duty, training_intensity, camping, temperature):
    score = 0
    if sleep_hours < 5:
        score += 2
    elif sleep_hours < 6:
        score += 1
    if night_duty:
        score += 1
    if training_intensity == "high":
        score += 2
    elif training_intensity == "medium":
        score += 1
    if camping:
        score += 2
    if temperature >= 35:
        score += 2
    elif temperature >= 30:
        score += 1

    if score >= 7:
        level = "🔥 매우 위험"
    elif score >= 4:
        level = "⚠️ 주의"
    else:
        level = "✅ 양호"
    return score, level

if st.button("기록 저장"):
    risk_score, risk_level = assess_risk(
        sleep_hours, night_duty, training_intensity, camping, temperature
    )
    entry = {
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "sleep_hours": sleep_hours,
        "night_duty": night_duty,
        "training_intensity": training_intensity,
        "camping": camping,
        "temperature": temperature,
        "risk_score": risk_score,
        "risk_level": risk_level
    }
    if soldier_id not in st.session_state.logs:
        st.session_state.logs[soldier_id] = []
    st.session_state.logs[soldier_id].append(entry)
    st.success(f"{soldier_id}의 기록이 세션에 저장되었습니다.")
