import mongoengine as me
import datetime

class Physics(me.Document):
    meta = {"collection": "physics"}

    num_land_cat = me.ListField(me.IntField(default=0), default=[])
    mp_physics = me.ListField(me.IntField(default=0), default=[])
    progn = me.ListField(me.IntField(default=0), default=[])
    ra_lw_physics = me.ListField(me.IntField(default=0), default=[])
    ra_sw_physics = me.ListField(me.IntField(default=0), default=[])
    radt = me.ListField(me.IntField(default=0), default=[])
    sf_sfclay_physics = me.ListField(me.IntField(default=0), default=[])
    sf_surface_physics = me.ListField(me.IntField(default=0), default=[])
    bl_pbl_physics = me.ListField(me.IntField(default=0), default=[])
    bldt = me.ListField(me.IntField(default=0), default=[])
    cu_physics = me.ListField(me.IntField(default=0), default=[])
    cu_diag = me.ListField(me.IntField(default=0), default=[])
    cudt = me.ListField(me.IntField(default=0), default=[])
    ishallow = me.ListField(me.IntField(default=0), default=[])
    isfflx = me.ListField(me.IntField(default=0), default=[])
    ifsnow = me.ListField(me.IntField(default=0), default=[])
    icloud = me.ListField(me.IntField(default=0), default=[])
    surface_input_source = me.ListField(me.IntField(default=0), default=[])
    num_soil_layers = me.ListField(me.IntField(default=0), default=[])
    sf_urban_physics = me.ListField(me.IntField(default=0), default=[])
    mp_zero_out = me.ListField(me.IntField(default=0), default=[])
    mp_zero_out_thresh = me.ListField(me.FloatField(), default=[])
    maxiens = me.ListField(me.IntField(default=0), default=[])
    maxens = me.ListField(me.IntField(default=0), default=[])
    maxens2 = me.ListField(me.IntField(default=0), default=[])
    maxens3 = me.ListField(me.IntField(default=0), default=[])
    ensdim = me.ListField(me.IntField(default=0), default=[])
    cu_rad_feedback = me.ListField(me.BooleanField(), default=[])