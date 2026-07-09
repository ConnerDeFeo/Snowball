# app.py
from flask import Flask
from routes.document_retrieval import document_retrieval_bp
from routes.health import health_bp
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(document_retrieval_bp)
    app.register_blueprint(health_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()


