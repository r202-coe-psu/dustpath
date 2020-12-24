import mongoengine as me
import datetime

class Map(me.Document, UserMixin):
    meta = {'collection': 'maps'}

    firstname = me.StringField(required=True)
    lastname = me.StringField(required=True)
