import mongoengine as me
import datetime

class Domain(me.Document):
    meta = {'collection': 'domains'}

    center = me.GeoPointField(required=True)
    radius = me.IntField(required=True)

    created_date = me.DateTimeField(
        required=True, 
        default=datetime.datetime.now(),)