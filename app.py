import streamlit as st
import pandas as pd
import joblib

# 1. Беттің баптаулары
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
    st.error(f"Модель жүктелмеді: {e}")
    st.stop()

# 3. Енгізу өрістері
st.sidebar.header("Деректеріңізді енгізіңіз:")
age = st.sidebar.slider("Жасыңыз", 15, 80, 25)
gender = st.sidebar.selectbox("Жынысыңыз", options=[1, 2], format_func=lambda x: "Әйел" if x==1 else "Ер")
meat = st.sidebar.selectbox("Ет тұтыну жиілігі", options=[1, 2, 3, 4], 
                            format_func=lambda x: ["3-4 рет", "Күн сайын", "1-2 рет", "Тұтынбаймын"][x-1])
veg = st.sidebar.radio("Вегетариансыз ба?", options=[1, 2], format_func=lambda x: "Жоқ" if x==1 else "Иә")
iron_food = st.sidebar.selectbox("Темірге бай тағамдар", options=[1, 2, 3], 
                                 format_func=lambda x: ["Сирек", "Жиі", "Кейде"][x-1])

# 4. Болжам жасау (Шегіністерге мұқият болыңыз!)
if st.button("Болжамды есептеу"):
    # Баған аттарынсыз, тікелей сандарды массив ретінде береміз (қате болмауы үшін)
    data = [[age, gender, meat, veg, iron_food]]
    
    try:
        prediction = model.predict(data)[0]
        
        # Нәтижені шығару
        st.success(f"Болжамды гемоглобин деңгейі: {prediction:.1f} г/л")
        
        # Анемия статусын тексеру
        if (gender == 1 and prediction < 120) or (gender == 2 and prediction < 130):
            st.warning("⚠️ Статус: Анемия қаупі бар.")
        else:
            st.balloons()
            st.info("✅ Статус: Гемоглобин деңгейі қалыпты.")
            
    except Exception as e:
        st.error(f"Болжам кезінде қате шықты: {e}")


