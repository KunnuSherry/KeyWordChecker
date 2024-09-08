from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def check_keyword_in_website(url, keyword):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        if keyword in soup.get_text():
            return f"Keyword '{keyword}' found in {url}"
        else:
            return f"Keyword '{keyword}' not found in {url}"
    except requests.exceptions.RequestException as e:
        return f"Error accessing {url}: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        urls = request.form['urls'].splitlines()
        keyword = request.form['keyword']
        for url in urls:
            result = check_keyword_in_website(url.strip(), keyword)
            results.append(result)
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
