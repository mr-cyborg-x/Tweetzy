import tweepy
import os

def get_tweets(keyword, count=10):
    api_key = os.getenv("TWITTER_API_KEY")
    api_secret = os.getenv("TWITTER_API_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    if not all([api_key, api_secret, access_token, access_token_secret]):
        # Fallback for demo purposes if credentials are missing
        # In a real app, this should raise an error
        print("Twitter credentials missing. Returning mock data.")
        return _get_mock_tweets(keyword, count)

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    try:
        tweets = api.search_tweets(q=keyword, count=count, lang="en", tweet_mode="extended")
        return [{
            "text": tweet.full_text,
            "username": tweet.user.name,
            "handle": f"@{tweet.user.screen_name}",
            "timestamp": tweet.created_at.strftime("%Y-%m-%d %H:%M:%S")
        } for tweet in tweets]
    except Exception as e:
        print(f"Error fetching tweets: {e}")
        return _get_mock_tweets(keyword, count)

import random

def _get_mock_tweets(keyword, count):
    # Mock data for testing/demo when API is unavailable
    templates = [
        # Positive
        f"I absolutely love {{keyword}}! It's been a game changer for me. #{{keyword}} #LoveIt",
        f"Just tried {{keyword}} and I'm blown away. Highly recommend! 🚀",
        f"The new updates to {{keyword}} are fantastic. Great job team!",
        f"Can't imagine my life without {{keyword}} now. It's that good.",
        f"{{keyword}} is exactly what I needed today. So happy! 😊",
        
        # Negative
        f"Honestly, {{keyword}} is overhyped. I don't get the appeal.",
        f"Had a terrible experience with {{keyword}} today. Frustrating. 😡",
        f"Why is {{keyword}} so broken? Please fix this.",
        f"I'm done with {{keyword}}. Moving to the competitor.",
        f"Disappointed with the latest {{keyword}} release. Expected better.",
        
        # Neutral / News
        f"Just saw a news article about {{keyword}}. Interesting read.",
        f"Anyone else noticing the trend with {{keyword}} lately?",
        f"Thinking about trying {{keyword}}. Any tips for a beginner?",
        f"The impact of {{keyword}} on the industry is undeniable.",
        f"Here are 5 things you need to know about {{keyword}}.",
        
        # Questions
        f"Does anyone know how to fix this issue with {{keyword}}?",
        f"What's your favorite feature of {{keyword}}?",
        f"Is {{keyword}} worth the price? asking for a friend.",
        
        # Short/Random
        f"{{keyword}} ftw!",
        f"{{keyword}}... 🤔",
        f"Wait, what happened with {{keyword}}?",
        f"Current mood: {{keyword}}",
    ]
    
    # Mock users for realistic feel
    mock_users = [
        {"name": "Tech Insider", "handle": "@tech_insider"},
        {"name": "Sarah Jenkins", "handle": "@sarah_j_dev"},
        {"name": "Crypto King", "handle": "@cryptoking"},
        {"name": "Daily News", "handle": "@dailynews_us"},
        {"name": "Alex Chen", "handle": "@alexc_coding"},
        {"name": "Marketing Guru", "handle": "@marketing_pro"},
        {"name": "Jessica Smith", "handle": "@jsmith_design"},
        {"name": "Code Wizard", "handle": "@codewizard99"},
        {"name": "Startup Life", "handle": "@startuplife"},
        {"name": "AI Enthusiast", "handle": "@ai_future"}
    ]
    
    mock_tweets = []
    for _ in range(count):
        template = random.choice(templates)
        user = random.choice(mock_users)
        
        # Randomly capitalize keyword sometimes
        display_keyword = keyword if random.random() > 0.5 else keyword.title()
        tweet_text = template.format(keyword=display_keyword)
        
        # Random timestamp within last 24 hours
        hours_ago = random.randint(1, 24)
        timestamp = f"{hours_ago}h ago"
        
        mock_tweets.append({
            "text": tweet_text,
            "username": user["name"],
            "handle": user["handle"],
            "timestamp": timestamp
        })
        
    return mock_tweets
