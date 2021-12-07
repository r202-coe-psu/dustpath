from flask_wtf import FlaskForm
from wtforms import Form, Field, validators, fields
from wtforms.widgets import ListWidget, CheckboxInput, TextArea, TextInput
import datetime


class InputListField(Field):
    widget = TextArea()

    def _value(self):
        if self.data:
            return ", ".join(self.data)
        else:
            return ""

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [
                x.strip() for x in valuelist[0].split(",") if len(x.strip()) > 0
            ]
        else:
            self.data = []

class BodyControlForm(FlaskForm):
    spec_bdy_width = InputListField("spec_bdy_width")
    spec_zone = InputListField("spec_zone")
    relax_zone = InputListField("relax_zone")
    # specified = me.ListField(me.BooleanField(), default=[])
    # nested = me.ListField(me.BooleanField(), default=[])