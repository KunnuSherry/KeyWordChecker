import csv
import io
from flask import Flask, render_template, request, Response
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        links = request.form.getlist('links')
        tags = request.form.get('tags').split(',')
        results = []

        for link in links:
            try:
                response = requests.get(link)
                soup = BeautifulSoup(response.text, 'html.parser')
                contains_tags = any(soup.find_all(tag) for tag in tags)
                results.append((link, 'Yes' if contains_tags else 'No'))
            except Exception as e:
                results.append((link, f'Error: {e}'))

        return render_template('index.html', results=results)

    return render_template('index.html', results=None)

@app.route('/export_csv')
def export_csv():
    links = request.args.getlist('links')
    tags = request.args.get('tags').split(',')
    results = []

    for link in links:
        try:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')
            contains_tags = any(soup.find_all(tag) for tag in tags)
            results.append((link, 'Yes' if contains_tags else 'No'))
        except Exception as e:
            results.append((link, f'Error: {e}'))

    # Create a string buffer to hold CSV data
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Link', 'Contains Tags'])
    cw.writerows(results)
    csv_data = si.getvalue()

    # Create a response object with the CSV data
    response = Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=results.csv"}
    )
    return response

if __name__ == '__main__':
    app.run(debug=True)
