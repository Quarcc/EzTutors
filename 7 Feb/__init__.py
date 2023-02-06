from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, g
from Forms import CreateStudentAccount, LoginAccount, CreateTutorAccount, CreateNotifications
import shelve, Notification, os, pickle
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import uuid as uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eztutors.db'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
app.config['SQLALCHEMY_SILENCE_UBER_WARNING'] = True
app.secret_key = os.urandom(24)  # generate a random secret key
db = SQLAlchemy(app)


class Student(db.Model):
    student_id_num = db.Column("id_num", db.String(7), primary_key=True)
    student_first_name = db.Column("first_name", db.String(80))
    student_last_name = db.Column("last_name", db.String(80))
    student_password = db.Column("password", db.String(127))
    student_mobile = db.Column("mobile", db.String(8))
    student_email = db.Column("email", db.String(150))
    student_education_level = db.Column("education level", db.String)
    student_class = db.Column("student class(es)", db.String)
    student_img = db.Column("Profile Picture", db.String)

    def __init__(self, student_id_num, student_first_name, student_last_name, student_password, student_mobile, student_email, student_education_level, student_class, student_img):
        self.student_id_num = student_id_num
        self.student_first_name = student_first_name
        self.student_last_name = student_last_name
        self.student_password = student_password
        self.student_mobile = student_mobile
        self.student_email = student_email
        self.student_education_level = student_education_level
        self.student_class = student_class
        self.student_img = student_img


class Tutor(db.Model):

    tutor_id_num = db.Column("id_num", db.String(7), primary_key=True)
    tutor_first_name = db.Column("first_name", db.String(80))
    tutor_last_name = db.Column("last_name", db.String(80))
    tutor_password = db.Column("password", db.String(127))
    tutor_age = db.Column("age", db.String(2))
    tutor_mobile = db.Column("mobile", db.String(8))
    tutor_email = db.Column("email", db.String(150))
    tutor_teaching_level = db.Column("teaching level", db.String)
    tutor_class = db.Column("tutor class(es)", db.String)

    def __init__(self, tutor_id_num, tutor_first_name, tutor_last_name, tutor_password, tutor_age, tutor_mobile, tutor_email, tutor_teaching_level, tutor_class):
        self.tutor_id_num = tutor_id_num
        self.tutor_first_name = tutor_first_name
        self.tutor_last_name = tutor_last_name
        self.tutor_password = tutor_password
        self.tutor_age = tutor_age
        self.tutor_mobile = tutor_mobile
        self.tutor_email = tutor_email
        self.tutor_teaching_level = tutor_teaching_level
        self.tutor_class = tutor_class


class Admin(db.Model):
    admin_id_num = db.Column("id_num", db.String(7), primary_key=True)
    admin_first_name = db.Column("first_name", db.String(80))
    admin_last_name = db.Column("last_name", db.String(80))
    admin_password = db.Column("password", db.String(127))
    admin_mobile = db.Column("mobile", db.Integer)
    admin_email = db.Column("email", db.String(150))

    def __init__(self, admin_id_num, admin_first_name, admin_last_name, admin_password, admin_mobile, admin_email):
        self.admin_id_num = admin_id_num
        self.admin_first_name = admin_first_name
        self.admin_last_name = admin_last_name
        self.admin_password = admin_password
        self.admin_mobile = admin_mobile
        self.admin_email = admin_email


@app.before_request
def before_request():
    g.user = None

    if 'user' in session:
        g.user = session['user']


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/studentlogin', methods=['POST', 'GET'])
def student_login():
    student_login_form = LoginAccount(request.form)
    if request.method == 'POST' and student_login_form.validate():
        session.pop('user', None)

    student_account = Student.query.all()

    for i in student_account:
        student_id = i.student_id_num
        if student_id == student_login_form.id_num.data:
            student_info = Student.query.filter_by(student_id_num=student_login_form.id_num.data).first()
            student_pass = student_info.student_password

            if student_pass == student_login_form.password.data:
                session['user'] = student_login_form.id_num.data

                return redirect(url_for('retrieve_student_account'))

    return render_template('studentlogin.html')


@app.route('/tutorlogin', methods=['POST', 'GET'])
def tutor_login():
    tutor_login_form = LoginAccount(request.form)
    if request.method == 'POST' and tutor_login_form.validate():
        session.pop('user', None)

    try:
        tutor_account = Tutor.query.all()
        for j in tutor_account:
            tutor_id = j.tutor_id_num
            if tutor_id == tutor_login_form.id_num.data:
                tutor_info = Tutor.query.filter_by(id_num=tutor_login_form.id_num.data).first()
                tutor_pass = tutor_info.tutor_password

                if tutor_pass == tutor_login_form.password.data:
                    session['user'] = tutor_login_form.id_num.data

                    return redirect(url_for('retrieve_tutor_account'))

    except:
        admin_account = Admin.query.all()
        for i in admin_account:
            admin_id = i.admin_id_num
            if admin_id == tutor_login_form.id_num.data:
                admin_info = Admin.query.filter_by(admin_id_num=tutor_login_form.id_num.data).first()
                admin_pass = admin_info.admin_password

                if admin_pass == tutor_login_form.password.data:
                    session['user'] = tutor_login_form.id_num.data

                    return redirect(url_for('retrieve_tutor_account'))

    return render_template('tutorlogin.html')


@app.route("/adminMain")
def admin_main():
    if g.user:
        id_num = session['user']
        return render_template('adminMain.html')


@app.route('/createstudent', methods=['GET', 'POST'])
def create_student_account():
    create_student_form = CreateStudentAccount(request.form)
    if request.method == 'POST' and create_student_form.validate():
        with app.app_context():
            db.create_all()

            student_id_num = request.form['student_id_num']
            student_first_name = request.form['student_first_name']
            student_last_name = request.form['student_last_name']
            student_password = request.form['student_password']
            student_mobile = request.form['student_mobile']
            student_email = request.form['student_email']
            student_education_level = request.form['student_education_level']
            student_class = pickle.dumps(create_student_form.student_class.data)
            student_img = request.files['student_img']
            student_img_filename = secure_filename(student_img.filename)
            img_name = str(uuid.uuid1()) + "_" + student_img_filename
            student_img = img_name

            student = Student(student_id_num, student_first_name, student_last_name, student_password, student_mobile, student_email, student_education_level, student_class, student_img)
            db.session.add(student)
            db.session.commit()

        return redirect(url_for('retrieve_student_account'))
    return render_template('createstudent.html', form=create_student_form)


@app.route('/retrievestudent')
def retrieve_student_account():
    update_student_account = CreateStudentAccount(request.form)
    with app.app_context():
        student_data = Student.query.all()

    for j in student_data:
        student_education_level = j.student_education_level

    for i in student_data:
        student_class_list = i.student_class
        student_class_list = pickle.loads(student_class_list)
        student_class = ', '.join(student_class_list)

    return render_template('retrievestudent.html', count=len(student_data), student=student_data, student_education_level=student_education_level, student_classes=student_class, student_class_list=student_class_list, form=update_student_account)


@app.route('/updatestudent', methods=['GET', 'POST'])
def update_student_account():
    update_student_form = CreateStudentAccount(request.form)
    if request.method == 'POST' and update_student_form.validate():
        with app.app_context():
            student_data = Student.query.get(request.form.get('student_id_num'))

            student_data.student_id_num = request.form['student_id_num']
            student_data.student_first_name = request.form['student_first_name']
            student_data.student_last_name = request.form['student_last_name']
            student_data.student_password = request.form['student_password']
            student_data.student_mobile = request.form['student_mobile']
            student_data.student_email = request.form['student_email']
            student_data.student_education_level = request.form['student_education_level']
            student_data.student_class = pickle.dumps(update_student_form.student_class.data)

            db.session.commit()
            return redirect(url_for('retrieve_student_account'))


@app.route('/deletestudent/<string:student_id_num>', methods=['POST'])
def delete_student_account(student_id_num):
    student_data = Student.query.get(student_id_num)
    db.session.delete(student_data)
    db.session.commit()

    return redirect(url_for('retrieve_student_account'))


@app.route('/createtutor', methods=['GET', 'POST'])
def create_tutor_account():
        create_tutor_form = CreateTutorAccount(request.form)
        if request.method == 'POST' and create_tutor_form.validate():
            with app.app_context():
                db.create_all()

                tutor_id_num = request.form['tutor_id_num']
                tutor_first_name = request.form['tutor_first_name']
                tutor_last_name = request.form['tutor_last_name']
                tutor_password = request.form['tutor_password']
                tutor_age = request.form['tutor_age']
                tutor_mobile = request.form['tutor_mobile']
                tutor_email = request.form['tutor_email']
                tutor_teaching_level = pickle.dumps(create_tutor_form.tutor_teaching_level.data)
                tutor_class = pickle.dumps(create_tutor_form.tutor_class.data)
                
                tutor = Tutor(tutor_id_num, tutor_first_name, tutor_last_name, tutor_password, tutor_age, tutor_mobile, tutor_email, tutor_teaching_level, tutor_class)
                db.session.add(tutor)
                db.session.commit()

            return redirect(url_for('retrieve_tutor_account'))
        return render_template('createtutor.html', form=create_tutor_form)


@app.route('/retrievetutor')
def retrieve_tutor_account():
    if g.user:
        id_num = session['user']
        update_tutor_form = CreateTutorAccount(request.form)
        with app.app_context():
            tutor_data = Tutor.query.all()
            
        for j in tutor_data:
            tutor_teaching_level = j.tutor_teaching_level
            tutor_teaching_level = pickle.loads(tutor_teaching_level)
            tutor_teach = ', '.join(tutor_teaching_level)

        for i in tutor_data:
            tutor_class_list = i.tutor_class
            tutor_class_list = pickle.loads(tutor_class_list)
            tutor_class = ', '.join(tutor_class_list)

        return render_template('retrievetutor.html', count=len(tutor_data), tutor=tutor_data, tutor_teaching=tutor_teach, tutor_teaching_level=tutor_teaching_level, tutor_classes=tutor_class, tutor_class_list=tutor_class_list,form=update_tutor_form)
    return redirect(url_for('tutor_login'))


@app.route('/updatetutor', methods=['GET', 'POST'])
def update_tutor_account():
    update_tutor_form = CreateTutorAccount(request.form)
    if request.method == 'POST' and update_tutor_form.validate():
        with app.app_context():
            tutor_data = Tutor.query.get(request.form.get('tutor_id_num'))

            tutor_data.tutor_id_num = request.form['tutor_id_num']
            tutor_data.tutor_first_name = request.form['tutor_first_name']
            tutor_data.tutor_last_name = request.form['tutor_last_name']
            tutor_data.tutor_password = request.form['tutor_password']
            tutor_data.tutor_age = request.form['tutor_age']
            tutor_data.tutor_mobile = request.form['tutor_mobile']
            tutor_data.tutor_email = request.form['tutor_email']
            tutor_data.tutor_teaching_level = pickle.dumps(update_tutor_form.tutor_teaching_level.data)
            tutor_data.tutor_class = pickle.dumps(update_tutor_form.tutor_class.data)

            db.session.commit()
            return redirect(url_for('retrieve_tutor_account'))


@app.route('/deletetutor/<string:tutor_id_num>', methods=['POST'])
def delete_tutor_account(tutor_id_num):
    tutor_data = Tutor.query.get(tutor_id_num)
    db.session.delete(tutor_data)
    db.session.commit()

    return redirect(url_for('retrieve_tutor_account'))


@app.route('/createNotification', methods=['GET', 'POST'])
def create_notification():
    create_notification_form = CreateNotifications(request.form)
    if request.method == 'POST' and create_notification_form.validate():
        notification_dict = {}
        db = shelve.open('notification.db', 'c')

        try:
            notification_dict = db['Notification']
        except:
            print("Error in retrieving Notifications from Database")

        date = datetime.now()
        notification = Notification.Notification(date, create_notification_form.title.data, create_notification_form.description.data)
        notification_dict[notification.get_notif_id()] = notification
        db['Notification'] = notification_dict

        db.close()

        return redirect(url_for('tutor_login'))
    return render_template('createNotification.html', form=create_notification_form)


@app.route('/retrieveNotification')
def retrieve_notification():
    notification_dict = {}
    db = shelve.open('notification.db', 'r')
    notification_dict = db['Notification']
    db.close()

    notification_list = []
    for key in notification_dict:
        notif = notification_dict.get(key)
        notification_list.append(notif)

    return render_template('retrieveNotification.html', count=len(notification_list), notification_list=notification_list)


@app.route('/updateNotification/<int:notif_id>/', methods=['GET', 'POST'])
def update_notification(notif_id):
    update_notification_form = CreateNotifications(request.form)
    if request.method == 'POST' and update_notification_form.validate():
        notification_dict = {}
        db = shelve.open('notification.db', 'w')
        notification_dict = db['Notification']

        notif = notification_dict.get(notif_id)
        notif.set_title(update_notification_form.title.data)
        notif.set_description(update_notification_form.description.data)

        db['Notification'] = notification_dict
        db.close()

        return redirect(url_for('retrieve_notification'))
    else:
        notification_dict = {}
        db = shelve.open('notification.db', 'r')
        notification_dict = db['Notification']
        db.close()

        notif = notification_dict.get(notif_id)
        update_notification_form.title.data = notif.get_title()
        update_notification_form.description.data = notif.description()

    return render_template('updateNotification.html', form=update_notification_form)


@app.route('/deleteNotification/<int:notif_id>', methods=['POST'])
def delete_notification(notif_id):
    notification_dict = {}
    db = shelve.open('notification.db', 'w')
    notification_dict = db['Notification']

    notification_dict.pop(notif_id)

    db['Notification'] = notification_dict
    db.close()

    return redirect(url_for('retrieve_notification'))


@app.route('/dropsession')
def drop_session():
    session.pop('user', None)
    return render_template('main.html')


if __name__ == '__main__':
    app.run(debug=True)
