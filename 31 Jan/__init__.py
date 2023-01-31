from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, g
from Forms import CreateStudentAccount, LoginAccount, CreateTutorAccount, CreateNotifications
import shelve, Notification, os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eztutors.db'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
app.secret_key = os.urandom(24)  # generate a random secret key
db = SQLAlchemy(app)


class Student(db.Model):
    student_id_num = db.Column("id_num", db.String(7), primary_key=True)
    student_first_name = db.Column("first_name", db.String(80))
    student_last_name = db.Column("last_name", db.String(80))
    student_password = db.Column("password", db.String(127))
    student_mobile = db.Column("mobile", db.Integer)
    student_email = db.Column("email", db.String(150))
    student_p1 = db.Column("p1", db.Boolean, default=False)
    student_p2 = db.Column("p2", db.Boolean, default=False)
    student_p3 = db.Column("p3", db.Boolean, default=False)
    student_p4 = db.Column("p4", db.Boolean, default=False)
    student_p5 = db.Column("p5", db.Boolean, default=False)
    student_p6 = db.Column("p6", db.Boolean, default=False)
    student_english = db.Column("english", db.Boolean)
    student_math = db.Column("math", db.Boolean)
    student_science = db.Column("science", db.Boolean)

    def __init__(self, student_id_num, student_first_name, student_last_name, student_password, student_mobile, student_email, student_p1, student_p2, student_p3, student_p4, student_p5, student_p6, student_english, student_math, student_science):
        self.student_id_num = student_id_num
        self.student_first_name = student_first_name
        self.student_last_name = student_last_name
        self.student_password = student_password
        self.student_mobile = student_mobile
        self.student_email = student_email
        self.student_p1 = student_p1
        self.student_p2 = student_p2
        self.student_p3 = student_p3
        self.student_p4 = student_p4
        self.student_p5 = student_p5
        self.student_p6 = student_p6
        self.student_english = student_english
        self.student_math = student_math
        self.student_science = student_science


class Tutor(db.Model):

    tutor_id_num = db.Column("id_num", db.String(7), primary_key=True)
    tutor_first_name = db.Column("first_name", db.String(80))
    tutor_last_name = db.Column("last_name", db.String(80))
    tutor_password = db.Column("password", db.String(127))
    tutor_age = db.Column("age", db.Integer)
    tutor_mobile = db.Column("mobile", db.Integer)
    tutor_email = db.Column("email", db.String(150))
    tutor_p1 = db.Column("p1", db.Boolean, default=False)
    tutor_p2 = db.Column("p2", db.Boolean, default=False)
    tutor_p3 = db.Column("p3", db.Boolean, default=False)
    tutor_p4 = db.Column("p4", db.Boolean, default=False)
    tutor_p5 = db.Column("p5", db.Boolean, default=False)
    tutor_p6 = db.Column("p6", db.Boolean, default=False)
    tutor_english = db.Column("english", db.Boolean)
    tutor_math = db.Column("math", db.Boolean)
    tutor_science = db.Column("science", db.Boolean)

    def __init__(self, tutor_id_num, tutor_first_name, tutor_last_name, tutor_password, tutor_age, tutor_mobile, tutor_email, tutor_p1, tutor_p2, tutor_p3, tutor_p4, tutor_p5, tutor_p6, tutor_english, tutor_math, tutor_science):
        self.tutor_id_num = tutor_id_num
        self.tutor_first_name = tutor_first_name
        self.tutor_last_name = tutor_last_name
        self.tutor_password = tutor_password
        self.tutor_age = tutor_age
        self.tutor_mobile = tutor_mobile
        self.tutor_email = tutor_email
        self.tutor_p1 = tutor_p1
        self.tutor_p2 = tutor_p2
        self.tutor_p3 = tutor_p3
        self.tutor_p4 = tutor_p4
        self.tutor_p5 = tutor_p5
        self.tutor_p6 = tutor_p6
        self.tutor_english = tutor_english
        self.tutor_math = tutor_math
        self.tutor_science = tutor_science


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

    admin_account = Admin.query.all()
    tutor_account = Tutor.query.all()
    for i in admin_account:
        admin_id = i.admin_id_num
        for j in tutor_account:
            tutor_id = j.tutor_id_num
            if admin_id == tutor_login_form.id_num.data:
                admin_info = Admin.query.filter_by(admin_id_num=tutor_login_form.id_num.data).first()
                admin_pass = admin_info.admin_password

                if admin_pass == tutor_login_form.password.data:
                    session['user'] = tutor_login_form.id_num.data

                    return redirect(url_for('admin_main'))

            elif tutor_id == tutor_login_form.id_num.data:
                tutor_info = Tutor.query.filter_by(id_num=tutor_login_form.id_num.data).first()
                tutor_pass = tutor_info.tutor_password

                if tutor_pass == tutor_login_form.password.data:
                    session['user'] = tutor_login_form.id_num.data

                    return redirect(url_for('retrieve_tutor_account'))

    return render_template('tutorlogin.html')


@app.route("/adminMain")
def admin_main():
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
            student_p1 = request.form.get('student_p1')
            if student_p1 == 'y':
                student_p1 = 1
            else:
                student_p1 = 0
            student_p2 = request.form.get('student_p2')
            if student_p2 == 'y':
                student_p2 = 1
            else:
                student_p2 = 0
            student_p3 = request.form.get('student_p3')
            if student_p3 == 'y':
                student_p3 = 1
            else:
                student_p3 = 0
            student_p4 = request.form.get('student_p4')
            if student_p4 == 'y':
                student_p4 = 1
            else:
                student_p4 = 0
            student_p5 = request.form.get('student_p5')
            if student_p5 == 'y':
                student_p5 = 1
            else:
                student_p5 = 0
            student_p6 = request.form.get('student_p6')
            if student_p6 == 'y':
                student_p6 = 1
            else:
                student_p6 = 0
            student_english = request.form.get('student_english')
            if student_english == 'y':
                student_english = 1
            else:
                student_english = 0
            student_math = request.form.get('student_math')
            if student_math == 'y':
                student_math = 1
            else:
                student_math = 0
            student_science = request.form.get('student_science')
            if student_science == 'y':
                student_science = 1
            else:
                student_science = 0
            student = Student(student_id_num, student_first_name, student_last_name, student_password, student_mobile, student_email, student_p1, student_p2, student_p3, student_p4, student_p5, student_p6, student_english, student_math, student_science)
            db.session.add(student)
            db.session.commit()

        return redirect(url_for('retrieve_student_account'))
    return render_template('createstudent.html', form=create_student_form)


@app.route('/retrievestudent')
def retrieve_student_account():
    update_student_account = CreateStudentAccount(request.form)
    with app.app_context():
        student_data = Student.query.all()

    return render_template('retrievestudent.html', count=len(student_data), student=student_data, form=update_student_account)


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
            student_data.student_p1 = request.form.get('student_p1')
            if student_data.student_p1 == 'y':
                student_data.student_p1 = 1
            else:
                student_data.student_p1 = 0
            student_data.student_p2 = request.form.get('student_p2')
            if student_data.student_p2 == 'y':
                student_data.student_p2 = 1
            else:
                student_data.student_p2 = 0
            student_data.student_p3 = request.form.get('student_p3')
            if student_data.student_p3 == 'y':
                student_data.student_p3 = 1
            else:
                student_data.student_p3 = 0
            student_data.student_p4 = request.form.get('student_p4')
            if student_data.student_p4 == 'y':
                student_data.student_p4 = 1
            else:
                student_data.student_p4 = 0
            student_data.student_p5 = request.form.get('student_p5')
            if student_data.student_p5 == 'y':
                student_data.student_p5 = 1
            else:
                student_data.student_p5 = 0
            student_data.student_p6 = request.form.get('student_p6')
            if student_data.student_p6 == 'y':
                student_data.student_p6 = 1
            else:
                student_data.student_p6 = 0
            student_data.student_english = request.form.get('student_english')
            if student_data.student_english == 'y':
                student_data.student_english = 1
            else:
                student_data.student_english = 0
            student_data.student_math = request.form.get('student_math')
            if student_data.student_math == 'y':
                student_data.student_math = 1
            else:
                student_data.student_math = 0
            student_data.student_science = request.form.get('student_science')
            if student_data.student_science == 'y':
                student_data.student_science = 1
            else:
                student_data.student_science = 0

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
    if g.user:
        id_num = session['user']
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
                tutor_p1 = request.form.get('tutor_p1')
                if tutor_p1 == 'y':
                    tutor_p1 = 1
                else:
                    tutor_p1 = 0
                tutor_p2 = request.form.get('tutor_p2')
                if tutor_p2 == 'y':
                    tutor_p2 = 1
                else:
                    tutor_p2 = 0
                tutor_p3 = request.form.get('tutor_p3')
                if tutor_p3 == 'y':
                    tutor_p3 = 1
                else:
                    tutor_p3 = 0
                tutor_p4 = request.form.get('tutor_p4')
                if tutor_p4 == 'y':
                    tutor_p4 = 1
                else:
                    tutor_p4 = 0
                tutor_p5 = request.form.get('tutor_p5')
                if tutor_p5 == 'y':
                    tutor_p5 = 1
                else:
                    tutor_p5 = 0
                tutor_p6 = request.form.get('tutor_p6')
                if tutor_p6 == 'y':
                    tutor_p6 = 1
                else:
                    tutor_p6 = 0
                tutor_english = request.form.get('tutor_english')
                if tutor_english == 'y':
                    tutor_english = 1
                else:
                    tutor_english = 0
                tutor_math = request.form.get('tutor_math')
                if tutor_math == 'y':
                    tutor_math = 1
                else:
                    tutor_math = 0
                tutor_science = request.form.get('tutor_science')
                if tutor_science == 'y':
                    tutor_science = 1
                else:
                    tutor_science = 0
                tutor = Tutor(tutor_id_num, tutor_first_name, tutor_last_name, tutor_password, tutor_age, tutor_mobile, tutor_email, tutor_p1, tutor_p2, tutor_p3, tutor_p4, tutor_p5, tutor_p6, tutor_english, tutor_math, tutor_science)
                db.session.add(tutor)
                db.session.commit()

            return redirect(url_for('retrieve_tutor_account'))
        return render_template('createtutor.html', form=create_tutor_form)
    return redirect(url_for('tutor_login'))


@app.route('/retrievetutor')
def retrieve_tutor_account():
    if g.user:
        id_num = session['user']
        update_tutor_form = CreateTutorAccount(request.form)
        with app.app_context():
            tutor_data = Tutor.query.all()

        return render_template('retrievetutor.html', count=len(tutor_data), tutor=tutor_data, form=update_tutor_form)
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
            tutor_data.tutor_p1 = request.form.get('tutor_p1')
            if tutor_data.tutor_p1 == 'y':
                tutor_data.tutor_p1 = 1
            else:
                tutor_data.tutor_p1 = 0
            tutor_data.tutor_p2 = request.form.get('tutor_p2')
            if tutor_data.tutor_p2 == 'y':
                tutor_data.tutor_p2 = 1
            else:
                tutor_data.tutor_p2 = 0
            tutor_data.tutor_p3 = request.form.get('tutor_p3')
            if tutor_data.tutor_p3 == 'y':
                tutor_data.tutor_p3 = 1
            else:
                tutor_data.tutor_p3 = 0
            tutor_data.tutor_p4 = request.form.get('tutor_p4')
            if tutor_data.tutor_p4 == 'y':
                tutor_data.tutor_p4 = 1
            else:
                tutor_data.tutor_p4 = 0
            tutor_data.tutor_p5 = request.form.get('tutor_p5')
            if tutor_data.tutor_p5 == 'y':
                tutor_data.tutor_p5 = 1
            else:
                tutor_data.tutor_p5 = 0
            tutor_data.tutor_p6 = request.form.get('tutor_p6')
            if tutor_data.tutor_p6 == 'y':
                tutor_data.tutor_p6 = 1
            else:
                tutor_data.tutor_p6 = 0
            tutor_data.tutor_english = request.form.get('tutor_english')
            if tutor_data.tutor_english == 'y':
                tutor_data.tutor_english = 1
            else:
                tutor_data.tutor_english = 0
            tutor_data.tutor_math = request.form.get('tutor_math')
            if tutor_data.tutor_math == 'y':
                tutor_data.tutor_math = 1
            else:
                tutor_data.tutor_math = 0
            tutor_data.tutor_science = request.form.get('tutor_science')
            if tutor_data.tutor_science == 'y':
                tutor_data.tutor_science = 1
            else:
                tutor_data.tutor_science = 0

            db.session.commit()
            return redirect(url_for('retrieve_tutor_account'))

    else:
        with app.app_context():
            tutor_data = Tutor.query.get(request.form.get('tutor_id_num'))

            update_tutor_form.tutor_id_num.data = tutor_data.tutor_id_num

    return render_template('updatetutor.html', form=update_tutor_form)


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
