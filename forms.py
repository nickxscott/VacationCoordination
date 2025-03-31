from flask_wtf import FlaskForm
from wtforms import SelectField,StringField, FieldList,FormField,SelectMultipleField
from wtforms.validators import InputRequired, Optional

class holidayForm(FlaskForm):
	user=SelectField('Job Creator', choices=['Joe', 'Taylor', 'Hayden', 'Nick'])
	holiday=SelectMultipleField('Holidays')




