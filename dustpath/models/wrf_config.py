import mongoengine as me
import datetime

class WrfConfig(me.Document):
    meta = {'collection': 'wrf_config'}

    max_domain = me.IntField(required=True, default=1)
    start_date = me.DateTimeField(required=True, default=datetime.datetime.now)
    end_date = me.DateTimeField(required=True, default=datetime.datetime.now)

    created_date = me.DateTimeField(
        required=True, 
        default=datetime.datetime.now(),)