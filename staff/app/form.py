from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, IntegerField
from wtforms.validators import Required

class LoginForm(FlaskForm):
    uname =   TextField('uname', validators = [Required()])
    psw =     PasswordField('psw', validators = [Required()])
    
class RegForm(FlaskForm):
    adder_name =    TextField('adder_name', validators = [Required()])
    adder_psw =     PasswordField('adder_psw', validators = [Required()])
    uname =   TextField('uname', validators = [Required()])
    psw =     PasswordField('psw', validators = [Required()])
    rep_psw = PasswordField('rep_psw', validators = [Required()])
    rights = IntegerField('rights', validators = [Required()])