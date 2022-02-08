import mongoengine as me
import datetime

class Domain(me.Document):
    meta = {'collection': 'domains'}

    center = me.GeoPointField(required=True)
    width = me.FloatField(required=True)
    hight = me.FloatField(required=True)

    created_date = me.DateTimeField(
        required=True, 
        default=datetime.datetime.now(),)