from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app.api.deps import get_current_user

api = Namespace("users", description="User operations")

user_model = api.model("User", {
    "id": fields.Integer(description="User ID"),
    "email": fields.String(required=True, description="User email"),
    "username": fields.String(required=True, description="Username"),
    "created_at": fields.DateTime(description="Creation timestamp"),
    "updated_at": fields.DateTime(description="Update timestamp"),
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
