import mongoengine as me
import datetime

class WrfConfig(me.Document):
    meta = {'collection': 'wrf_configs'}

    max_domain = me.IntField(required=True, default=1)
    start_date = me.DateField(required=True)
    end_date = me.DateField(required=True)

    created_date = me.DateTimeField(
        required=True, 
        default=datetime.datetime.now(),)