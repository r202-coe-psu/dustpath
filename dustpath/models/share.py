import mongoengine as me
import datetime

class Share(me.Document):
    meta = {"collection": "share"}
 
    wrf_core = me.ListField(me.StringField())
    max_dom = me.ListField(me.IntField(default=0), default=[])
    start_date = me.ListField(me.DateTimeField(), default=[])
    end_date = me.ListField(me.DateTimeField(), default=[])
    interval_seconds = me.ListField(me.IntField(default=0), default=[])
    io_form_geogrid = me.ListField(me.IntField(default=0), default=[])