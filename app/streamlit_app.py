import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Reddit AI Sentiment Analysis",
    page_icon="🤖",
    layout="wide"
)

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("data/processed/chatgpt_final_dataset.csv")

df = load_data()

# Title and intro
st.title("🤖 Reddit AI Sentiment Analysis")
st.markdown(
    """
    This interactive dashboard explores Reddit discussions about AI tools such as ChatGPT.
    It compares sentiment and keyword patterns across multiple subreddits and highlights
    how different online communities talk about artificial intelligence.
    """
)

# -----------------------------
# Sidebar filter
# -----------------------------
st.sidebar.header("Filters")
st.sidebar.markdown("Use the filters below to focus the analysis on one or more Reddit communities.")

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

# -----------------------------
# Overview metrics
# -----------------------------
st.subheader("Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Comments", f"{len(df_filtered):,}")
col2.metric("Average Sentiment", f"{df_filtered['sentiment_score'].mean():.3f}")
col3.metric("Selected Subreddits", len(selected_subreddits))

st.markdown(
    """
    The charts below summarize the emotional tone of Reddit discussions and the most frequent
    themes that appear in comments about AI.
    """
)

# -----------------------------
# Sentiment distribution
# -----------------------------
st.subheader("Sentiment Distribution")
st.caption("This chart shows how many comments are classified as negative, neutral, or positive in the selected subreddits.")

sentiment_order = ["negative", "neutral", "positive"]

fig1, ax1 = plt.subplots(figsize=(6, 4))
sns.countplot(data=df_filtered, x="sentiment", order=sentiment_order, ax=ax1)
ax1.set_title("Sentiment Distribution")
ax1.set_xlabel("Sentiment")
ax1.set_ylabel("Count")
plt.tight_layout()
st.pyplot(fig1)

st.markdown(
    """
    **Interpretation:** This distribution provides a quick overview of the overall tone of the discussion.
    In this project, Reddit conversations about AI tend to be more positive or neutral than strongly negative.
    """
)

# -----------------------------
# Average sentiment by subreddit
# -----------------------------
st.subheader("Average Sentiment by Subreddit")
st.caption("Average sentiment scores help compare how optimistic or neutral each subreddit is on average.")

avg_sentiment = (
    df_filtered.groupby("subreddit")["sentiment_score"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.barplot(
    data=avg_sentiment,
    x="subreddit",
    y="sentiment_score",
    hue="subreddit",
    palette="viridis",
    legend=False,
    ax=ax2
)
ax2.set_title("Average Sentiment Score by Subreddit")
ax2.set_xlabel("Subreddit")
ax2.set_ylabel("Average Sentiment")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig2)

st.markdown(
    """
    **Interpretation:** Higher average sentiment scores suggest a more optimistic tone.
    This comparison helps identify which Reddit communities are most enthusiastic about AI tools.
    """
)

# -----------------------------
# Top keywords
# -----------------------------
st.subheader("Top Keywords")
st.caption("These are the most frequent keywords found in the filtered comments after stopword removal and text cleaning.")

keyword_text = " ".join(df_filtered["text_keywords"].dropna().astype(str))
keyword_counts = Counter(keyword_text.split())
top_keywords = pd.DataFrame(
    keyword_counts.most_common(15),
    columns=["word", "count"]
)

if not top_keywords.empty:
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    sns.barplot(
        data=top_keywords,
        x="count",
        y="word",
        hue="word",
        palette="viridis",
        legend=False,
        ax=ax3
    )
    ax3.set_title("Top Keywords")
    ax3.set_xlabel("Frequency")
    ax3.set_ylabel("Keyword")
    plt.tight_layout()
    st.pyplot(fig3)
    st.markdown(
        """
        **Interpretation:** The most common keywords highlight the main themes of the discussion,
        such as productivity, writing, work, and comparisons with other AI tools.
        """
    )
else:
    st.info("No keyword data available for the selected subreddit(s).")

# -----------------------------
# Word cloud
# -----------------------------
st.subheader("Word Cloud")
st.caption("The word cloud provides a quick visual summary of the most prominent terms in the selected comments.")

if keyword_text.strip():
    wordcloud = WordCloud(
        width=1000,
        height=500,
        background_color="white",
        max_words=100
    ).generate(keyword_text)

    fig4, ax4 = plt.subplots(figsize=(12, 6))
    ax4.imshow(wordcloud, interpolation="bilinear")
    ax4.axis("off")
    st.pyplot(fig4)
else:
    st.info("Not enough keyword data to generate a word cloud.")

# -----------------------------
# Example highly positive comments
# -----------------------------
st.subheader("Example Highly Positive Comments")
st.caption("These examples illustrate how users express strong enthusiasm or appreciation when discussing AI tools.")

# Keep only shorter comments so the examples are easier to read in the app
positive_examples = (
    df_filtered[df_filtered["comment_body"].astype(str).str.len() < 500]
    .sort_values("sentiment_score", ascending=False)
    [["subreddit", "sentiment_score", "comment_body"]]
    .head(5)
)

if not positive_examples.empty:
    for _, row in positive_examples.iterrows():
        with st.expander(
            f"{row['subreddit']} | sentiment score = {row['sentiment_score']:.4f}"
        ):
            st.write(row["comment_body"])
else:
    st.info("No short positive comment examples are available for the selected subreddit(s).")

st.markdown("---")
st.subheader("Key Takeaways")
st.markdown(
    """
    - Reddit discussions about AI are generally more positive or neutral than negative.
    - Different subreddits show different discussion patterns and levels of optimism.
    - Keyword analysis reveals strong interest in practical AI applications such as writing, work, and search.
    - Community-specific examples help illustrate how sentiment is expressed in real user comments.
    """
)