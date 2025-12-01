import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from services.twitter_service import get_tweets
from services.analysis_service import analyze_sentiment
from database.db import save_analysis, get_history
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    keyword = data.get('keyword')
    count = data.get('count', 10)

    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400

    try:
        tweets = get_tweets(keyword, count)
        print(f"Fetched {len(tweets)} tweets for keyword: {keyword}")
        results = analyze_sentiment(tweets)
        print(f"Analysis results keys: {results.keys()}")
        print(f"Number of analyzed tweets: {len(results.get('tweets', []))}")
        
        analysis_data = {
            "keyword": keyword,
            "results": results,
            "timestamp": results['timestamp'] # Assuming timestamp is added in analyze_sentiment or here
        }
        
        save_analysis(analysis_data)
        
        return jsonify(results)
    except Exception as e:
        print(f"Error in analyze endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/history', methods=['GET'])
def history():
    try:
        history_data = get_history()
        return jsonify(history_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
