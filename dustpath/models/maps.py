import mongoengine as me
import datetime

class Map(me.Document, UserMixin):
    meta = {'collection': 'maps'}

    center = me.GeoPointField(required=True)
    radius = me.IntField(required=True)
