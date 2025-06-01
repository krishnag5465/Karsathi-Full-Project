from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.auth import auth
from routes.convert import convert
from routes.predict import predict  # ✅ import added
import os

app = Flask(__name__, static_folder='frontend')
app.secret_key = 'supersecretkey'
CORS(app, supports_credentials=True)

# Register blueprints
app.register_blueprint(auth, url_prefix='/api/auth')
app.register_blueprint(convert, url_prefix='/api/convert')
app.register_blueprint(predict, url_prefix='/api/predict')  # ✅ route added

@app.route('/')
def serve_welcome():
    return send_from_directory(app.static_folder, 'welcome.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(debug=True)
