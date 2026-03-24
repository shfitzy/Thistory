from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.crud import user as crud_user
from app.api.deps import get_current_user

api = Namespace("users", description="User operations")

# Models for request/response documentation
user_model = api.model("User", {
    "id": fields.Integer(description="User ID"),
    "email": fields.String(required=True, description="User email"),
    "username": fields.String(required=True, description="Username"),
    "created_at": fields.DateTime(description="Creation timestamp"),
    "updated_at": fields.DateTime(description="Update timestamp"),
})

user_create_model = api.model("UserCreate", {
    "email": fields.String(required=True, description="User email"),
    "username": fields.String(required=True, description="Username"),
    "password": fields.String(required=True, description="Password"),
})

user_update_model = api.model("UserUpdate", {
    "email": fields.String(description="User email"),
    "username": fields.String(description="Username"),
    "password": fields.String(description="Password"),
})


@api.route("/me")
class CurrentUser(Resource):
    @jwt_required()
    @api.marshal_with(user_model)
    @api.doc(security="Bearer")
    def get(self):
        """Get current user"""
        user = get_current_user()
        if not user:
            api.abort(401, "Invalid or missing token")
        return user


@api.route("")
class UserList(Resource):
    @jwt_required(optional=True)
    @api.marshal_list_with(user_model)
    @api.doc(security="Bearer", params={
        "skip": {"description": "Number of records to skip", "type": "integer", "default": 0},
        "limit": {"description": "Maximum number of records to return", "type": "integer", "default": 100}
    })
    def get(self):
        """Get list of users"""
        user = get_current_user()
        if not user:
            api.abort(401, "Invalid or missing token")
        
        skip = request.args.get("skip", 0, type=int)
        limit = request.args.get("limit", 100, type=int)
        
        users = crud_user.get_users(skip=skip, limit=limit)
        return users

    @jwt_required()
    @api.expect(user_create_model)
    @api.marshal_with(user_model, code=201)
    @api.doc(security="Bearer", responses={201: "User created", 400: "Email or username already exists"})
    def post(self):
        """Create a new user"""
        current_user = get_current_user()
        if not current_user:
            api.abort(401, "Invalid or missing token")
        
        data = request.get_json()
        
        db_user = User.query.filter_by(email=data.get("email")).first()
        if db_user:
            api.abort(400, "Email already registered")
        
        db_user = User.query.filter_by(username=data.get("username")).first()
        if db_user:
            api.abort(400, "Username already taken")
        
        user = crud_user.create_user(data)
        return user, 201


@api.route("/<int:user_id>")
class UserResource(Resource):
    @jwt_required()
    @api.marshal_with(user_model)
    @api.doc(security="Bearer", responses={404: "User not found"})
    def get(self, user_id):
        """Get a user by ID"""
        current_user = get_current_user()
        if not current_user:
            api.abort(401, "Invalid or missing token")
        
        db_user = crud_user.get_user(user_id)
        if db_user is None:
            api.abort(404, "User not found")
        return db_user

    @jwt_required()
    @api.expect(user_update_model)
    @api.marshal_with(user_model)
    @api.doc(security="Bearer", responses={403: "Not enough permissions", 404: "User not found"})
    def put(self, user_id):
        """Update a user"""
        current_user = get_current_user()
        if not current_user:
            api.abort(401, "Invalid or missing token")
        
        data = request.get_json()
        db_user = crud_user.update_user(user_id, data)
        if db_user is None:
            api.abort(404, "User not found")
        return db_user

    @jwt_required()
    @api.doc(security="Bearer", responses={204: "User deleted", 403: "Not enough permissions", 404: "User not found"})
    def delete(self, user_id):
        """Delete a user"""
        current_user = get_current_user()
        if not current_user:
            api.abort(401, "Invalid or missing token")
        
        success = crud_user.delete_user(user_id)
        if not success:
            api.abort(404, "User not found")
        return "", 204
