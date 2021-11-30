import mongoengine as me
import datetime

class Dynamics(me.Document):
    meta = {"collection": "dynamics"}

    rk_ord = me.ListField(me.IntField(default=0), default=[])
    w_damping = me.ListField(me.IntField(default=0), default=[])
    diff_opt = me.ListField(me.IntField(default=0), default=[])
    km_opt = me.ListField(me.IntField(default=0), default=[])
    diff_6th_opt = me.ListField(me.IntField(default=0), default=[])
    diff_6th_factor = me.ListField(me.FloatField(), default=[])
    base_temp = me.FloatField(required=True)
    damp_opt = me.ListField(me.IntField(default=0), default=[])
    zdamp = me.ListField(me.FloatField(), default=[])
    dampcoef = me.ListField(me.FloatField(), default=[])
    khdif = me.ListField(me.IntField(default=0), default=[])
    kvdif = me.ListField(me.IntField(default=0), default=[])
    non_hydrostatic = me.ListField(me.BooleanField(), default=[])
    moist_adv_opt = me.ListField(me.IntField(default=0), default=[])
    scalar_adv_opt = me.ListField(me.IntField(default=0), default=[])
    chem_adv_opt = me.ListField(me.IntField(default=0), default=[])
    tke_adv_opt = me.ListField(me.IntField(default=0), default=[])
    time_step_sound = me.ListField(me.IntField(default=0), default=[])
    h_mom_adv_order = me.ListField(me.IntField(default=0), default=[])
    v_mom_adv_order = me.ListField(me.IntField(default=0), default=[])
    h_sca_adv_order = me.ListField(me.IntField(default=0), default=[])
    v_sca_adv_order = me.ListField(me.IntField(default=0), default=[])