import pandas as pd
from newsapi import NewsApiClient
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os

def analyze_indian_stock_sentiment(stock_name):
    """
    Fetches news from India for a specific stock using a robust search,
    performs sentiment analysis, and prints the results.
    """
    # 1. --- FETCH NEWS ARTICLES ---
    # PASTE your API key from the NewsAPI website here.
    api_key = 'API_KEY_HERE'  # Replace with your actual NewsAPI key

    # This check ensures you've replaced the placeholder.
    if api_key == 'API_KEY_HERE':
        print("Error: Please replace 'API_KEY_HERE' with your actual NewsAPI key.")
        return

    newsapi = NewsApiClient(api_key=api_key)

    print(f"\n📰 Searching all recent news in India about '{stock_name}'...")
    
    # --- THIS IS THE CORRECTED PART ---
    # We now use get_everything() which is more powerful and reliable for this task.
    try:
        all_articles = newsapi.get_everything(
            q=f'"{stock_name}"', # Search for the exact company name
            sources='the-times-of-india,the-hindu,business-today,livemint,the-economic-times', # Focus on major Indian sources
            language='en',
            sort_by='publishedAt', # Get the most recent articles first
            page_size=100
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    if not all_articles['articles']:
        print(f"No recent news found for '{stock_name}' from the specified sources.")
        return

    # 2. --- ANALYZE SENTIMENT (No changes here) ---
    analyzer = SentimentIntensityAnalyzer()
    analyzed_articles = []

    for article in all_articles['articles']:
        if not article['description']: # Skip articles with no description
            continue

        text_to_analyze = f"{article['title']}. {article['description']}"
        sentiment = analyzer.polarity_scores(text_to_analyze)
        compound_score = sentiment['compound']

        analyzed_articles.append({
            'Published At': article['publishedAt'].split("T")[0],
            'Source': article['source']['name'],
            'Title': article['title'],
            'Compound Score': compound_score
        })

    # 3. --- AGGREGATE AND DISPLAY RESULTS (No changes here) ---
    if not analyzed_articles:
        print("Could not analyze any articles (they may have been missing descriptions).")
        return
        
    df = pd.DataFrame(analyzed_articles)
    average_score = df['Compound Score'].mean()

    print(f"\n📊 Analysis Complete. Found and analyzed {len(df)} articles.")
    print(f"Average Sentiment Score: {average_score:.4f}")

    if average_score >= 0.05:
        final_sentiment = "Positive 📈"
    elif average_score <= -0.05:
        final_sentiment = "Negative 📉"
    else:
        final_sentiment = "Neutral 😐"
        
    print(f"Overall Sentiment: {final_sentiment}")
    
    print("\n--- Top 10 Recent Articles ---")
    pd.set_option('display.max_colwidth', 80)
    print(df.head(10).to_string(index=False, columns=['Published At', 'Source', 'Title', 'Compound Score']))


# --- RUN THE ANALYZER ---
if __name__ == "__main__":
    stock_to_analyze = "Infosys" 
    analyze_indian_stock_sentiment(stock_to_analyze)
    
    stock_to_analyze = "Tata Motors"
    analyze_indian_stock_sentiment(stock_to_analyze)