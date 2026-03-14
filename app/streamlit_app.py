import pandas as pd
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Reddit AI Sentiment Analysis",
    layout="wide"
)

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("data/processed/chatgpt_final_dataset.csv")

df = load_data()

# Title and intro
st.title("Reddit AI Sentiment Analysis")
st.markdown("""
This dashboard explores Reddit discussions about AI tools such as ChatGPT.
It uses keyword analysis and sentiment analysis to compare discussions across subreddits.
""")

# -----------------------------
# Sidebar filter
# -----------------------------
st.sidebar.header("Filters")

subreddit_options = sorted(df["subreddit"].dropna().unique())

selected_subreddits = st.sidebar.multiselect(
    "Select subreddit(s)",
    options=subreddit_options,
    default=subreddit_options
)

# Apply filter
df_filtered = df[df["subreddit"].isin(selected_subreddits)].copy()

# Handle empty selection
if df_filtered.empty:
    st.warning("No data available for the selected subreddit(s).")
    st.stop()

# Basic dataset preview
st.subheader("Dataset Preview")
st.write("Shape of the filtered dataset:", df_filtered.shape)
st.dataframe(df_filtered.head())