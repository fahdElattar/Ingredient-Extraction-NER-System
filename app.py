from flask import Flask, request, render_template
import requests

app = Flask(__name__)

NER_ENDPOINT = 'https://flurried-wilfredo-unfleeing.ngrok-free.dev/predict'

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    recipe_text = request.form.get('recipe', '').strip()

    if not recipe_text:
        return render_template('index.html', error="Please enter a recipe.")

    sentences = [line.strip() for line in recipe_text.split('\n') if line.strip()]

    try:
        response = requests.post(NER_ENDPOINT, json={'sentences': sentences})
    except Exception:
        return render_template('index.html', error="Failed to contact NER server.")

    if response.status_code != 200:
        return render_template('index.html', error="NER model returned an error.")

    extracted = response.json()

    return render_template(
        'index.html',
        recipe=recipe_text,
        ingredients=extracted
    )

if __name__ == '__main__':
    app.run(debug=True)
