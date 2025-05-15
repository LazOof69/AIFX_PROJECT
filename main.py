from fetch_price import fetch_usdjpy
from fetch_news import fetch_news
from analyze import analyze_technical_indicators
from sentiment import analyze_news_sentiment
from decision import make_final_decision

def main():
    fetch_usdjpy()
    fetch_news()
    analyze_technical_indicators()
    analyze_news_sentiment()
    make_final_decision()

if __name__ == "__main__":
    main()
