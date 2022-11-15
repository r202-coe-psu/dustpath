from flask_wtf import FlaskForm
from wtforms import fields
# from wtforms.fields import html5
from wtforms import validators
from wtforms.widgets import TextInput

class ProjectForm(FlaskForm):
    name = fields.StringField('Project Name', validators=[validators.Length(min=1)])
    domain = fields.SelectField('Domain')
    # max_domain = fields.IntegerField('จำนวนโดเมน',
    #                                 default=1, 
    #                                 validators=[
    #                                     validators.InputRequired(),
    #                                     validators.NumberRange(min=1, message="จำนวนโดเมนน้อยเกินไป"),
    #                                 ])
    start_date = fields.DateField('Simulation Start Date',
                                    format='%d-%m-%Y',
                                    widget=TextInput())
    end_date = fields.DateField('Simulation End Date',
                                    format='%d-%m-%Y',
                                    widget=TextInput())