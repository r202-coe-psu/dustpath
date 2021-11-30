import mongoengine as me
import datetime

class Ungrib(me.Document):
    meta = {"collection": "ungrib"}
    
    out_format = me.ListField(me.StringField())
    prefix = me.ListField(me.StringField())