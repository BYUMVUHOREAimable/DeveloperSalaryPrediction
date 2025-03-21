import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def shorten_categories(categories, cutoff):
    return {cat: (cat if count >= cutoff else "Other") for cat, count in categories.items()}


def clean_experience(x):
    if x == "More than 50 years":
        return 50
    if x == "Less than 1 year":
        return 0.5
    try:
        return float(x)
    except ValueError:
        return None


def clean_education(x):
    if "Bachelor's degree" in x:
        return "Bachelor's degree"
    if "Master's degree" in x:
        return "Master's degree"
    if "Professional degree" in x or "Other doctoral" in x:
        return "Post grad"
    return "Less than a Bachelor's"


@st.cache_data
def load_data():
    try:
        df = pd.read_csv("developer-survey/survey_results_public.csv")
        df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
        df = df.dropna()
        df = df[df["Employment"] == "Employed full-time"].drop("Employment", axis=1)

        country_map = shorten_categories(df["Country"].value_counts(), 400)
        df["Country"] = df["Country"].map(country_map)
        df = df[(df["ConvertedComp"] <= 250000) & (df["ConvertedComp"] >= 10000)]
        df = df[df["Country"] != "Other"]

        df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
        df["EdLevel"] = df["EdLevel"].apply(clean_education)
        df = df.rename(columns={"ConvertedComp": "Salary"})
        return df
    except FileNotFoundError:
        st.error("Dataset file not found. Please check the file path.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An error occurred while loading data: {e}")
        return pd.DataFrame()


df = load_data()


def show_explore_page():
    st.title("Explore Software Engineer Salaries")
    st.write("### Stack Overflow Developer Survey 2024")

    if df.empty:
        st.warning("No data available.")
        return

    st.write("#### Number of Data from Different Countries")
    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig1)

    st.write("#### Mean Salary Based on Country")
    st.bar_chart(df.groupby("Country")["Salary"].mean().sort_values())

    st.write("#### Mean Salary Based on Experience")
    st.line_chart(df.groupby("YearsCodePro")["Salary"].mean().sort_values())