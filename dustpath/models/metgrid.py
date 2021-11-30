import mongoengine as me
import datetime

class Metgrid(me.Document):
    meta = {"collection": "metgrid"}
    
    fg_name = me.ListField(me.StringField())
    io_form_metgrid = me.ListField(me.IntField(default=0), default=[])