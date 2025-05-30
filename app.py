from flask import Flask, render_template, request, jsonify
import joblib
import requests
from bs4 import BeautifulSoup
import random

app = Flask(__name__)

# Load trained model
model = joblib.load("fake-news-detection/model/fake_news_model.pkl")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    news_url = data.get("url")

    if not news_url:
        return jsonify({"error": "Please enter a news URL!"})

    try:
        # Fetch article text from URL
        response = requests.get(news_url)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        article_text = " ".join([p.get_text() for p in paragraphs])

        if not article_text:
            return jsonify({"error": "Could not extract text from this URL."})

        # Predict
        prediction = model.predict([article_text])[0]
        confidence = round(max(model.predict_proba([article_text])[0]) * 100, 2)

        result = "Fake News ❌" if prediction == 0 else "Real News ✅"

        return jsonify({"result": result, "confidence": confidence})

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/feature-analysis")
def feature_analysis():
    # Generate random feature values (you can replace with actual logic)
    features = {
        "sensationalism": random.randint(0, 100),
        "credible_sources": random.randint(0, 100),
        "emotional_language": random.randint(0, 100),
        "factual_content": random.randint(0, 100),
    }
    return render_template("feature_analysis.html", features=features)

if __name__ == "__main__":
    app.run(debug=True)
