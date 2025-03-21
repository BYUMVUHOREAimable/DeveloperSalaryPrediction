import streamlit as st
import pickle
import numpy as np
import pandas as pd

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

def show_predict_page():
    st.title("Software Developer Salary Prediction")

    st.write("""### We need some information to predict the salary""")

    countries = (
        "United States",
        "India",
        "United Kingdom",
        "Germany",
        "Canada",
        "Brazil",
        "France",
        "Spain",
        "Australia",
        "Netherlands",
        "Poland",
        "Italy",
        "Russian Federation",
        "Sweden",
    )

    education = (
        "Less than a Bachelors",
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad",
    )

    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education)
    experience = st.slider("Years of Experience", 0, 50, 3)

    ok = st.button("Calculate Salary")
    if ok:
        # Convert input to DataFrame with feature names
        X = pd.DataFrame([[country, education, experience]], columns=["Country", "EdLevel", "YearsCodePro"])
        
        # Transform categorical values
        X["Country"] = le_country.transform(X["Country"])
        X["EdLevel"] = le_education.transform(X["EdLevel"])
        X = X.astype(float)

        # Predict salary
        salary = regressor.predict(X)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")
