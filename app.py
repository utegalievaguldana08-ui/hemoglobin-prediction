import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Оқытылған модельді жүктеу
# Файл аты GitHub-тағымен бірдей болуы керек
try:
    model = joblib.load('hb_model.pkl')
except:
    st.error("Модель файлы (hb_model.pkl) табылмады. GitHub-қа жүктегеніңізді тексеріңіз.")

st.set_page_config(page_title="Hemoglobin Predictor", page_icon="🩸")

st.title("🩸 Гемоглобин деңгейін болжаудың виртуалды моделі")
st.write("Бұл модель жиналған деректер негізінде гемоглобин деңгейін болжайды.")

# 2. Пайдаланушы енгізетін деректер (Sidebar)
st.sidebar.header("Деректеріңізді енгізіңіз:")

age = st.sidebar.slider("Жасыңыз", 15, 80, 25)
gender = st.sidebar.selectbox("Жынысыңыз", options=[1, 2], format_func=lambda x: "Әйел" if x==1 else "Ер")
meat = st.sidebar.selectbox("Ет тұтыну жиілігі (аптасына)", options=[1, 2, 3, 4], 
                            format_func=lambda x: ["3-4 рет", "Күн сайын", "1-2 рет", "Тұтынбаймын"][x-1])
veg = st.sidebar.radio("Вегетариансыз ба?", options=[1, 2], format_func=lambda x: "Жоқ" if x==1 else "Иә")
iron_food = st.sidebar.selectbox("Темірге бай тағамдарды тұтыну", options=[1, 2, 3], 
                                 format_func=lambda x: ["Сирек", "Жиі", "Кейде"][x-1])

# 3. Болжам жасау логикасы
if st.button("Болжамды есептеу"):
    # Бұл бөлікті дәл осылай өзгертіңіз:
    features = pd.DataFrame([[age, gender, meat, veg, iron_food]], 
                            columns=['Age', 'Gender', 'Meat_Freq', 'Veg_Diet', 'Iron_Food'])
    
    # Модель арқылы болжам жасау
    prediction = model.predict(features)[0]
    
    # Нәтижені шығару
    st.subheader(f"Болжамды гемоглобин деңгейі: {prediction:.1f} г/л")
    
    # ДДСҰ стандарты бойынша статус анықтау
    if (gender == 1 and prediction < 120) or (gender == 2 and prediction < 130):
        st.error("Статус: Анемия қаупі жоғары. Дәрігермен кеңесу ұсынылады.")
    else:
        st.success("Статус: Гемоглобин деңгейі қалыпты.")

    # Визуалды салыстыру (Optional)

    st.info("Бұл болжам сіз енгізген 5 факторға негізделген машиналық оқыту нәтижесі.")
