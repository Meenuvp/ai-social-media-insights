import matplotlib.pyplot as plt
import streamlit as st

def plot_sentiment(ratio):
    plt.figure()
    ratio.plot(kind="pie", autopct="%1.1f%%")
    plt.ylabel("")
    st.pyplot(plt)

def plot_category(df):
    plt.figure()
    df["category"].value_counts().plot(kind="bar")
    plt.xlabel("Category")
    plt.ylabel("Posts Count")
    st.pyplot(plt)
