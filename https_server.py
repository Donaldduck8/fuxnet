from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, this is a secure Flask app!"


if __name__ == '__main__':
    print("ASDASD")
    app.run(host="0.0.0.0", ssl_context=(r'cert.pem', r'key.pem'), port=443)