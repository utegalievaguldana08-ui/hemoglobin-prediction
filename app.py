import streamlit as st
import pandas as pd
import joblib

# 1. Беттің тақырыбы мен дизайны
st.set_page_config(page_title="Hemoglobin Predictor", page_icon="🩸")

st.title("🩸 Гемоглобин деңгейін болжаудың виртуалды моделі")
st.write("Бұл модель жиналған деректер негізінде гемоглобин деңгейін болжайды.")

# 2. Модельді жүктеу
@st.cache_resource
def load_model():
    return joblib.load('hb_model.pkl')

try:
    model = load_model()
except Exception as e:
    st.error(f"Модель файлын жүктеу мүмкін болмады: {e}")
    st.stop()

# 3. Пайдаланушы енгізетін деректер (Sidebar)
st.sidebar.header("Деректеріңізді енгізіңіз:")

age = st.sidebar.slider("Жасыңыз", 15, 80, 25)
gender = st.sidebar.selectbox("Жынысыңыз", options=[1, 2], format_func=lambda x: "Әйел" if x==1 else "Ер")
meat = st.sidebar.selectbox("Ет тұтыну жиілігі (аптасына)", options=[1, 2, 3, 4], 
                            format_func=lambda x: ["3-4 рет", "Күн сайын", "1-2 рет", "Тұтынбаймын"][x-1])
veg = st.sidebar.radio("Вегетариансыз ба?", options=[1, 2], format_func=lambda x: "Жоқ" if x==1 else "Иә")
iron_food = st.sidebar.selectbox("Темірге бай тағамдарды тұтыну", options=[1, 2, 3], 
                                 format_func=lambda x: ["Сирек", "Жиі", "Кейде"][x-1])

# 4. Болжам жасау бөлімі
if st.button("Болжамды есептеу"):
    # Деректерді модель күткендей баған аттарымен дайындау
    # Егер модель 'ValueError' берсе, төмендегі баған аттарын Colab-тағымен салыстыру керек
    input_data = pd.DataFrame([[age, gender, meat, veg, iron_food]], 
                            columns=['Age', 'Gender', 'Meat_Freq', 'Veg_Diet', 'Iron_Food'])
    
    try:
        prediction = model.predict(input_data)[0]
        
        # Нәтижені шығару
        st.success(f"### Болжамды гемоглобин деңгейі: {


