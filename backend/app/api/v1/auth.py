from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.database import db
from app.models.user import User
from app.crud import user as crud_user
from app.core.security import verify_password

api = Namespace("auth", description="Authentication operations")

# Models for request/response documentation
user_model = api.model("User", {
    "id": fields.Integer(description="User ID"),
    "email": fields.String(required=True, description="User email"),
    "username": fields.String(required=True, description="Username"),
    "is_active": fields.Boolean(description="Active status"),
    "is_superuser": fields.Boolean(description="Superuser status"),
    "created_at": fields.DateTime(description="Creation timestamp"),
    "updated_at": fields.DateTime(description="Update timestamp"),
})

register_model = api.model("Register", {
    "email": fields.String(required=True, description="User email"),
    "username": fields.String(required=True, description="Username"),
    "password": fields.String(required=True, description="Password"),
    "is_active": fields.Boolean(description="Active status", default=True),
})

login_model = api.model("Login", {
    "username": fields.String(required=True, description="Username or email"),
    "password": fields.String(required=True, description="Password"),
})

token_model = api.model("Token", {
    "access_token": fields.String(description="JWT access token"),
    "token_type": fields.String(description="Token type", default="bearer"),
})


@api.route("/register")
class Register(Resource):
    @api.expect(register_model)
    @api.marshal_with(user_model, code=201)
    @api.doc(responses={201: "User created", 400: "Email or username already exists"})
    def post(self):
        """Register a new user"""
        data = request.get_json()
        
        # Check if user already exists
        db_user = User.query.filter_by(email=data.get("email")).first()
        if db_user:
            api.abort(400, "Email already registered")
        
        db_user = User.query.filter_by(username=data.get("username")).first()
        if db_user:
            api.abort(400, "Username already taken")
        
        # Create new user
        user = crud_user.create_user(data)
        return user, 201


@api.route("/login")
class Login(Resource):
    @api.expect(login_model)
    @api.marshal_with(token_model)
    @api.doc(responses={200: "Login successful", 401: "Invalid credentials"})
    def post(self):
        """Login and get access token"""
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        
        if not username or not password:
            api.abort(400, "Username and password are required")
        
        # Try to find user by username or email
        db_user = User.query.filter_by(username=username).first()
        if not db_user:
            db_user = User.query.filter_by(email=username).first()
        
        if not db_user or not verify_password(password, db_user.hashed_password):
            api.abort(401, "Incorrect username/email or password")
        
        if not db_user.is_active:
            api.abort(400, "Inactive user")
        
        # Create access token
        access_token = create_access_token(identity=db_user.id)
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }, 200
