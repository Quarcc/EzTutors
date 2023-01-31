from wtforms import Form, StringField, BooleanField, IntegerField, validators
from wtforms.fields import EmailField
from wtforms.validators import Regexp
from wtforms_validators import AlphaSpace, AlphaNumeric


class CreateStudentAccount(Form):
    student_id_num = StringField('Identification Number', validators=[Regexp(regex='^(?=.{7}$)([S]{1}\d{2,6})$', message="Student Identification Number must only contain 'S' and 6 following digits. Eg. S123456")])
    student_first_name = StringField('First name', [validators.Length(min=1, max=150), AlphaSpace(message="First name should only contain alphabets")])
    student_last_name = StringField('Last Name', [validators.Length(min=1, max=150), AlphaSpace(message="Last name should only contain alphabets")])
    student_password = StringField('Password', validators=[Regexp(regex="/^(?!\s*$).+/", message="This is a required field")])
    student_mobile = StringField('Mobile Number', validators=[Regexp(regex=r"\[|6|8|9|]\d{7}", message="Mobile Number can only begin with '6', '8' or '9'. A valid mobile number should contain 8 digits.")])
    student_email = EmailField('Email Address', validators=[Regexp(regex="/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/", message="Email is not valid")])
    student_p1 = BooleanField('p1')
    student_p2 = BooleanField('p2')
    student_p3 = BooleanField('p3')
    student_p4 = BooleanField('p4')
    student_p5 = BooleanField('p5')
    student_p6 = BooleanField('p6')
    student_math = BooleanField('Math')
    student_english = BooleanField('English')
    student_science = BooleanField('Science')


class CreateTutorAccount(Form):
    tutor_id_num = StringField('Identification Number', validators=[Regexp(regex='^(?=.{7}$)([T]{1}\d{2,6})$', message="Student Identification Number must only contain 'S' and 6 following digits. Eg. S123456")])
    tutor_first_name = StringField('First name', [validators.Length(min=1, max=150), AlphaSpace(message="First name should only contain alphabets")])
    tutor_last_name = StringField('Last Name', [validators.Length(min=1, max=150), AlphaSpace(message="Last name should only contain alphabets")])
    tutor_password = StringField('Password', validators=[Regexp(regex="/^(?!\s*$).+/", message="This is a required field")])
    tutor_age = IntegerField('Age', validators=[Regexp(regex='/^(1[89]|[2-9]\d)$/gm', message="Age must be between 18 and 99 only")])
    tutor_mobile = StringField('Mobile Number', validators=[Regexp(regex=r"\[|6|8|9|]\d{7}", message="Mobile Number can only begin with '6', '8' or '9'. A valid mobile number should contain 8 digits.")])
    tutor_email = EmailField('Email Address', validators=[Regexp(regex="/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/", message="Email is not valid")])
    tutor_p1 = BooleanField('p1')
    tutor_p2 = BooleanField('p2')
    tutor_p3 = BooleanField('p3')
    tutor_p4 = BooleanField('p4')
    tutor_p5 = BooleanField('p5')
    tutor_p6 = BooleanField('p6')
    tutor_math = BooleanField('Math')
    tutor_english = BooleanField('English')
    tutor_science = BooleanField('Science')


class CreateNotifications(Form):
    title = StringField('Notification Title', [validators.Length(min=1, max=120), AlphaNumeric(message="Notification Title should not contain any special characters")])
    description = StringField('Notification Description', [validators.Length(min=0, max=150)])


class LoginAccount(Form):
    id_num = StringField('Identification Number', [validators.Length(min=1, max=7), validators.DataRequired()])
    password = StringField('Password', [validators.Length(min=1, max=150), validators.DataRequired()])
