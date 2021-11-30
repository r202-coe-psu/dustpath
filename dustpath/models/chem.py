import mongoengine as me
import datetime

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