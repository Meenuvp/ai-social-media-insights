import streamlit as st
import pandas as pd
import plotly.express as px

from data_loader import load_data, filter_data
from sentiment_analysis import clean_text, apply_sentiment
from category_analysis import apply_category
from insights import generate_insights
from youtube_fetcher import fetch_youtube_comments


# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI Social Media Insights",
    page_icon="🚀",
    layout="wide"
)

# ---------- LOAD DATA ----------
df = load_data()


# ---------- COLORFUL CSS ----------
st.markdown("""
<style>

body {
background: linear-gradient(120deg,#f6f9fc,#e3f2fd);
}

/* BUTTON STYLE */
.stButton > button {
    width:100%;
    height:3.2rem;
    font-size:1.1rem;
    font-weight:600;
    background: linear-gradient(90deg,#4f8bf9,#6a11cb);
    color:white;
    border-radius:10px;
    border:none;
}

.stButton > button:hover {
    background: linear-gradient(90deg,#6a11cb,#4f8bf9);
    color:white;
}

/* TITLE */
.dashboard-title{
font-size:42px;
font-weight:800;
text-align:center;
background: linear-gradient(90deg,#ff4b2b,#ff416c,#6a11cb,#2575fc);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
margin-bottom:30px;
}

/* METRIC CARDS */
.metric-card{
padding:25px;
border-radius:20px;
color:white;
font-size:22px;
font-weight:700;
text-align:center;
box-shadow:0px 10px 20px rgba(0,0,0,0.15);
}

.m1{background:linear-gradient(135deg,#ff7e5f,#feb47b);}
.m2{background:linear-gradient(135deg,#43cea2,#185a9d);}
.m3{background:linear-gradient(135deg,#ff512f,#dd2476);}
.m4{background:linear-gradient(135deg,#6a11cb,#2575fc);}

</style>
""", unsafe_allow_html=True)


# ---------- TITLE ----------
st.markdown(
"<div class='dashboard-title'>🚀 AI Powered Social Media Insights</div>",
unsafe_allow_html=True
)


# ---------- SIDEBAR ----------
with st.sidebar:

    st.title("🎛 Dashboard Controls")

    st.markdown("---")

    source = st.radio(
        "Choose Data Source",
        ["Dataset Analysis", "YouTube Analysis"]
    )

    st.markdown("---")

    # ABOUT SECTION
    st.subheader("📊 About Dashboard")

    st.info("""
This dashboard analyzes social media data using AI.

Features included:
• Sentiment Analysis 😊😡😐  
• Content Category Detection 📂  
• Interactive Visualizations 📊  
• AI Generated Insights 🧠  
• YouTube Comment Analysis 📺
""")

    st.markdown("---")

    # QUICK STATS
    st.subheader("⚡ Quick Stats")

    st.metric("Platforms Supported", "3")
    st.metric("AI Models Used", "2")
    st.metric("Charts Available", "4")

    st.markdown("---")

    # INSTRUCTIONS
    st.subheader("📝 How to Use")

    st.write("""
1️⃣ Select Data Source  
2️⃣ Choose Platform  
3️⃣ Select Account  
4️⃣ Click Analyze  
5️⃣ Explore Insights
""")

    st.markdown("---")

    st.caption("🚀 Built with Streamlit")
    st.caption("AI Social Media Insights Dashboard")


# ==========================================================
# DATASET ANALYSIS
# ==========================================================
if source == "Dataset Analysis":

    col1,col2 = st.columns(2)

    with col1:
        platform = st.selectbox(
            "📱 Select Platform",
            ["Twitter","LinkedIn"]
        )

    with col2:

        accounts = df[df["platform"].str.lower() == platform.lower()]["account_id"].unique()

        if len(accounts) == 0:
            st.error("No accounts available")
        else:
            account_id = st.selectbox("👤 Select Account",accounts)

    if len(accounts) != 0:

        analyze_btn = st.button(f"🚀 Analyze {platform} @{account_id}")

        if analyze_btn:

            filtered_df = filter_data(df,platform,account_id)

            filtered_df["post"] = filtered_df["post"].apply(clean_text)
            filtered_df = apply_sentiment(filtered_df)
            filtered_df = apply_category(filtered_df)

            total_posts = len(filtered_df)
            positive = (filtered_df["sentiment"]=="Positive").sum()
            negative = (filtered_df["sentiment"]=="Negative").sum()
            neutral = (filtered_df["sentiment"]=="Neutral").sum()

            # METRICS
            c1,c2,c3,c4 = st.columns(4)

            with c1:
                st.markdown(f"<div class='metric-card m1'>Total Posts<br>{total_posts}</div>",unsafe_allow_html=True)

            with c2:
                st.markdown(f"<div class='metric-card m2'>Positive 😊<br>{positive}</div>",unsafe_allow_html=True)

            with c3:
                st.markdown(f"<div class='metric-card m3'>Negative 😡<br>{negative}</div>",unsafe_allow_html=True)

            with c4:
                st.markdown(f"<div class='metric-card m4'>Neutral 😐<br>{neutral}</div>",unsafe_allow_html=True)

            tab1,tab2,tab3,tab4 = st.tabs(
                ["📊 Sentiment","📂 Categories","📄 Data","🧠 Insights"]
            )

            # SENTIMENT
            with tab1:

                sentiment_counts = filtered_df["sentiment"].value_counts()

                fig = px.pie(
                    values=sentiment_counts.values,
                    names=sentiment_counts.index,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )

                st.plotly_chart(fig,use_container_width=True)

            # CATEGORY
            with tab2:

                cat_counts = filtered_df["category"].value_counts()

                fig = px.bar(
                    x=cat_counts.index,
                    y=cat_counts.values,
                    color=cat_counts.index,
                    color_discrete_sequence=px.colors.qualitative.Bold
                )

                st.plotly_chart(fig,use_container_width=True)

            # DATA
            with tab3:

                st.dataframe(filtered_df,use_container_width=True)

            # INSIGHTS
            with tab4:

                insights = generate_insights(filtered_df,platform,account_id)
                st.success(insights)


# ==========================================================
# YOUTUBE ANALYSIS
# ==========================================================
else:

    channel = st.text_input("📺 Enter YouTube Channel")

    if channel:
        fetch_btn = st.button(f"📥 Fetch & Analyze {channel}")
    else:
        fetch_btn = st.button("📥 Fetch & Analyze Channel")

    if fetch_btn:

        comments = fetch_youtube_comments(channel)

        if not comments:
            st.error("No comments found")

        else:

            yt_df = pd.DataFrame({"post":comments})

            yt_df["post"] = yt_df["post"].apply(clean_text)
            yt_df = apply_sentiment(yt_df)

            total_comments = len(yt_df)
            positive = (yt_df["sentiment"]=="Positive").sum()
            negative = (yt_df["sentiment"]=="Negative").sum()
            neutral = (yt_df["sentiment"]=="Neutral").sum()

            c1,c2,c3,c4 = st.columns(4)

            with c1:
                st.markdown(f"<div class='metric-card m1'>Total Comments<br>{total_comments}</div>",unsafe_allow_html=True)

            with c2:
                st.markdown(f"<div class='metric-card m2'>Positive 😊<br>{positive}</div>",unsafe_allow_html=True)

            with c3:
                st.markdown(f"<div class='metric-card m3'>Negative 😡<br>{negative}</div>",unsafe_allow_html=True)

            with c4:
                st.markdown(f"<div class='metric-card m4'>Neutral 😐<br>{neutral}</div>",unsafe_allow_html=True)

            tab1,tab2,tab3 = st.tabs(["📊 Sentiment","📄 Comments","🧠 Insights"])

            with tab1:

                sentiment_counts = yt_df["sentiment"].value_counts()

                fig = px.pie(
                    values=sentiment_counts.values,
                    names=sentiment_counts.index,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )

                st.plotly_chart(fig,use_container_width=True)

            with tab2:

                st.dataframe(yt_df,use_container_width=True)

            with tab3:

                insights = generate_insights(yt_df,"YouTube",channel)
                st.success(insights)