from flask import Flask, render_template, make_response

from src.crawler import CrawlingThread


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/background-crawling/', methods=['GET'])
def thread_crawling():
    t = CrawlingThread()
    t.start()
    return make_response(f"データ収集をします"), 202

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=8080)