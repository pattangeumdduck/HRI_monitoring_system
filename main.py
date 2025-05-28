
import streamlit as st

st.set_page_config(page_title="군 장병 온열손상 경보 시스템", layout="centered")
st.title("🧭 군 장병 온열손상 종합 경보 시스템")

st.markdown("""
### 📌 시스템 개요

훈련 중 발생하는 온열손상은 예측이 어렵고 결과는 치명적입니다.  
병사의 건강 상태는 다양해졌지만, 훈련 기준은 여전히 모호합니다.  
지휘 판단을 보조하고 인명사고를 예방하기 위해,  
**병사별 피로도와 위험도를 정량화하고 시각화**하는 시스템이 필요합니다.

이 대시보드는 이를 위해 고안되었습니다.
""")

st.markdown("### 🧭 페이지 안내")
st.page_link("pages/1_add_entry.py", label="➕ 병사 정보 입력", icon="📝")
st.page_link("pages/2_risk_history.py", label="📈 병사별 위험도 이력 조회", icon="📊")
st.page_link("pages/3_stats_dashboard.py", label="📊 통계 요약/분석 대시보드", icon="📉")
st.page_link("pages/4_policy_guide.py", label="🛡️ 지휘관 정책 가이드", icon="📘")
