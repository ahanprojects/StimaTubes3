from flask import Flask, render_template, request
from main import main

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    query = request.args.get('msg')
    return str(main(query))

if __name__ == "__main__":
    app.run() 