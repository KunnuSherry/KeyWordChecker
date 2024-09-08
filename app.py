from flask import Flask, render_template, request, send_file
import requests
from bs4 import BeautifulSoup
import csv
from io import StringIO

app = Flask(__name__)

def check_keyword_in_url(url, keyword):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return keyword.lower() in soup.text.lower()
        else:
            return False
    except Exception as e:
        print(f"Error checking {url}: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        urls = request.form.get('urls').splitlines()
        keyword = request.form.get('keyword')
        for url in urls:
            contains_keyword = check_keyword_in_url(url, keyword)
            results.append({
                'url': url,
                'contains_keyword': 'Yes' if contains_keyword else 'No'
            })
        return render_template('index.html', results=results, keyword=keyword)
    return render_template('index.html', results=None)

@app.route('/export_csv', methods=['POST'])
def export_csv():
    urls = request.form.get('urls').splitlines()
    keyword = request.form.get('keyword')
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['URL', 'Contains Keyword'])

    for url in urls:
        contains_keyword = check_keyword_in_url(url, keyword)
        writer.writerow([url, 'Yes' if contains_keyword else 'No'])

    output.seek(0)
    return send_file(output, mimetype='text/csv', attachment_filename='results.csv', as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
