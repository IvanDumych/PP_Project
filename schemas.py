from pp_project.models import User, Audience, Reservation
from marshmallow import Schema, fields


class UserSchema(Schema):
    class Meta:
        model = User
        fields = ("id", "first_name", "second_name", "user_name")
        

class AudienceSchema(Schema):
    class Meta:
        model = Audience
        fields = ("id", "location", "size", "capacity")
