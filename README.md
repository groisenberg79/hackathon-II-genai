# Social Sentiment Analysis

Hackathon project analyzing sentiment trends in online discussions using Reddit data.

## Tools
- Python
- Pandas
- Sentiment Analysis (VADER)
- Matplotlib / Seaborn
- Streamlit

## Data Pipeline

1. Raw Reddit comments are stored in `data/raw/`.
2. The notebook `01_eda_sentiment.ipynb` performs:
   - text cleaning
   - stopword removal
   - keyword extraction
   - sentiment analysis using VADER.
3. The final dataset is exported to:

data/processed/chatgpt_final_dataset.csv

4. The Streamlit app loads this dataset to generate the dashboard.
