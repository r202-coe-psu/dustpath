import mongoengine as me
import datetime

class NameListQuilt(me.Document):
    meta = {"collection": "namelist_quilt"}
    
    nio_tasks_per_group = me.ListField(me.IntField(default=0), default=[])
    nio_groups = me.ListField(me.IntField(default=0), default=[])