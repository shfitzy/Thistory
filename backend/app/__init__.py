from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restx import Api
from app.core.config import DevelopmentConfig
from app.database import db
from app.models.user import User
from app.api.v1.auth import api as auth_api
from app.api.v1.users import api as users_api

def create_app(config_class=DevelopmentConfig):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app, origins=config_class.CORS_ORIGINS, supports_credentials=True)
    
    # Register basic routes BEFORE API setup to ensure they take precedence
    @app.route("/", methods=["GET"], endpoint="home")
    def home():
        return {"message": "Thistory API"}
    
    @app.route("/health", methods=["GET"], endpoint="health")
    def health():
        return {"status": "healthy"}
        
    # Initialize API
    api = Api(
        app,
        version="1.0",
        title="Thistory API",
        description="RESTful API backend",
        doc="/docs/",
    )
    
    # Register namespaces
    api.add_namespace(auth_api, path="/api/v1/auth")
    api.add_namespace(users_api, path="/api/v1/users")
    
    # Debug: Print all registered routes
    if app.config.get("DEBUG"):
        print("\nRegistered routes:")
        for rule in app.url_map.iter_rules():
            print(f"  {rule.rule} -> {rule.endpoint} ({', '.join(rule.methods)})")
        print()
    
    return app

# Export the factory
__all__ = ["create_app"]