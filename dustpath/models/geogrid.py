import mongoengine as me
import datetime

class GeoGrid(me.Document):
    meta = {"collection": "geogrid"}
    
    parent_id = me.ListField(me.IntField(default=0), default=[])
    parent_grid_ratio = me.ListField(me.IntField(default=0), default=[])
    i_parent_start = me.ListField(me.IntField(default=0), default=[])
    j_parent_start = me.ListField(me.IntField(default=0), default=[])
    e_we = me.ListField(me.IntField(default=0), default=[])
    e_sn = me.ListField(me.IntField(default=0), default=[])
    
    geog_data_res = me.ListField(me.StringField())
    dx = me.ListField(me.IntField(default=0), default=[])
    dy = me.ListField(me.IntField(default=0), default=[])
    map_proj = me.ListField(me.StringField())
    ref_lat = me.ListField(me.FloatField(), default=[])
    ref_lon = me.ListField(me.FloatField(), default=[])
    truelat1 = me.ListField(me.FloatField(), default=[])
    truelat2 = me.ListField(me.FloatField(), default=[])
    stand_lon = me.ListField(me.FloatField(), default=[])
    geog_data_path = me.StringField()