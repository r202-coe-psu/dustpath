from importlib.metadata import requires
import mongoengine as me
import datetime

class Domain(me.Document):
    meta = {'collection': 'domains'}

    name = me.StringField(requires=True)
    center = me.GeoPointField(required=True)
    width = me.FloatField(required=True)
    hight = me.FloatField(required=True)
    dx = me.FloatField(requires=True)
    dy = me.FloatField(requires=True)
    e_we = me.IntField(requires=True)
    e_sn = me.IntField(requires=True)

    created_date = me.DateTimeField(
        required=True, 
        default=datetime.datetime.now(),)