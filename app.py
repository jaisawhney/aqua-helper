from flask import Flask
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(6))


@app.route("/")
def index():
    return "Hello World!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 3000))
