from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    gads = datetime.datetime.now().year
    return render_template("index.html", gads=gads)

@app.route('/klasiskas')
def klasiskas():
    return render_template('Enges/klasiskas.html')

if __name__ == '__main__':
    app.run(debug=True)