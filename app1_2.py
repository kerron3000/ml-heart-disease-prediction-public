import streamlit as st
import pandas as pd
import joblib
import os


# Loading the saved optimized Pipeline
@st.cache_resource  # Keeps the model in memory
def load_model():
    model_file = 'heart_disease_rf_optimized.pkl'
    if not os.path.exists(model_file):
        st.error(
            f"Model file '{model_file}' not found! Please run the training script first."
        )
        return None
    return joblib.load(model_file)


data_package = load_model()

if data_package:
    # Extract the pipeline instead of separate model/preprocessor
    pipeline = data_package['pipeline']
    target_mapping = data_package['target_mapping']

    st.set_page_config(page_title="Heart IQ", page_icon=":heart:")

    st.title("Heart Disease Prediction Tool")
    st.write(
        "Enter patient clinical data to predict the presence of heart disease."
    )

    st.header("Patient Data Input")

    # Create two columns for inputs
    col_num, col_cat = st.columns(2)

    # Column 1

    with col_num:
        st.subheader("Numerical Inputs")
        age = st.slider("Age of Patient", 1, 100, 50)
        bp = st.number_input("Resting Blood Pressure (BP)", 80, 200, 120)
        chol = st.number_input("Serum Cholesterol", 100, 600, 200)
        max_hr = st.slider("Max Heart Rate (Max HR)", 60, 220, 150)
        st_dep = st.number_input("Enter ST Depression value (mm)",
                                 0.0,
                                 6.2,
                                 1.0,
                                 step=0.1)

# Column 2

    with col_cat:
        st.subheader("Categorical Inputs")
        sex = st.selectbox("Sex (1 = Male, 0 = Female)", [1, 0])
        cp = st.selectbox("Chest Pain Type: (1; 2; 3; 4)", [1, 2, 3, 4])
        fbs = st.selectbox(
            "Fasting Blood Sugar > 120 mg/dl (1 = True, 0 = False)", [0, 1])
        ekg = st.selectbox("EKG Results (0; 1; 2)", [0, 1, 2])
        exang = st.selectbox("Exercise Induced Angina (1 = Yes, 0 = No)",
                             [0, 1])
        slope = st.selectbox("Slope of ST Segment value (mm)", [1, 2, 3])
        ca = st.selectbox("Number of Major Vessels (0–3)", [0, 1, 2, 3])
        thal = st.selectbox("Thallium (3 = Normal, 6 = Fixed, 7 = Reversible)",
                            [3, 6, 7])

    # Prediction Logic

    if st.button("Predict Diagnosis"):
        # Construct dataframe for the pipeline
        input_data = pd.DataFrame([{
            'Age': age,
            'Sex': sex,
            'Chest pain type': cp,
            'BP': bp,
            'Cholesterol': chol,
            'FBS over 120': fbs,
            'EKG results': ekg,
            'Max HR': max_hr,
            'Exercise angina': exang,
            'ST depression': st_dep,
            'Slope of ST': slope,
            'Number of vessels fluro': ca,
            'Thallium': thal
        }])

        # The pipeline automatically applies the StandardScaler and OneHotEncoder
        prediction = pipeline.predict(input_data)
        probability = pipeline.predict_proba(input_data)

        # Display Results
        result = target_mapping[prediction[0]]

        st.divider()
        if result == 'Presence':
            st.error(f"### Prediction: {result}")
        else:
            st.success(f"### Prediction: {result}")

        st.write(f"Confidence Level: **{max(probability[0])*100:.2f}%**")

    st.info(
        "Note: This tool is for demonstration purposes and not for medical diagnosis."
    )
