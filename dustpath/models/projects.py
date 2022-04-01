from bson.json_util import default
import mongoengine as me
import datetime

class WrfConfiguration(me.EmbeddedDocument):
    # max_domain = me.IntField(required=True, default=1)
    start_date = me.DateField(required=True)
    end_date = me.DateField(required=True)
    domain = me.ReferenceField("Domain", dbref=True)

class Status(me.EmbeddedDocument):
    # max_domain = me.IntField(required=True, default=1)
    copy_project = me.StringField(required=True, default='')
    write_namelist_wps = me.StringField(required=True, default='')
    link_geogrid_table = me.StringField(required=True, default='')
    run_geogrid = me.StringField(required=True, default='')
    link_gfs_file = me.StringField(required=True, default='')
    link_Vtable = me.StringField(required=True, default='')
    run_ungrib = me.StringField(required=True, default='')
    run_metgrid = me.StringField(required=True, default='')
    link_met_data = me.StringField(required=True, default='')

    write_no_emiss_namelist_input = me.StringField(required=True, default='')
    run_real_1 = me.StringField(required=True, default='')
    write_prep_chem_src_input = me.StringField(required=True, default='')
    run_prep_chem_src = me.StringField(required=True, default='')
    link_prep_chem_src = me.StringField(required=True, default='')
    write_emiss_namelist_input = me.StringField(required=True, default='')
    convert_emission = me.StringField(required=True, default='')
    
    link_chemi = me.StringField(required=True, default='')
    run_real_2 = me.StringField(required=True, default='')

    run_wrf = me.StringField(required=True, default='')
    plot = me.StringField(required=True, default='')
    generate_GIF = me.StringField(required=True, default='')
    create_tumbon_table = me.StringField(required=True, default='')
class Project(me.Document):
    meta = {"collection": "projects"}
    
    name = me.StringField(default="")
    wrf_config = me.EmbeddedDocumentField(WrfConfiguration, default=WrfConfiguration)
    status = me.EmbeddedDocumentField(Status, default=Status)
    output_filename = me.StringField(required=True, default="")
    # has_token = me.BooleanField(default=False)
    # line_notify_token = me.StringField(default="")
    # owner = me.ReferenceField("User", dbref=True, required=True)
    # assistant = me.ListField(me.ReferenceField("User", dbref=True))
    # users = me.ListField(me.ReferenceField("User", dbref=True))
    # security_guard = me.ListField(me.ReferenceField("User", dbref=True))
    # status = me.StringField(required=True, default="active")
    
    created_date = me.DateTimeField(required=True, default=datetime.datetime.now)
    updated_date = me.DateTimeField(
        required=True, default=datetime.datetime.now, auto_now=True
    )

    # @property
    # def is_owner(self, user):
    #     if user.is_admin:
    #         return True
    #     if self.owner.id == user.id:
    #         return True
    #     return False