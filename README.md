# Twitter Sentiment Analysis App

A clean, modern Twitter Sentiment Analysis application built with Flask and Vanilla JavaScript.

## 🚀 Features

- **Real-time Sentiment Analysis**: Analyze tweets for positive, negative, and neutral sentiment.
- **Dynamic Mock Data**: Generates realistic, context-aware mock tweets when API keys are missing.
- **Clean UI**: Modern blue/white design with card-based layout.
- **No Node.js Required**: Pure Python/Flask stack.

## 🛠️ Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🏃‍♂️ How to Run

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    python app.py
    ```

4.  **Open your browser:**
    - Local: [http://localhost:5000](http://localhost:5000)
    - Network: The terminal will show your network URL (e.g., `http://192.168.x.x:5000`)

## 📁 Project Structure

- `backend/app.py`: Main Flask application.
- `backend/templates/`: HTML templates (Jinja2).
- `backend/static/`: CSS and JavaScript files.
- `backend/services/`: Logic for Twitter API and sentiment analysis.
- `backend/database/`: MongoDB connection (optional).

## 🔑 Environment Variables

Create a `.env` file in the `backend` directory with your Twitter API credentials (optional):

```env
TWITTER_API_KEY=your_key
TWITTER_API_SECRET=your_secret
TWITTER_ACCESS_TOKEN=your_token
TWITTER_ACCESS_TOKEN_SECRET=your_token_secret
MONGO_URI=your_mongo_uri
```

If credentials are missing, the app automatically uses the **Mock Data Generator**.
