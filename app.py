from flask import Flask, render_template, request, send_file
import csv
from io import StringIO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

def check_tag(link, tags):
    # Set up Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get(link)
        content = driver.page_source
    except Exception as e:
        driver.quit()
        return str(e)

    driver.quit()
    return all(tag.lower() in content.lower() for tag in tags)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    if request.method == 'POST':
        links = request.form['links'].splitlines()
        tags = [tag.strip() for tag in request.form['tags'].split(',')]
        results = [(link, check_tag(link, tags)) for link in links]
    return render_template('index.html', results=results)

@app.route('/export_csv')
def export_csv():
    links = request.args.getlist('links')
    tags = request.args.get('tags').split(',')
    tags = [tag.strip() for tag in tags]
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Link', 'Contains Tags'])
    for link in links:
        contains = check_tag(link, tags)
        cw.writerow([link, contains])
    output = si.getvalue().encode('utf-8')
    return send_file(StringIO(output), mimetype='text/csv', as_attachment=True, download_name='results.csv')

if __name__ == '__main__':
    app.run(debug=True)
