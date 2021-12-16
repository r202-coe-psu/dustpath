import mongoengine as me
import datetime

class BodyControl(me.Document):
    meta = {"collection": "bdy_control"}
    
    spec_bdy_width = me.ListField(me.IntField(default=0), default=[])
    spec_zone = me.ListField(me.IntField(default=0), default=[])
    relax_zone = me.ListField(me.IntField(default=0), default=[])
    specified = me.ListField(me.BooleanField(), default=[])
    nested = me.ListField(me.BooleanField(), default=[])
    
    
class Chem(me.Document):
    meta = {"collection": "chem"}
    
    kemit = me.ListField(me.IntField(default=0), default=[])
    # ! chem_opt = me.ListField(me.IntField(), default=[])
    chem_opt = me.ListField(me.IntField(default=0), default=[])
    # ! bioemdt = me.ListField(me.IntField(), default=[])
    photdt = me.ListField(me.IntField(default=0), default=[])
    chemdt = me.ListField(me.IntField(default=0), default=[])
    io_style_emissions = me.ListField(me.IntField(default=0), default=[])
    emiss_opt = me.ListField(me.IntField(default=0), default=[])
    emiss_opt_vol = me.ListField(me.IntField(default=0), default=[])
    emiss_ash_hgt = me.ListField(me.FloatField(), default=[])
    chem_in_opt = me.ListField(me.IntField(default=0), default=[])
    # ! chem_in_opt = me.ListField(me.IntField(default=0), default=[])
    # ! emiss_inpt_opt = me.ListField(me.IntField(default=0), default=[])
    phot_opt = me.ListField(me.IntField(default=0), default=[])
    gas_drydep_opt = me.ListField(me.IntField(default=0), default=[])
    aer_drydep_opt = me.ListField(me.IntField(default=0), default=[])
    bio_emiss_opt = me.ListField(me.IntField(default=0), default=[])
    ne_area = me.ListField(me.IntField(default=0), default=[])
    # ! dust_opt = me.ListField(me.IntField(default=0), default=[])
    dust_opt = me.ListField(me.IntField(default=0), default=[])
    dmsemis_opt = me.ListField(me.IntField(default=0), default=[]) 
    seas_opt = me.ListField(me.IntField(default=0), default=[])
    depo_fact = me.ListField(me.FloatField(), default=[])
    gas_bc_opt = me.ListField(me.IntField(default=0), default=[])
    gas_ic_opt = me.ListField(me.IntField(default=0), default=[])
    aer_bc_opt = me.ListField(me.IntField(default=0), default=[])
    aer_ic_opt = me.ListField(me.IntField(default=0), default=[])
    gaschem_onoff = me.ListField(me.IntField(default=0), default=[])
    aerchem_onoff = me.ListField(me.IntField(default=0), default=[])
    wetscav_onoff = me.ListField(me.IntField(default=0), default=[])
    cldchem_onoff = me.ListField(me.IntField(default=0), default=[])
    vertmix_onoff = me.ListField(me.IntField(default=0), default=[])
    chem_conv_tr = me.ListField(me.IntField(default=0), default=[])
    conv_tr_wetscav = me.ListField(me.IntField(default=0), default=[])
    conv_tr_aqchem = me.ListField(me.IntField(default=0), default=[])
    biomass_burn_opt = me.ListField(me.IntField(default=0), default=[])
    plumerisefire_frq = me.ListField(me.IntField(default=0), default=[])
    have_bcs_chem = me.ListField(me.BooleanField(), default=[])
    aer_ra_feedback = me.ListField(me.IntField(default=0), default=[])   
    # ! aer_ra_feedback = me.IntField(required=True)  
    aer_op_opt = me.ListField(me.IntField(default=0), default=[])  
    opt_pars_out = me.ListField(me.IntField(default=0), default=[])
    diagnostic_chem = me.ListField(me.IntField(default=0), default=[])
    

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
    

class Metgrid(me.Document):
    meta = {"collection": "metgrid"}
    
    fg_name = me.ListField(me.StringField())
    io_form_metgrid = me.ListField(me.IntField(default=0), default=[])
    

class NameListQuilt(me.Document):
    meta = {"collection": "namelist_quilt"}
    
    nio_tasks_per_group = me.ListField(me.IntField(default=0), default=[])
    nio_groups = me.ListField(me.IntField(default=0), default=[])
    

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


class Share(me.Document):
    meta = {"collection": "share"}
 
    wrf_core = me.ListField(me.StringField())
    max_dom = me.ListField(me.IntField(default=0), default=[])
    start_date = me.ListField(me.DateTimeField(), default=[])
    end_date = me.ListField(me.DateTimeField(), default=[])
    interval_seconds = me.ListField(me.IntField(default=0), default=[])
    io_form_geogrid = me.ListField(me.IntField(default=0), default=[])
    

class TimeControl(me.Document):
    meta = {"collection": "time_control"}

    run_days = me.ListField(me.IntField(default=0), default=[])
    run_hours = me.ListField(me.IntField(default=0), default=[])
    run_minutes = me.ListField(me.IntField(default=0), default=[])
    run_seconds = me.ListField(me.IntField(default=0), default=[])
    
    start_year = me.ListField(me.IntField(default=0), default=[])
    start_month = me.ListField(me.IntField(default=0), default=[])
    start_day = me.ListField(me.IntField(default=0), default=[])
    start_hour = me.ListField(me.IntField(default=0), default=[])
    start_minute = me.ListField(me.IntField(default=0), default=[])
    start_second = me.ListField(me.IntField(default=0), default=[])
    
    end_year = me.ListField(me.IntField(default=0), default=[])
    end_month = me.ListField(me.IntField(default=0), default=[])
    end_day = me.ListField(me.IntField(default=0), default=[])
    end_hour = me.ListField(me.IntField(default=0), default=[])
    end_minute = me.ListField(me.IntField(default=0), default=[])
    end_second = me.ListField(me.IntField(default=0), default=[])
    
    interval_seconds = me.ListField(me.IntField(default=0), default=[])
    history_interval = me.ListField(me.IntField(default=0), default=[])
    frames_per_outfile = me.ListField(me.IntField(default=0), default=[])
    
    restart = me.ListField(me.BooleanField(), default=[])
    #! restart  
    restart_interval = me.ListField(me.IntField(default=0), default=[])
    
    io_form_history = me.ListField(me.IntField(default=0), default=[])
    io_form_restart = me.ListField(me.IntField(default=0), default=[])
    io_form_input = me.ListField(me.IntField(default=0), default=[])
    io_form_boundary = me.ListField(me.IntField(default=0), default=[])
   
    # ! auxinput6_inname  
    # ! auxinput6_inname
    # ! auxinput7_inname
    # ! auxinput7_inname
    # ! auxinput8_inname
    # ! auxinput12_inname
    auxinput5_interval_m = me.ListField(me.IntField(default=0), default=[])
    auxinput7_interval_m = me.ListField(me.IntField(default=0), default=[])
    auxinput8_interval_m = me.ListField(me.IntField(default=0), default=[])
    
    io_form_auxinput2 = me.ListField(me.IntField(default=0), default=[])
    io_form_auxinput5 = me.ListField(me.IntField(default=0), default=[])
    io_form_auxinput6 = me.ListField(me.IntField(default=0), default=[])
    io_form_auxinput7 = me.ListField(me.IntField(default=0), default=[])
    io_form_auxinput8 = me.ListField(me.IntField(default=0), default=[])
    io_form_auxinput12 = me.ListField(me.IntField(default=0), default=[])
    
    debug_level = me.ListField(me.IntField(default=0), default=[])
    
    auxinput1_inname = me.ListField(me.StringField())
    auxinput13_inname = me.ListField(me.StringField())
    auxinput13_interval_m = me.ListField(me.IntField(default=0), default=[])
    
    io_form_auxinput13 = me.ListField(me.IntField(default=0), default=[])
    

class Ungrib(me.Document):
    meta = {"collection": "ungrib"}
    
    out_format = me.ListField(me.StringField())
    prefix = me.ListField(me.StringField())