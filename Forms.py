from wtforms import Form, StringField, HiddenField, FileField, SelectField, TextAreaField, SelectMultipleField, MultipleFileField, validators, widgets, ValidationError
from wtforms.fields import EmailField
from wtforms.validators import Regexp
from wtforms_validators import AlphaSpace
from flask_wtf.file import FileAllowed


def account(form, field):
    if field.data == "":
        raise ValidationError('This is a required field')
    if not field.data.isalpha():
        raise ValidationError('Your field should only alphabets')
    if len(field.data)>120:
        raise ValidationError('Your field must be less than 120 characters')


class CreateStudentAccount(Form):
    student_id_num = StringField('Identification Number', validators=[Regexp(regex='^(?=.{7}$)([S]{1}\d{2,6})$', message="Student Identification Number must only contain 'S' and 6 following digits. Eg. S123456")])
    student_first_name = StringField('First name', [account])
    student_last_name = StringField('Last Name', [account])
    student_password = StringField('Password', validators=[Regexp(regex="^(?!\s*$).+", message="This is a required field")])
    student_mobile = StringField('Mobile Number (+65)', validators=[Regexp(regex=r"^[|6|8|9|]{1}\d{7}$", message="Mobile Number can only begin with '6', '8' or '9'. A valid mobile number should contain 8 digits.")])
    student_email = EmailField('Email Address', validators=[Regexp(regex="^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", message="Email is not valid")])
    student_education_level = SelectField('Education Level', choices=[('', 'Select'), ('P1', 'Primary 1'), ('P2', 'Primary 2'), ('P3', 'Primary 3'), ('P4', 'Primary 4'), ('P5', 'Primary 5'), ('P6', 'Primary 6')], validators=[Regexp(regex="^(?!\s*$).+", message="This is a required field")])
    student_class = SelectMultipleField('Subjects Enrolled', choices=[('ENG', 'English'), ('MATH', 'Mathematics'), ('SCI', 'Science')], option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False), render_kw={'style': 'list-style: none;'})
    student_img = FileField("Profile Picture (Optional)")


class CreateTutorAccount(Form):
    tutor_id_num = StringField('Identification Number', validators=[Regexp(regex='^(?=.{7}$)([T]{1}\d{2,6})$', message="Tutor Identification Number must only contain 'T' and 6 following digits. Eg. T123456")])
    tutor_first_name = StringField('First name', [account])
    tutor_last_name = StringField('Last Name', [account])
    tutor_password = StringField('Password', validators=[Regexp(regex="^(?!\s*$).+", message="This is a required field")])
    tutor_age = StringField('Age', validators=[Regexp(regex='(2[1-9]|[3-5][0-9]|6[0-5])', message="Age must only be between 21 and 65 inclusively")])
    tutor_mobile = StringField('Mobile Number (+65)', validators=[Regexp(regex=r"^[|6|8|9|]{1}\d{7}$", message="Mobile Number can only begin with '6', '8' or '9'. A valid mobile number should contain 8 digits.")])
    tutor_email = EmailField('Email Address', validators=[Regexp(regex="^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", message="Email is not valid")])
    tutor_teaching_level = SelectMultipleField('Teaching Level', choices=[('P1', 'Primary 1'), ('P2', 'Primary 2'), ('P3', 'Primary 3'), ('P4', 'Primary 4'), ('P5', 'Primary 5'), ('P6', 'Primary 6')], option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False), render_kw={'style': 'list-style: none;'})
    tutor_class = SelectMultipleField('Tutoring Classes', choices=[('ENG', 'English'), ('MATH', 'Mathematics'), ('SCI', 'Science')], option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False), render_kw={'style': 'list-style: none;'})
    tutor_img = FileField("Profile Picture (Optional)")


class CreateNotifications(Form):
    target_user = StringField('Target User', validators=[Regexp(regex='^(?=.{7}$)([S,T]{1}\d{2,6})$', message="Identification Number must only contain 'T' or 'S' and 6 following digits. Eg. T123456")])
    title = StringField('Notification Title', [account])
    description = StringField('Notification Description', [validators.Length(min=0, max=120)])


class CreateTodo(Form):
    text = StringField('', validators=[Regexp(regex="^(?!\s*$).+", message="This is a required field")])


class LoginAccount(Form):
    id_num = StringField('Identification Number', validators=[Regexp(regex="^(?!\s*$).+", message="This is a required field")], render_kw={"placeholder": "Identification Number"})
    password = StringField('Password', validators=[Regexp(regex="^(?!\s*$).+", message="This is a required field")], render_kw={"placeholder": "Password"})


class CreateTestQuestion(Form):
    content_id = StringField('Test Paper Number', validators=[Regexp(regex='^(?=.{7}$)([T]{1}[E,M,S]{1}\d{3,7})$', message='Your Content ID should be in T(E/M/S)12345 format ')], default='T')
    content_subject = SelectField('Subject: ', validators=[Regexp(regex='^(?!\s*$).+', message='Please select')], choices=[('', 'Select'), ('ENG', 'English'), ('MATH', 'Mathematics'), ('SCI', 'Science')], default='')
    marks = StringField("Marks", validators=[Regexp(regex='^[0]{1}$', message='Marks must be 0')], default='0')
    q1 = StringField("Question 1", validators=[Regexp(regex='^[a-zA-Z-0-9-\/+*--(){}^=]+', message="Question cannot be empty")])
    a1 = StringField("Question 1 Answer",  validators=[Regexp(regex='^[a-zA-Z-0-9-\/+*--(){}^=]+', message="Answer cannot be empty")])
    q2 = StringField("Question 2",  validators=[Regexp(regex='^[a-zA-Z-0-9-\/+*--(){}^=]+', message="Question cannot be empty")])
    a2 = StringField("Question 2 Answer",  validators=[Regexp(regex='^[a-zA-Z-0-9-\/+*--(){}^=]+', message="Answer cannot be empty")])
    q3 = StringField("Question 3",  validators=[Regexp(regex='^[a-zA-Z-0-9-\/+*--(){}^=]+', message="Question cannot be empty")])
    a3 = StringField("Question 3 Answer",  validators=[Regexp(regex='^[a-zA-Z-0-9-\/+*--(){}^=]+', message="Answer cannot be empty")])


class StudentTestQuestion(Form):
    content_id = HiddenField('Revision Paper Number', validators=[Regexp(regex='^(?=.{7}$)([R]{1}[E,M,S]{1}\d{3,7})$', message='Your Content ID should be in R(E/M/S)12345 format ')])
    content_subject = HiddenField('Subject', validators=[Regexp(regex='^[A-Z][a-z]{3,19}$', message="Subject should be English, Math or Science")])
    q1 = HiddenField("Question 1", validators=[Regexp(regex='^[a-zA-Z-0-9-\/+*--(){}^=]+', message="Question cannot be empty")])
    a1 = StringField("Question 1 Answer",  validators=[Regexp(regex='^[a-zA-Z-0-9-\/+*--(){}^=]+', message="Answer cannot be empty")])
    q2 = HiddenField("Question 2",  validators=[Regexp(regex='^[a-zA-Z-0-9-\/+*--(){}^=]+', message="Question cannot be empty")])
    a2 = StringField("Question 2 Answer",  validators=[Regexp(regex='^[a-zA-Z-0-9-\/+*--(){}^=]+', message="Answer cannot be empty")])
    q3 = HiddenField("Question 3",  validators=[Regexp(regex='^[a-zA-Z-0-9-\/+*--(){}^=]+', message="Question cannot be empty")])
    a3 = StringField("Question 3 Answer",  validators=[Regexp(regex='^[a-zA-Z-0-9-\/+*--(){}^=]+', message="Answer cannot be empty")])


class CreateFeedback(Form):
    feedback_name = HiddenField('Name')
    feedback_adminid = HiddenField('Admin ID')
    feedback_subject = SelectField('Subject Type', validators=[Regexp(regex='^(?!\s*$).+', message='Please select')], choices=[('', 'Select'), ('Academic Assistance', 'Academic Assistance'), ('System Errors', 'System Error')], default='')
    feedback_title = StringField('Feedback Title', validators=[Regexp(regex="^(?!\s*$).+", message='This is a required field.')])
    feedback_description = TextAreaField('Description', validators=[Regexp(regex="^(?!\s*$).+", message='This is a required field.')])
    feedback_file = FileField('Upload an Attachment (Optional)', validators=[FileAllowed(['pdf', 'docx', 'jpg', 'png', 'jpeg'], message='Invalid File Type')])


class CreateAnnouncementForm(Form):
    atitle = StringField('Announcement Title', validators=[Regexp(regex="^(?!\s*$).+", message="This is a required field")])
    acontent = TextAreaField('Announcement Description', validators=[Regexp(regex="^(?!\s*$).+", message="This is a required field")])
    id_num = HiddenField('Tutor ID')
    afiles = MultipleFileField('Upload Files Here (Optional):')


class CreateStudentContent(Form):
    content_subject = SelectField('Subject: ', validators=[Regexp(regex='^(?!\s*$).+', message='Please select')],
                                  choices=[('', 'Select'), ('ENG', 'English'), ('MATH', 'Mathematics'),
                                           ('SCI', 'Science')], default='')
    cname = StringField('Content Title')
    cfile = FileField('Upload Content File')
