import mongoengine as me
import datetime

class BodyControl(me.Document):
    meta = {"collection": "bdy_control"}
    
    spec_bdy_width = me.ListField(me.IntField(default=0), default=[])
    spec_zone = me.ListField(me.IntField(default=0), default=[])
    relax_zone = me.ListField(me.IntField(default=0), default=[])
    specified = me.ListField(me.BooleanField(), default=[])
    nested = me.ListField(me.BooleanField(), default=[])