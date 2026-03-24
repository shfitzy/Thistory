import pytest
import os
from app import create_app
from app.database import db as _db
from app.core.config import TestingConfig
from flask_jwt_extended import create_access_token


@pytest.fixture(scope='session')
def app():
    """Create application for testing"""
    # Set testing environment
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    os.environ['JWT_SECRET_KEY'] = 'test-secret-key'
    
    app = create_app(TestingConfig)
    
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture(scope='function', autouse=True)
def db(app):
    """Create clean database for each test"""
    with app.app_context():
        # Clear all tables
        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()
        yield _db
