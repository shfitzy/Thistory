import os
from typing import List


class Config:
    """Base configuration"""
    # Database
    # SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'app.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production"))
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)) * 60  # Convert to seconds
    
    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


# Default to development config
config = DevelopmentConfig()
