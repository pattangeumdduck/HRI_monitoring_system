
import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title="📊 통계 대시보드", layout="wide")
st.title("📊 병사 위험도 통계 대시보드")

log_dir = "dummy_logs"
file_logs = {}
if os.path.exists(log_dir):
    for fname in os.listdir(log_dir):
        if fname.endswith("_log.csv"):
            soldier_id = fname.replace("_log.csv", "")
            path = os.path.join(log_dir, fname)
            df = pd.read_csv(path)
            df["datetime"] = pd.to_datetime(df["datetime"])
            file_logs[soldier_id] = df

session_logs = st.session_state.get("logs", {})
for sid, records in session_logs.items():
    df = pd.DataFrame(records)
    df["datetime"] = pd.to_datetime(df["datetime"])
    if sid in file_logs:
        file_logs[sid] = pd.concat([file_logs[sid], df])
    else:
        file_logs[sid] = df

if not file_logs:
    st.warning("⚠️ 데이터가 없습니다.")
    st.stop()

all_df = pd.concat(file_logs.values(), keys=file_logs.keys(), names=["soldier_id"])

st.subheader("1️⃣ 위험도 점수 히스토그램")
fig, ax = plt.subplots()
all_df["risk_score"].hist(bins=10, ax=ax)
st.pyplot(fig)

st.subheader("2️⃣ 시간대별 평균 위험 점수 추이")
time_df = all_df.groupby("datetime")["risk_score"].mean().reset_index()
st.line_chart(time_df.set_index("datetime"))

st.subheader("3️⃣ 고위험 병사 수 변화 추이 (risk_score >= 7)")
high_risk = all_df[all_df["risk_score"] >= 7]
count_df = high_risk.groupby("datetime").size().reset_index(name="count")
st.line_chart(count_df.set_index("datetime"))

st.subheader("4️⃣ 요일별 평균 수면시간 / 기온")
all_df["weekday"] = all_df["datetime"].dt.day_name()
summary = all_df.groupby("weekday")[["sleep_hours", "temperature"]].mean()
st.dataframe(summary)
