import mongoengine as me
import datetime

class Domains(me.Document):
    meta = {"collection": "domains"}

    time_step = me.ListField(me.IntField(default=0), default=[])
    time_step_fract_num = me.ListField(me.IntField(default=0), default=[])
    time_step_fract_den = me.ListField(me.IntField(default=0), default=[])
    max_dom = me.ListField(me.IntField(default=0), default=[])
    
    s_we = me.ListField(me.IntField(default=0), default=[])
    e_we = me.ListField(me.IntField(default=0), default=[])
    s_sn = me.ListField(me.IntField(default=0), default=[])
    e_sn = me.ListField(me.IntField(default=0), default=[])
    e_vert = me.ListField(me.IntField(default=0), default=[])
    dx = me.ListField(me.IntField(default=0), default=[])
    dy = me.ListField(me.IntField(default=0), default=[])
    
    # ! s_we = me.IntField(required=True)
    # ! e_we = me.IntField(required=True)
    # ! s_sn = me.IntField(required=True)
    # ! e_sn = me.IntField(required=True)
    # ! e_vert = me.IntField(required=True)
    # ! dx = me.IntField(required=True)
    # ! dy = me.IntField(required=True)
    # ! reasonable_time_step_ratio = me.FloatField(required=True)
    
    num_metgrid_levels = me.ListField(me.IntField(default=0), default=[])
    num_metgrid_soil_levels = me.ListField(me.IntField(default=0), default=[])
    grid_id = me.ListField(me.IntField(default=0), default=[])
    parent_id = me.ListField(me.IntField(default=0), default=[])
    i_parent_start = me.ListField(me.IntField(default=0), default=[])
    j_parent_start = me.ListField(me.IntField(default=0), default=[])
    parent_grid_ratio = me.ListField(me.IntField(default=0), default=[])
    parent_time_step_ratio = me.ListField(me.IntField(default=0), default=[])
    p_top_requested = me.ListField(me.IntField(default=0), default=[])
    feedback = me.ListField(me.IntField(default=0), default=[])
    # ! feedback = me.ListField(me.IntField(default=0), default=[])
    smooth_option = me.ListField(me.IntField(default=0), default=[])
    p_top_requested = me.ListField(me.IntField(default=0), default=[])
    zap_close_levels = me.ListField(me.IntField(default=0), default=[])
    interp_type = me.ListField(me.IntField(default=0), default=[])
    t_extrap_type = me.ListField(me.IntField(default=0), default=[])
    force_sfc_in_vinterp = me.ListField(me.IntField(default=0), default=[])
    use_levels_below_ground = me.ListField(me.BooleanField(), default=[])
    use_surface = me.ListField(me.BooleanField(), default=[])
    lagrange_order = me.ListField(me.IntField(default=0), default=[])
    sfcp_to_sfcp = me.ListField(me.BooleanField(), default=[])
    