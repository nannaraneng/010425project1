
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 데이터 로드
@st.cache_data
def load_data():
    file_path = 'Environment_Temperature_change_E_All_Data_NOFLAG.csv'  # 파일 경로
    data = pd.read_csv(file_path, encoding='latin1')
    return data

data = load_data()

# 제목 표시
st.title("전 세계 국가/지역별 기온 변화 (1960~2020)")

# 지역 및 기간 선택
areas = data['Area'].unique()
selected_area = st.selectbox("국가 또는 지역을 선택하세요:", areas)

time_columns = [col for col in data.columns if col.startswith('Y')]
selected_years = st.slider("기간을 설정하세요:", 1961, 2019, (1961, 2019))

# 데이터 필터링
filtered_data = data[(data['Area'] == selected_area) & (data['Element'] == 'Temperature change')]
time_data = filtered_data[time_columns]
time_data = time_data.loc[:, f'Y{selected_years[0]}':f'Y{selected_years[1]}']

# 시각화
if not time_data.empty:
    mean_temp = time_data.mean()
    years = [int(col[1:]) for col in mean_temp.index]

    plt.figure(figsize=(10, 6))
    plt.plot(years, mean_temp, marker='o', label='Temperature Change (°C)')
    plt.title(f'Temperature Change in {selected_area} ({selected_years[0]}-{selected_years[1]})')
    plt.xlabel('Year')
    plt.ylabel('Temperature Change (°C)')
    plt.grid(True)
    plt.legend()
    st.pyplot(plt)
else:
    st.warning("No data available for the selected region and years.")

