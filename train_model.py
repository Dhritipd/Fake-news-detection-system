import os
import pandas as pd
import joblib
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# ✅ Ensure stopwords are downloaded
nltk.download('stopwords')
stop_words = stopwords.words('english')

# ✅ Load datasets
fake_path = "data/Fake.csv"
real_path = "data/True.csv"

if not (os.path.exists(fake_path) and os.path.exists(real_path)):
    raise FileNotFoundError("❌ Dataset files not found! Ensure 'Fake.csv' and 'True.csv' are in the 'data/' folder.")

df_fake = pd.read_csv(fake_path)
df_real = pd.read_csv(real_path)

# ✅ Add labels
df_fake["label"] = 0  # Fake news
df_real["label"] = 1  # Real news

# ✅ Combine datasets
df = pd.concat([df_fake, df_real]).reset_index(drop=True)

# ✅ Function to clean text
def clean_text(text):
    text = re.sub(r'[^\w\s.]', '', text)  # Keep words, spaces, and periods
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text.lower()

df["text"] = df["text"].apply(clean_text)

# ✅ Split dataset
X_train, X_test, y_train, y_test = train_test_split(df["text"], df["label"], test_size=0.2, random_state=42)

# ✅ Create a pipeline (TF-IDF + Naive Bayes)
pipeline = Pipeline([
    ('vectorizer', TfidfVectorizer(stop_words=stop_words)),
    ('classifier', MultinomialNB())
])

# ✅ Train the model
pipeline.fit(X_train, y_train)

# ✅ Ensure the model directory exists
model_dir = "fake-news-detection/model"
os.makedirs(model_dir, exist_ok=True)

# ✅ Save the trained model
joblib.dump(pipeline, os.path.join(model_dir, "fake_news_model.pkl"))

print("✅ Model training complete!")
