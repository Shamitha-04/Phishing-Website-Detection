from flask import Flask, render_template, request
import joblib
import re
from sklearn.feature_extraction.text import CountVectorizer

app = Flask(__name__)

model = joblib.load('model.pkl')

vectorizer = joblib.load('vector.pkl')


def preprocess_url(url):
    # Convert to lowercase
    url = url.lower()
    
    # Remove 'http://', 'https://', 'www.', '.com', '.edu', and '.org'
    url = re.sub(r'https?://|www\.|\.com|\.edu|\.org', '', url)
    
    return url

def preprocess_and_predict(url):
    try:
        preprocessed_url = preprocess_url(url)
        url_vector = vectorizer.transform([preprocessed_url])
        prediction = model.predict(url_vector)[0]
        result = "phishing" if prediction == -1 else "legitimate"

        return result

    except Exception as e:
        return f"Error occurred during prediction: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_url():
    url = request.form.get('url')
    prediction_result = preprocess_and_predict(url)
    return render_template('result.html', url=url, prediction=prediction_result)

if __name__ == '__main__':
    app.run(debug=True)