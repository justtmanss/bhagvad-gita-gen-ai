from flask import Flask, jsonify
from database import init_db
from routes import api_bp

app = Flask(__name__)

# Initialize the database
init_db(app)

# Register API routes
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True)
