from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField
from wtforms.validators import Required

class AddForm(FlaskForm):
    supplyer =   TextField('supplyer', validators = [Required()])
    title =     TextField('title', validators = [Required()])
    count = IntegerField('count', validators = [Required()])
    staffname = TextField('staffname', validators = [Required()])
    
class RemoveForm(FlaskForm):
    uname =   TextField('uname', validators = [Required()])
    title =     TextField('title', validators = [Required()])
    count = IntegerField('count', validators = [Required()])
    staffname = TextField('staffname', validators = [Required()])