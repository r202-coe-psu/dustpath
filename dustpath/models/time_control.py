import mongoengine as me
import datetime

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