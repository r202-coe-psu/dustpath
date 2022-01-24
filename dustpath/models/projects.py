from bson.json_util import default
import mongoengine as me
import datetime

class WrfConfiguration(me.EmbeddedDocument):
    # max_domain = me.IntField(required=True, default=1)
    start_date = me.DateField(required=True)
    end_date = me.DateField(required=True)
    domain = me.ReferenceField("Domain", dbref=True)

class Project(me.Document):
    meta = {"collection": "projects"}
    
    name = me.StringField(default="")
    wrf_config = me.EmbeddedDocumentField(WrfConfiguration, default=WrfConfiguration)
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