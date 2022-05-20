import mongoengine as me
import datetime

from flask_login import UserMixin


class User(me.Document, UserMixin):
    username = me.StringField(min_length=5, max_length=64)
    email = me.StringField(required=True, unique=True)
    picture_url = me.StringField()

    first_name = me.StringField(required=True, max_length=128)
    last_name = me.StringField(required=True, max_length=128)

    status = me.StringField(required=True, default="disactive")
    created_date = me.DateTimeField(required=True, default=datetime.datetime.now)
    updated_date = me.DateTimeField(
        required=True, default=datetime.datetime.now, auto_now=True
    )
    meta = {"collection": "users"}

    def display_name(self):
        return "%s %s" % (self.first_name, self.last_name)
