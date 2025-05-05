from flask import Flask, send_from_directory
from core.api import api

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def serve_frontend():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)