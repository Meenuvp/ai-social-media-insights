import streamlit as st
import pandas as pd

from data_loader import load_data, filter_data
from sentiment_analysis import clean_text, apply_sentiment, sentiment_ratio
from category_analysis import apply_category
from insights import generate_insights
from visualization import plot_sentiment, plot_category
from youtube_fetcher import fetch_youtube_comments

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Social Media Insights",
    page_icon="📊",
    layout="wide"
)

# ---------------- HEADER ----------------
st.title("📊 AI-Powered Social Media Insights Dashboard")
st.markdown("Analyze **Twitter, LinkedIn, and YouTube audience sentiment** using AI.")

# ---------------- LOAD DATA ----------------
df = load_data()

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Controls")

source = st.sidebar.radio(
    "Select Data Source",
    ["Twitter / LinkedIn Dataset", "YouTube (Live API)"]
)

# ---------------- DATASET ANALYSIS ----------------
if source == "Twitter / LinkedIn Dataset":

    st.sidebar.subheader("Dataset Settings")

    platform = st.sidebar.selectbox(
        "Select Platform",
        ["Twitter", "LinkedIn"]
    )

    selected_platform = platform.lower()

    platform_accounts = (
        df[df["platform"] == selected_platform]["account_id"].unique()
    )

    if len(platform_accounts) == 0:
        st.error("No accounts found for this platform.")

    else:
        account_id = st.sidebar.selectbox(
            "Select Account ID",
            platform_accounts
        )

        if st.sidebar.button("🚀 Run Analysis"):

            with st.spinner("Analyzing posts..."):

                filtered_df = filter_data(df, platform, account_id)

                if filtered_df.empty:
                    st.error("No data found for this account.")

                else:

                    filtered_df["post"] = filtered_df["post"].apply(clean_text)
                    filtered_df = apply_sentiment(filtered_df)
                    filtered_df = apply_category(filtered_df)

                    # -------- METRICS --------
                    positive = (filtered_df["sentiment"] == "Positive").sum()
                    negative = (filtered_df["sentiment"] == "Negative").sum()
                    neutral = (filtered_df["sentiment"] == "Neutral").sum()

                    col1, col2, col3 = st.columns(3)

                    col1.metric("😊 Positive", positive)
                    col2.metric("😐 Neutral", neutral)
                    col3.metric("😡 Negative", negative)

                    # -------- DATA --------
                    st.subheader("📄 Analyzed Posts")
                    st.dataframe(filtered_df, use_container_width=True)

                    # -------- VISUALIZATIONS --------
                    col4, col5 = st.columns(2)

                    with col4:
                        st.subheader("📊 Sentiment Ratio")
                        plot_sentiment(sentiment_ratio(filtered_df))

                    with col5:
                        st.subheader("📊 Category Distribution")
                        plot_category(filtered_df)

                    # -------- INSIGHTS --------
                    st.subheader("🧠 AI Insights")

                    insights = generate_insights(filtered_df, platform, account_id)

                    st.success(insights)

# ---------------- YOUTUBE ANALYSIS ----------------
else:

    st.subheader("📺 YouTube Comment Analyzer")

    channel_input = st.text_input(
        "Enter Channel ID / Handle",
        placeholder="example: jktamil"
    )

    if st.button("Fetch & Analyze Comments"):

        with st.spinner("Fetching comments from YouTube..."):

            comments = fetch_youtube_comments(channel_input)

            if not comments:
                st.error("No comments found.")

            else:

                yt_df = pd.DataFrame({
                    "platform": "YouTube",
                    "account_type": "Channel",
                    "account_id": channel_input,
                    "post": comments
                })

                yt_df["post"] = yt_df["post"].apply(clean_text)
                yt_df = apply_sentiment(yt_df)
                yt_df = apply_category(yt_df)

                # -------- METRICS --------
                positive = (yt_df["sentiment"] == "Positive").sum()
                negative = (yt_df["sentiment"] == "Negative").sum()
                neutral = (yt_df["sentiment"] == "Neutral").sum()

                col1, col2, col3 = st.columns(3)

                col1.metric("😊 Positive", positive)
                col2.metric("😐 Neutral", neutral)
                col3.metric("😡 Negative", negative)

                # -------- DATA --------
                st.subheader("📄 YouTube Comments")
                st.dataframe(yt_df, use_container_width=True)

                # -------- VISUALIZATION --------
                st.subheader("📊 Sentiment Ratio")
                plot_sentiment(sentiment_ratio(yt_df))

                # -------- INSIGHTS --------
                st.subheader("🧠 AI Insights")
                st.success(generate_insights(yt_df, "YouTube", channel_input))