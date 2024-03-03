from flask import Flask, jsonify

app = Flask(__name__)

# Basic configuration
app.config['DEBUG'] = True  # Enable debug mode for development purposes

# Define a route for the root URL ("/")
@app.route('/')
def home():
    return "Hello, World!"

# Define a configurable route
@app.route('/<name>')
def hello_name(name):
    return jsonify(message=f"Hello, {name}!")

if __name__ == '__main__':
    # Run the server on all available interfaces, port can be configured
    app.run(host='0.0.0.0', port=80)