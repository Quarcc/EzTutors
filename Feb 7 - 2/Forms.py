from wtforms import Form, StringField, FileField, SelectField, SelectMultipleField, validators, widgets
from wtforms.fields import EmailField
from wtforms.validators import Regexp
from wtforms_validators import AlphaSpace, AlphaNumeric


class CreateStudentAccount(Form):
    student_id_num = StringField('Identification Number', validators=[Regexp(regex='^(?=.{7}$)([S]{1}\d{2,6})$', message="Student Identification Number must only contain 'S' and 6 following digits. Eg. S123456")])
    student_first_name = StringField('First name', [validators.Length(min=1, max=150), AlphaSpace(message="First name should only contain alphabets")])
    student_last_name = StringField('Last Name', [validators.Length(min=1, max=150), AlphaSpace(message="Last name should only contain alphabets")])
    student_password = StringField('Password', validators=[Regexp(regex="^(?!\s*$).+", message="This is a required field")])
    student_mobile = StringField('Mobile Number (+65)', validators=[Regexp(regex=r"^[|6|8|9|]{1}\d{7}$", message="Mobile Number can only begin with '6', '8' or '9'. A valid mobile number should contain 8 digits.")])
    student_email = EmailField('Email Address', validators=[Regexp(regex="^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", message="Email is not valid")])
    student_education_level = SelectField('Education Level', choices=[('', 'Select'), ('P1', 'Primary 1'), ('P2', 'Primary 2'), ('P3', 'Primary 3'), ('P4', 'Primary 4'), ('P5', 'Primary 5'), ('P6', 'Primary 6')], validators=[Regexp(regex="^(?!\s*$).+", message="This is a required field")])
    student_class = SelectMultipleField('Subjects Enrolled', choices=[('ENG', 'English'), ('MATH', 'Mathematics'), ('SCI', 'Science')], option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False), render_kw={'style': 'list-style: none;'})
    student_img = FileField('Profile Picture')


class CreateTutorAccount(Form):
    tutor_id_num = StringField('Identification Number', validators=[Regexp(regex='^(?=.{7}$)([T]{1}\d{2,6})$', message="Tutor Identification Number must only contain 'T' and 6 following digits. Eg. T123456")])
    tutor_first_name = StringField('First name', [validators.Length(min=1, max=150), AlphaSpace(message="First name should only contain alphabets")])
    tutor_last_name = StringField('Last Name', [validators.Length(min=1, max=150), AlphaSpace(message="Last name should only contain alphabets")])
    tutor_password = StringField('Password', validators=[Regexp(regex="^(?!\s*$).+", message="This is a required field")])
    tutor_age = StringField('Age', validators=[Regexp(regex='(2[1-9]|[3-5][0-9]|6[0-5])', message="Age must be between 21 and 65 inclusively only")])
    tutor_mobile = StringField('Mobile Number (+65)', validators=[Regexp(regex=r"^[|6|8|9|]{1}\d{7}$", message="Mobile Number can only begin with '6', '8' or '9'. A valid mobile number should contain 8 digits.")])
    tutor_email = EmailField('Email Address', validators=[Regexp(regex="^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", message="Email is not valid")])
    tutor_teaching_level = SelectMultipleField('Teaching Level', choices=[('P1', 'Primary 1'), ('P2', 'Primary 2'), ('P3', 'Primary 3'), ('P4', 'Primary 4'), ('P5', 'Primary 5'), ('P6', 'Primary 6')], option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False), render_kw={'style': 'list-style: none;'})
    tutor_class = SelectMultipleField('Tutoring Classes', choices=[('ENG', 'English'), ('MATH', 'Mathematics'), ('SCI', 'Science')], option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False), render_kw={'style': 'list-style: none;'})


class CreateNotifications(Form):
    title = StringField('Notification Title', [validators.Length(min=1, max=120), AlphaNumeric(message="Notification Title should not contain any special characters")])
    description = StringField('Notification Description', [validators.Length(min=0, max=150)])


class LoginAccount(Form):
    id_num = StringField('Identification Number', [validators.Length(min=1, max=7), validators.DataRequired()])
    password = StringField('Password', [validators.Length(min=1, max=150), validators.DataRequired()])
