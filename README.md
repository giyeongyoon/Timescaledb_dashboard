# 🌱 실시간 토양 수분 센서 대시보드

IoT 기반 실시간 **토양 수분 센서** 데이터를 수집하여 **TimescaleDB**에 저장하고,  
**Flask + Dash**를 통해 시각화하는 웹 대시보드 프로젝트입니다.

---

## 🔧 주요 기능

- 📡 **실시간 데이터 수집**  
  센서로부터 주기적으로 토양 수분 데이터를 수집 및 저장

- 🧠 **TimescaleDB 기반 시계열 저장**  
  고성능 시계열 DB로 대량 데이터도 안정적 관리

- 📊 **Dash를 통한 시각화**  
  라인 차트, 게이지, 시간 범위 필터 등 직관적인 시각화 제공

- 🌐 **Flask 통합**  
  Dash 앱을 Flask에 통합해 유연한 라우팅 및 확장성 확보

---

## 🛠 기술 스택

- Python
- Flask
- Dash (Plotly)
- TimescaleDB (PostgreSQL 기반)
- Pandas
