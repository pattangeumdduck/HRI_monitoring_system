import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="병사별 온열손상 위험도", layout="centered")
st.title("📈 병사별 온열손상 위험도 ")

log_dir = "dummy_logs"
file_logs = {}
if os.path.exists(log_dir):
    for fname in os.listdir(log_dir):
        if fname.endswith("_log.csv"):
            soldier_id = fname.replace("_log.csv", "")
            path = os.path.join(log_dir, fname)
            df = pd.read_csv(path)
            df["datetime"] = pd.to_datetime(df["datetime"])
            file_logs[soldier_id] = df.to_dict(orient="records")

# 세션 기반 병사 로그 가져오기
session_logs = st.session_state.get("logs", {})

# 두 소스 병합
combined_ids = list(set(file_logs.keys()) | set(session_logs.keys()))

if not combined_ids:
    st.warning("⚠️ 아직 입력된 병사 기록이 없습니다. '병사 정보 입력'에서 데이터를 추가하세요.")
    st.stop()

# 🔍 전체 병사 요약 테이블
st.subheader("📋 현재 병사별 최신 위험도 요약")
summary = []
for sid in combined_ids:
    records = session_logs.get(sid) or file_logs.get(sid)
    if not records:
        continue
    df = pd.DataFrame(records)
    df["datetime"] = pd.to_datetime(df["datetime"])
    latest = df.sort_values("datetime", ascending=False).iloc[0]
    summary.append({
        "병사 ID": sid,
        "기록 시각": latest["datetime"],
        "위험 점수": latest["risk_score"],
        "위험 등급": latest["risk_level"]
    })
st.dataframe(pd.DataFrame(summary), use_container_width=True)

# 훈련 강도 기준 설정
st.subheader("🧪 훈련/작업 강도 설정")
target_intensity = st.selectbox("훈련 강도 선택", ["low", "medium", "high"])
thresholds = {"low": 7, "medium": 6, "high": 5}

# 위험 병사 필터링
at_risk = [entry for entry in summary if entry["위험 점수"] >= thresholds[target_intensity]]

st.subheader(f"🚨 현재 `{target_intensity}` 강도에 부적절한 병사")
if at_risk:
    st.dataframe(pd.DataFrame(at_risk), use_container_width=True)
else:
    st.success("✅ 현재 기준에서 모든 병사가 안전합니다.")

# 병사 선택 및 이력 시각화
st.subheader("👤 병사별 이력 확인")
selected_id = st.selectbox("병사 선택", combined_ids)
records = session_logs.get(selected_id) or file_logs.get(selected_id)
df = pd.DataFrame(records)
df["datetime"] = pd.to_datetime(df["datetime"])
st.line_chart(df.set_index("datetime")["risk_score"])
st.dataframe(df, use_container_width=True)

# 위험도 기준 설명
with st.expander("📘 위험도 산정 기준 및 배경 설명"):
    st.markdown(
        """
### 🔍 위험도 산정 공식

병사의 피로 및 온열손상 위험도는 다음 요소를 기반으로 산정됩니다:

| 요소 | 기준 | 점수 |
|------|------|------|
| **수면 시간** | 5시간 미만: +2 / 5~6시간: +1 | 🛌 |
| **야간 당직 여부** | 있음: +1 | 🌙 |
| **훈련 강도** | medium: +1 / high: +2 | 🏃 |
| **숙영 여부** | 있음: +2 | ⛺ |
| **기온 (°C)** | 30~34도: +1 / 35도 이상: +2 | 🌡️ |

- 총합 점수로 위험도를 아래와 같이 분류합니다:
    - ✅ **0~3점**: 양호
    - ⚠️ **4~6점**: 주의
    - 🔥 **7점 이상**: 매우 위험

---

이 모델은 실제 데이터 기반은 아니며, 학술적 근거와 임상 경험을 바탕으로 구성된 **시연용 기준 모델**입니다.  
📌 추후 실제 사고 데이터를 바탕으로 **가중치와 변수 보정이 필요**합니다.
        """
    )

