from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import Required

class LoginForm(FlaskForm):
    uname =   TextField('uname', validators = [Required()])
    psw =     PasswordField('psw', validators = [Required()])
    
class RegForm(FlaskForm):
    mail =    TextField('mail', validators = [Required()])
    rep_psw = PasswordField('rep_psw', validators = [Required()])
    uname =   TextField('uname', validators = [Required()])
    psw =     PasswordField('psw', validators = [Required()])