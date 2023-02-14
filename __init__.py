from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_file, session, g, jsonify, flash, \
    send_from_directory
from Forms import CreateStudentAccount, LoginAccount, CreateTutorAccount, CreateNotifications, CreateTodo, \
    CreateFeedback, CreateTestQuestion, StudentTestQuestion, CreateAnnouncementForm, CreateStudentContent
import shelve, Notification, Todo, Feedback, STEST, Test, announce, os, pickle, imghdr
from Content import Content
from Feedback import Feedback
from announce import Announcement
from Notification import Notification
from Todo import Todo
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session
from chat import get_response
import uuid as uuid

# ----------------- EZEKKIOUS --------------------
UPLOAD_FOLDER = 'static/announcements'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'zip', 'docx', 'xlxs', 'xls'}
UPLOAD_FOLDER_ANDI = 'static/feedback'
ALLOWED_EXTENSIONS2 = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER_CONTENT = 'static/content'
ALLOWED_EXTENSIONS_CONTENT = {'pdf', 'docx'}

# ----------------- WEE JUN CAI, BRANDON, ADMIN START----------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eztutors.db'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
app.config['SQLALCHEMY_SILENCE_UBER_WARNING'] = True
app.secret_key = os.urandom(24)  # generate a random secret key
db = SQLAlchemy(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # EZEKKIOUS
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS  # EZEKKIOUS
app.config['UPLOAD_FOLDER_ANDI'] = UPLOAD_FOLDER_ANDI  # EZEKKIOUS
app.config['UPLOAD_FOLDER_CONTENT'] = UPLOAD_FOLDER_CONTENT  # EZEKKIOUS
app.config['ALLOWED_EXTENSIONS_CONTENT'] = ALLOWED_EXTENSIONS_CONTENT  # EZEKKOUS
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024  # EZEKKIOUS
app.config['SECRET_KEY'] = 'secret'  # EZEKKIOUS
app.config['SESSION_TYPE'] = 'filesystem'  # EZEKKIOUS
socketio = SocketIO(app)  # EZEKKIOUS
Session(app)  # EZEKKIOUS
with app.app_context():
    inspector = inspect(db.engine)


class Student(db.Model):
    student_id_num = db.Column("id_num", db.String(7), primary_key=True)
    student_first_name = db.Column("first_name", db.String(80))
    student_last_name = db.Column("last_name", db.String(80))
    student_password = db.Column("password", db.String(127))
    student_mobile = db.Column("mobile", db.String(8))
    student_email = db.Column("email", db.String(150))
    student_education_level = db.Column("education level", db.String)
    student_class = db.Column("student class(es)", db.String)
    student_img = db.Column("student profile picture", db.String)

    def __init__(self, student_id_num, student_first_name, student_last_name, student_password, student_mobile,
                 student_email, student_education_level, student_class, student_img):
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
    tutor_img = db.Column("tutor profile picture", db.String)

    def __init__(self, tutor_id_num, tutor_first_name, tutor_last_name, tutor_password, tutor_age, tutor_mobile,
                 tutor_email, tutor_teaching_level, tutor_class, tutor_img):
        self.tutor_id_num = tutor_id_num
        self.tutor_first_name = tutor_first_name
        self.tutor_last_name = tutor_last_name
        self.tutor_password = tutor_password
        self.tutor_age = tutor_age
        self.tutor_mobile = tutor_mobile
        self.tutor_email = tutor_email
        self.tutor_teaching_level = tutor_teaching_level
        self.tutor_class = tutor_class
        self.tutor_img = tutor_img


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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_file2(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS2


def allowed_file3(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_CONTENT


@app.route('/static/announcements/<path:name>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name, as_attachment=True)


@app.route('/static/feedback/<path:name>')
def download_file2(name):
    return send_from_directory(app.config['UPLOAD_FOLDER_ANDI'], name, as_attachment=True)


@app.route('/static/content/<path:name>')
def download_file3(name):
    return send_from_directory(app.config['UPLOAD_FOLDER_CONTENT'], name, as_attachment=True)


def save_image(img_file):
    image_name = str(uuid.uuid1()) + "_" + secure_filename(img_file.filename)
    image_path = os.path.join(app.root_path, 'static/profile_pics', image_name)
    img_file.save(image_path)
    return image_name


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')


@app.before_request
def before_request():
    g.user = None

    if 'user' in session:
        g.user = session['user']


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/removeprofile/<string:id_num>/', methods=['POST'])
def a_remove_profile_pic(id_num):
    if id_num[0] == 'T':
        tutor_data = Tutor.query.filter_by(tutor_id_num=id_num).first()

        tutor_img = tutor_data.tutor_img
        if tutor_img != 'defaultprofile.jpg':
            os.remove(os.path.join(app.root_path, 'static/profile_pics', tutor_img))
            tutor_data.tutor_img = "defaultprofile.jpg"
            db.session.commit()
            return redirect(url_for('a_accounts'))
    elif id_num[0] == 'S':
        student_data = Student.query.filter_by(student_id_num=id_num).first()

        student_img = student_data.student_img
        if student_img != 'defaultprofile.jpg':
            os.remove(os.path.join(app.root_path, 'static/profile_pics', student_img))
            student_data.student_img = "defaultprofile.jpg"
            db.session.commit()
            return redirect(url_for('a_accounts'))
    return render_template('adminAccounts.html')


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

                return redirect(url_for('retrieve_content'))

            else:
                flash('INVALID STUDENT CREDENTIALS', 'student')

    return render_template('studentlogin.html')


@app.route('/tutorlogin', methods=['POST', 'GET'])
def tutor_login():
    tutor_login_form = LoginAccount(request.form)
    if request.method == 'POST' and tutor_login_form.validate():
        session.pop('user', None)

    if not inspector.has_table("tutor"):
        admin_account = Admin.query.all()
        for i in admin_account:
            admin_id = i.admin_id_num
            if admin_id == tutor_login_form.id_num.data:
                admin_info = Admin.query.filter_by(admin_id_num=tutor_login_form.id_num.data).first()
                admin_pass = admin_info.admin_password

                if admin_pass == tutor_login_form.password.data:
                    session['user'] = tutor_login_form.id_num.data

                    return redirect(url_for('tutor_retrieve_content'))

                else:
                        flash('INVALID TUTOR CREDENTIALS', 'tutor')
    else:
        admin_account = Admin.query.all()
        tutor_account = Tutor.query.all()
        for j in tutor_account:
            tutor_id = j.tutor_id_num
            for i in admin_account:
                admin_id = i.admin_id_num
                if tutor_id == tutor_login_form.id_num.data:
                    tutor_info = Tutor.query.filter_by(tutor_id_num=tutor_login_form.id_num.data).first()
                    tutor_pass = tutor_info.tutor_password

                    if tutor_pass == tutor_login_form.password.data:
                        session['user'] = tutor_login_form.id_num.data

                        return redirect(url_for('tutor_retrieve_content'))
                if admin_id == tutor_login_form.id_num.data:
                    admin_info = Admin.query.filter_by(admin_id_num=tutor_login_form.id_num.data).first()
                    admin_pass = admin_info.admin_password

                    if admin_pass == tutor_login_form.password.data:
                        session['user'] = tutor_login_form.id_num.data

                        return redirect(url_for('admin_main'))

                    else:
                        flash('INVALID ADMIN CREDENTIALS', 'admin')
    return render_template('tutorlogin.html')


@app.route("/adminMain", methods=['GET', 'POST'])
def admin_main():
    if g.user[0] == 'A':
        id_num = session['user']
        # -------- Feedback Display ---------
        feedback_dict = {}
        feedback_list = []
        try:
            dbf = shelve.open('Feedback.db', 'r')
            feedback_dict = dbf['Feedback']
            dbf.close()

            feedback_list = []
            for key in feedback_dict:
                feedback = feedback_dict.get(key)
                feedback_list.append(feedback)
        except:
            pass

        # --------- To-Do Create ----------
        create_todo_form = CreateTodo(request.form)
        if request.method == 'POST' and create_todo_form.validate():
            todo_dict = {}
            db = shelve.open('todo.db', 'c')

            try:
                todo_dict = db['Todo']
                Todo.count_id = db['Todo_id']
            except:
                print("Error in retrieving To Do list from Database")

            date = datetime.now()
            date = date.strftime("%A, %d %B %Y %I:%M%p")
            todo = Todo(create_todo_form.text.data, date)
            todo_dict[todo.get_todo_id()] = todo
            db['Todo'] = todo_dict
            db['Todo_id'] = Todo.count_id

            db.close()

            return redirect(url_for('admin_main'))

        # --------- To-Do Display ----------
        todod_dict = {}
        todo_list = []
        try:
            dbtr = shelve.open('todo.db', 'r')
            todod_dict = dbtr['Todo']
            dbtr.close()

            for key in todod_dict:
                todo = todod_dict.get(key)
                todo_list.append(todo)

        except:
            pass

        # --------- Display Announcements ----------
        ann_dict = {}
        ann_list = []
        user_dict = {}
        file_dict = {}
        lol = ""
        iname = ""
        try:
            db = shelve.open('announcement.db', 'r')
            ann_dict = db['announce']
            db.close()

            for key in ann_dict:
                announcement = ann_dict.get(key)
                ann_list.append(announcement)

            for i in ann_list:
                user_id = i.get_id_num()
                if user_id[0] == "T":
                    tutor_account = Tutor.query.filter_by(tutor_id_num=user_id).first()
                    tutor_first_name = tutor_account.tutor_first_name
                    tutor_last_name = tutor_account.tutor_last_name
                    name = tutor_first_name + " " + tutor_last_name + "  (Tutor)"
                    user_dict[user_id] = name
                else:
                    user_dict[user_id] = 'Jabe Ez (Administrator)'

            for j in ann_list:
                lol = j.get_ann_id()
                iname = j.get_files()
                file_dict[lol] = iname

        except:
            pass

        # --------- Update Announcement ---------
        edit_announcement_form = CreateAnnouncementForm(request.form)

        return render_template('adminMain.html', feedback=feedback_list, feedback_num=len(feedback_list),
                               todo_createform=create_todo_form, todo=todo_list, todo_num=len(todo_list),
                               announce=ann_list, announce_num=len(ann_list), user_dict=user_dict,
                               announce_updateform=edit_announcement_form, file_dict=file_dict)
    return redirect(url_for('tutor_login'))


@app.route('/adeleteFeedback/<int:feedback_id>', methods=['POST'])
def a_delete_feedback(feedback_id):
    feedback_dict = {}
    db = shelve.open('Feedback.db', 'w')
    feedback_dict = db['Feedback']
    feedback_dict.pop(feedback_id)
    db['Feedback'] = feedback_dict
    db.close()
    return redirect(url_for('admin_main'))


@app.route('/deleteAnnouncements/<int:ann_id>', methods=['POST'])
def a_delete_announcement(ann_id):
    ann_dict = {}
    db = shelve.open('announcement.db', 'w')
    ann_dict = db['announce']
    ann_dict.pop(ann_id)
    db['announce'] = ann_dict
    db.close()
    return redirect(url_for('admin_main'))


@app.route('/adminAnnouncement', methods=['GET', 'POST'])
def a_announcement():
    if g.user[0] == 'A':
        id_num = session['user']
        ann_dict = {}
        Tann_list = []
        Aann_list = []
        user_dict = {}
        ann_list = []
        file_dict = {}
        file_name = []
        try:
            db = shelve.open('announcement.db', 'r')
            ann_dict = db['announce']
            db.close()

            for key in ann_dict:
                announcement = ann_dict.get(key)
                ann_list.append(announcement)

            for j in ann_list:
                lol = j.get_ann_id()
                iname = j.get_files()
                file_dict[lol] = iname

            for i in ann_list:
                user_id = i.get_id_num()
                if user_id[0] == "T":
                    tutor_account = Tutor.query.filter_by(tutor_id_num=user_id).first()
                    tutor_first_name = tutor_account.tutor_first_name
                    tutor_last_name = tutor_account.tutor_last_name
                    name = tutor_first_name + " " + tutor_last_name + "  (Tutor)"
                    user_dict[user_id] = name
                    Tann_list.append(i)
                else:
                    user_dict[user_id] = 'Jabe Ez (Administrator)'
                    Aann_list.append(i)

        except:
            pass

        create_announcement_form = CreateAnnouncementForm(request.form)
        if request.method == 'POST' and create_announcement_form.validate():
            ann_dict = {}
            db = shelve.open('announcement.db', 'c')

            try:
                ann_dict = db['announce']
                Announcement.count_id = db['announce_id']
            except:
                db['announce'] = ann_dict
            date1 = datetime.now()
            adate = date1.strftime("%A, %d %B %Y %I:%M%p")
            update = None

            if 'afiles' not in request.files:
                return redirect(request.url)

            afile = request.files['afiles']

            if afile.filename == '':
                filename = ''
                afile = filename

            if afile and allowed_file(afile.filename):
                filename = str(uuid.uuid1()) + "" + secure_filename(afile.filename)
                afile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                afile = filename

            announcement = announce.Announcement(id_num, adate, create_announcement_form.atitle.data,
                                                 create_announcement_form.acontent.data, afile, update)
            ann_dict[announcement.get_ann_id()] = announcement
            db['announce'] = ann_dict
            db['announce_id'] = Announcement.count_id
            db.close()

            return redirect(url_for('a_announcement'))
        return render_template('adminAnnouncements.html', form=create_announcement_form, tutor_ann_list=Tann_list,
                               admin_ann_list=Aann_list, count_tutor=len(Tann_list), count_admin=len(Aann_list),
                               user_dict=user_dict, file_dict=file_dict)
    return redirect(url_for('tutor_login'))


@app.route('/updateAdminAnnouncement/<int:ann_id>/', methods=['GET', 'POST'])
def a_edit_announcement(ann_id):
    if g.user[0] == 'A':
        id_num = session['user']
        ann_dict = {}
        Tann_list = []
        Aann_list = []
        user_dict = {}
        ann_list = []
        file_dict = {}
        file_name = []
        try:
            db = shelve.open('announcement.db', 'r')
            ann_dict = db['announce']
            db.close()

            for key in ann_dict:
                announcement = ann_dict.get(key)
                ann_list.append(announcement)

            for j in ann_list:
                lol = j.get_ann_id()
                iname = j.get_files()
                file_dict[lol] = iname

            for i in ann_list:
                user_id = i.get_id_num()
                if user_id[0] == "T":
                    tutor_account = Tutor.query.filter_by(tutor_id_num=user_id).first()
                    tutor_first_name = tutor_account.tutor_first_name
                    tutor_last_name = tutor_account.tutor_last_name
                    name = tutor_first_name + " " + tutor_last_name + "  (Tutor)"
                    user_dict[user_id] = name
                    Tann_list.append(i)
                else:
                    user_dict[user_id] = 'Jabe Ez (Administrator)'
                    Aann_list.append(i)

        except:
            pass

        edit_announcement_form = CreateAnnouncementForm(request.form)
        if request.method == 'POST' and edit_announcement_form.validate():
            ann_dict = {}
            db = shelve.open('announcement.db', 'w')
            ann_dict = db['announce']
            announcement = ann_dict.get(ann_id)
            announcement.set_title(edit_announcement_form.atitle.data)
            announcement.set_content(edit_announcement_form.acontent.data)
            date = datetime.now()
            date = date.strftime("%A, %d %B %Y %I:%M%p")
            announcement.set_update(date)

            if 'afiles' not in request.files:
                return redirect(request.url)

            afile = request.files['afiles']

            if afile.filename == '':
                filename = announcement.get_files()
                afile = filename
            elif afile and allowed_file(afile.filename):
                filename = str(uuid.uuid1()) + "" + secure_filename(afile.filename)
                afile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                afile = filename

            announcement.set_files(afile)
            db['announce'] = ann_dict
            db.close()
            return redirect(url_for('a_announcement'))
        else:
            ann_dict = {}
            db = shelve.open('announcement.db', 'r')
            ann_dict = db['announce']
            db.close()

            announcement = ann_dict.get(ann_id)
            edit_announcement_form.atitle.data = announcement.get_title()
            edit_announcement_form.acontent.data = announcement.get_content()
        return render_template('adminUpdateAnnouncement.html', form=edit_announcement_form, tutor_ann_list=Tann_list,
                               admin_ann_list=Aann_list, count_tutor=len(Tann_list), count_admin=len(Aann_list),
                               user_dict=user_dict, file_dict=file_dict)
    return redirect(url_for('tutor_login'))


@app.route('/deletestudent/<string:student_id_num>', methods=['POST'])
def delete_student_account(student_id_num):
    student_data = Student.query.get(student_id_num)

    student_img = student_data.student_img
    if student_img != 'defaultprofile.jpg':
        os.remove(os.path.join(app.root_path, 'static/profile_pics', student_img))

    db.session.delete(student_data)
    db.session.commit()

    return redirect(url_for('a_accounts'))


@app.route('/deletetutor/<string:tutor_id_num>', methods=['POST'])
def delete_tutor_account(tutor_id_num):
    tutor_data = Tutor.query.get(tutor_id_num)

    tutor_img = tutor_data.tutor_img
    if tutor_img != 'defaultprofile.jpg':
        os.remove(os.path.join(app.root_path, 'static/profile_pics', tutor_img))

    db.session.delete(tutor_data)
    db.session.commit()

    return redirect(url_for('a_accounts'))


@app.route('/adminAccounts', methods=['GET', 'POST'])
def a_accounts():
    if g.user[0] == 'A':
        id_num = session['user']
        with app.app_context():
            student_data = Student.query.all()
            tutor_data = Tutor.query.all()

            student_name = ""
            student_name_dict = {}

            for i in student_data:
                student_id_num = i.student_id_num
                student_name = i.student_first_name + " " + i.student_last_name
                student_name_dict[student_id_num] = student_name

            tutor_name = ""
            tutor_name_dict = {}

            for j in tutor_data:
                tutor_id_num = j.tutor_id_num
                tutor_name = j.tutor_first_name + " " + j.tutor_last_name
                tutor_name_dict[tutor_id_num] = tutor_name

        return render_template('adminAccounts.html', student_count=len(student_data), student_data=student_data,
                               student_name_dict=student_name_dict, tutor_count=len(tutor_data), tutor_data=tutor_data,
                               tutor_name_dict=tutor_name_dict)
    return redirect(url_for('student_login'))


@app.route('/adminCreate/student', methods=['POST', 'GET'])
def a_create_saccount():
    if g.user[0] == 'A':
        id_num = session['user']

        create_student_form = CreateStudentAccount(request.form)
        with app.app_context():
            student_data = Student.query.all()

            student_name = ""
            student_name_dict = {}

            for i in student_data:
                student_id_num = i.student_id_num
                student_name = i.student_first_name + " " + i.student_last_name
                student_name_dict[student_id_num] = student_name

        student_id_list = []
        student_id_num = ''
        for i in student_data:
            student_id_list.append(i.student_id_num)

        if request.method == 'POST' and create_student_form.validate():
            with app.app_context():
                db.create_all()
                if request.form['student_id_num'] in student_id_list:
                    flash('Student ID already exists. Please enter a new Student ID.', 'unique')
                    return redirect(url_for('a_create_saccount'))

                student_id_num = request.form['student_id_num']
                student_first_name = request.form['student_first_name']
                student_last_name = request.form['student_last_name']
                student_password = request.form['student_password']
                student_mobile = request.form['student_mobile']
                student_email = request.form['student_email']
                student_education_level = request.form['student_education_level']
                student_class = pickle.dumps(create_student_form.student_class.data)

                student_img = request.files['file3']
                if student_img.filename == "":
                    filename = "defaultprofile.jpg"
                    student_img = filename

                elif student_img and allowed_file2(student_img.filename):
                    filename = str(uuid.uuid1()) + "_" + secure_filename(student_img.filename)
                    student_img.save(os.path.join(app.config['UPLOAD_FOLDER_BRANDON'], filename))
                    student_img = filename

                else:
                    filename = secure_filename(student_img.filename)
                    file_ext = allowed_file(filename)
                    if file_ext not in app.config['ALLOWED_EXTENSIONS2'] or file_ext != validate_image(student_img.stream):
                        flash('Invalid File Type.', 'creates')
                        return redirect(url_for('a_create_saccount'))

                student = Student(student_id_num, student_first_name, student_last_name, student_password, student_mobile,
                                  student_email, student_education_level, student_class, student_img)
                db.session.add(student)
                db.session.commit()

            return redirect(url_for('a_create_saccount'))
        return render_template('adminCreateSAccount.html', form=create_student_form, student_count=len(student_data),
                               student_data=student_data, student_name_dict=student_name_dict)
    return redirect(url_for('tutor_login'))


@app.route('/adminCreate/tutor', methods=['GET', 'POST'])
def a_create_taccount():
    if g.user[0] == 'A':
        id_num = session['user']
        create_tutor_form = CreateTutorAccount(request.form)
        with app.app_context():
            tutor_data = Tutor.query.all()

            tutor_name = ""
            tutor_name_dict = {}

            for j in tutor_data:
                tutor_id_num = j.tutor_id_num
                tutor_name = j.tutor_first_name + " " + j.tutor_last_name
                tutor_name_dict[tutor_id_num] = tutor_name

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

                img = request.files['tutor_img']
                if img.filename == "":
                    tutor_img = "defaultprofile.jpg"
                else:
                    tutor_img = save_image(img)

                tutor = Tutor(tutor_id_num, tutor_first_name, tutor_last_name, tutor_password, tutor_age, tutor_mobile,
                              tutor_email, tutor_teaching_level, tutor_class, tutor_img)
                db.session.add(tutor)
                db.session.commit()

                return redirect(url_for('a_create_taccount'))
        return render_template('adminCreateTAccount.html', form=create_tutor_form, tutor_count=len(tutor_data),
                               tutor_data=tutor_data, tutor_name_dict=tutor_name_dict)
    return redirect(url_for('tutor_login'))


@app.route('/adminUpdateAccounts/students/<string:id_num>/', methods=['POST', 'GET'])
def a_update_saccount(id_num):
    if g.user[0] == 'A':
        id_num = session['user']
        student_class_dict = {}
        update_student_form = CreateStudentAccount(request.form)
        with app.app_context():
            student_current_data = Student.query.filter_by(student_id_num=id_num).first()
            name = student_current_data.student_first_name + " " + student_current_data.student_last_name

            student_class_list = student_current_data.student_class
            student_id_num = student_current_data.student_id_num
            student_class_list = pickle.loads(student_class_list)
            student_class = ', '.join(student_class_list)
            student_class_dict[student_id_num] = student_class

            if request.method == 'POST' and update_student_form.validate():

                with app.app_context():
                    student_data = Student.query.filter_by(student_id_num=id_num).first()

                    student_data.student_id_num = request.form['student_id_num']
                    student_data.student_first_name = request.form['student_first_name']
                    student_data.student_last_name = request.form['student_last_name']
                    student_data.student_password = request.form['student_password']
                    student_data.student_mobile = request.form['student_mobile']
                    student_data.student_email = request.form['student_email']
                    student_data.student_education_level = request.form['student_education_level']
                    student_data.student_class = pickle.dumps(update_student_form.student_class.data)

                    img = request.files['student_img']
                    if img.filename != "":
                        student_img = save_image(img)

                    student_data.student_img = student_img
                    db.session.commit()
                    return redirect(url_for('a_accounts'))

        return render_template('adminUpdateSAccounts.html', form=update_student_form, name=name,
                               student_data=student_current_data, student_class_dict=student_class_dict)
    return redirect(url_for('tutor_login'))


@app.route('/adminUpdateAccounts/tutors/<string:id_num>/', methods=['POST', 'GET'])
def a_update_taccount(id_num):
    if g.user[0] == 'A':
        tutor_class_dict = {}
        tutor_level_dict = {}
        tutor_img = ""
        update_tutor_form = CreateTutorAccount(request.form)
        with app.app_context():
            tutor_current_data = Tutor.query.filter_by(tutor_id_num=id_num).first()
            name = tutor_current_data.tutor_first_name + " " + tutor_current_data.tutor_last_name

            tutor_class_list = tutor_current_data.tutor_class
            tutor_id_num = tutor_current_data.tutor_id_num
            tutor_class_list = pickle.loads(tutor_class_list)
            tutor_class = ', '.join(tutor_class_list)
            tutor_class_dict[tutor_id_num] = tutor_class

            tutor_teaching_level = tutor_current_data.tutor_teaching_level
            tutor_id_num = tutor_current_data.tutor_id_num
            tutor_teaching_level = pickle.loads(tutor_teaching_level)
            tutor_teach = ', '.join(tutor_teaching_level)
            tutor_level_dict[tutor_id_num] = tutor_teach

            if request.method == 'POST' and update_tutor_form.validate():

                with app.app_context():
                    tutor_data = Tutor.query.filter_by(tutor_id_num=id_num).first()

                    tutor_data.tutor_id_num = request.form['tutor_id_num']
                    tutor_data.tutor_first_name = request.form['tutor_first_name']
                    tutor_data.tutor_last_name = request.form['tutor_last_name']
                    tutor_data.tutor_password = request.form['tutor_password']
                    tutor_data.tutor_age = request.form['tutor_age']
                    tutor_data.tutor_mobile = request.form['tutor_mobile']
                    tutor_data.tutor_email = request.form['tutor_email']
                    tutor_data.tutor_teaching_level = pickle.dumps(update_tutor_form.tutor_teaching_level.data)
                    tutor_data.tutor_class = pickle.dumps(update_tutor_form.tutor_class.data)

                    img = request.files['tutor_img']
                    if img.filename != "":
                        tutor_img = save_image(img)
                    else:
                        tutor_img = tutor_data.tutor_img

                    tutor_data.tutor_img = tutor_img
                    db.session.commit()
                    return redirect(url_for('a_accounts'))
        return render_template('adminUpdateTAccounts.html', form=update_tutor_form, name=name,
                               tutor_data=tutor_current_data, tutor_class_dict=tutor_class_dict,
                               tutor_level_dict=tutor_level_dict)
    return redirect(url_for('tutor_login'))


@app.route('/adminAccountsAll', methods=['GET', 'POST'])
def a_all_accounts():
    if g.user[0] == 'A':
        with app.app_context():
            student_data = Student.query.all()

            student_class = ""
            student_class_list = []
            student_class_dict = {}

            for i in student_data:
                student_class_list = i.student_class
                student_id_num = i.student_id_num
                student_class_list = pickle.loads(student_class_list)
                student_class = ', '.join(student_class_list)
                student_class_dict[student_id_num] = student_class

            tutor_data = Tutor.query.all()

            tutor_class = ""
            tutor_class_list = []
            tutor_class_dict = {}

            tutor_level = ""
            tutor_level_list = []
            tutor_level_dict = {}

            for j in tutor_data:
                tutor_class_list = j.tutor_class
                tutor_id_num = j.tutor_id_num
                tutor_class_list = pickle.loads(tutor_class_list)
                tutor_class = ', '.join(tutor_class_list)
                tutor_class_dict[tutor_id_num] = tutor_class

                tutor_level_list = j.tutor_teaching_level
                tutor_level_list = pickle.loads(tutor_level_list)
                tutor_level = ', '.join(tutor_level_list)
                tutor_level_dict[tutor_id_num] = tutor_level

        return render_template('adminAccountsAll.html', count_student=len(student_data), student_data=student_data,
                               student_class_dict=student_class_dict, count_tutor=len(tutor_data), tutor_data=tutor_data,
                               tutor_class_dict=tutor_class_dict, tutor_level_dict=tutor_level_dict)
    return redirect(url_for('tutor_login'))


@app.route('/deleteNotification/<int:notif_id>', methods=['POST'])
def a_delete_notification(notif_id):
    notification_dict = {}
    db = shelve.open('notification.db', 'w')
    notification_dict = db['Notification']

    notification_dict.pop(notif_id)

    db['Notification'] = notification_dict
    db.close()

    return redirect(url_for('a_notification'))


@app.route('/adminNotifications', methods=['GET', 'POST'])
def a_notification():
    if g.user[0] == 'A':
        id_num = session['user']
        create_notification_form = CreateNotifications(request.form)

        with app.app_context():
            student_data = Student.query.all()
            tutor_data = Tutor.query.all()

            student_name = ""
            student_name_dict = {}

            for i in student_data:
                student_id_num = i.student_id_num
                student_name = i.student_first_name + " " + i.student_last_name
                student_name_dict[student_id_num] = student_name

            tutor_name = ""
            tutor_name_dict = {}

            for j in tutor_data:
                tutor_id_num = j.tutor_id_num
                tutor_name = j.tutor_first_name + " " + j.tutor_last_name
                tutor_name_dict[tutor_id_num] = tutor_name

        if request.method == 'POST' and create_notification_form.validate():
            notification_dict = {}
            db = shelve.open('notification.db', 'c')

            try:
                notification_dict = db['Notification']
                Notification.count_id = db["Notification_id"]
            except:
                print("Error in retrieving Notifications from Database")

            sender = id_num
            date = datetime.now()
            date = date.strftime("%A, %d %B %Y %I:%M%p")
            notification = Notification(date, create_notification_form.title.data,
                                        create_notification_form.description.data,
                                        create_notification_form.target_user.data, sender)
            notification_dict[notification.get_notif_id()] = notification
            db['Notification'] = notification_dict
            db['Notification_id'] = Notification.count_id
            db.close()

            return redirect(url_for('a_notification'))

        notif_data = []
        notif_display_dict = {}
        notif_user_dict = {}
        student_name = ""
        tutor_name = ""
        try:
            dbr = shelve.open('notification.db', 'r')
            notif_display_dict = dbr['Notification']
            dbr.close()

            for i in notif_display_dict:
                notif = notif_display_dict.get(i)
                notif_data.append(notif)

            for j in notif_data:
                if j.get_target_user()[0] == 'S':
                    student_data2 = Student.query.filter_by(student_id_num=j.get_target_user()).first()
                    student_name = student_data2.student_first_name + " " + student_data2.student_last_name
                    notif_user_dict[j.get_target_user()] = student_name
                elif j.get_target_user()[0] == 'T':
                    tutor_data2 = Tutor.query.filter_by(tutor_id_num=j.get_target_user()).first()
                    tutor_name = tutor_data2.tutor_first_name + " " + tutor_data2.tutor_last_name
                    notif_user_dict[j.get_target_user()] = tutor_name
        except:
            pass

        return render_template('adminNotifications.html', count=len(notif_data), form=create_notification_form,
                               student_data=student_data, student_name_dict=student_name_dict, tutor_data=tutor_data,
                               tutor_name_dict=tutor_name_dict, notif_list=notif_data, notif_user_dict=notif_user_dict)
    return redirect(url_for('tutor_login'))


@app.route('/adminUpdateNotifications/<int:notif_id>', methods=['GET', 'POST'])
def a_edit_notification(notif_id):
    if g.user[0] == 'A':
        id_num = session['user']
        update_notification_form = CreateNotifications(request.form)

        with app.app_context():
            student_data = Student.query.all()
            tutor_data = Tutor.query.all()

            student_name = ""
            student_name_dict = {}

            for i in student_data:
                student_id_num = i.student_id_num
                student_name = i.student_first_name + " " + i.student_last_name
                student_name_dict[student_id_num] = student_name

            tutor_name = ""
            tutor_name_dict = {}

            for j in tutor_data:
                tutor_id_num = j.tutor_id_num
                tutor_name = j.tutor_first_name + " " + j.tutor_last_name
                tutor_name_dict[tutor_id_num] = tutor_name

        if request.method == 'POST' and update_notification_form.validate():
            notification_dict = {}
            db = shelve.open('notification.db', 'w')
            notification_dict = db['Notification']
            notif = notification_dict.get(notif_id)
            notif.set_target_user(update_notification_form.target_user.data)
            notif.set_title(update_notification_form.title.data)
            notif.set_description(update_notification_form.description.data)

            db['Notification'] = notification_dict
            db.close()

            return redirect(url_for('a_notification'))
        else:
            notification_dict = {}
            db = shelve.open('notification.db', 'r')
            notification_dict = db['Notification']
            db.close()

            notif = notification_dict.get(notif_id)
            update_notification_form.target_user.data = notif.get_target_user()
            update_notification_form.title.data = notif.get_title()
            update_notification_form.description.data = notif.get_description()

        notif_data = []
        notif_display_dict = {}
        notif_user_dict = {}
        student_name = ""
        tutor_name = ""
        try:
            dbr = shelve.open('notification.db', 'r')
            notif_display_dict = dbr['Notification']
            dbr.close()

            for i in notif_display_dict:
                notif = notif_display_dict.get(i)
                notif_data.append(notif)

            for j in notif_data:
                if j.get_target_user()[0] == 'S':
                    student_data2 = Student.query.filter_by(student_id_num=j.get_target_user()).first()
                    student_name = student_data2.student_first_name + " " + student_data2.student_last_name
                    notif_user_dict[j.get_target_user()] = student_name
                elif j.get_target_user()[0] == 'T':
                    tutor_data2 = Tutor.query.filter_by(tutor_id_num=j.get_target_user()).first()
                    tutor_name = tutor_data2.tutor_first_name + " " + tutor_data2.tutor_last_name
                    notif_user_dict[j.get_target_user()] = tutor_name
        except:
            pass

        return render_template('adminUpdateNotification.html', count=len(notif_data), form=update_notification_form,
                               student_data=student_data, student_name_dict=student_name_dict, tutor_data=tutor_data,
                               tutor_name_dict=tutor_name_dict, notif_list=notif_data, notif_user_dict=notif_user_dict)
    return redirect(url_for('tutor_login'))


@app.route('/createTodo', methods=['POST', 'GET'])
def create_todo():
    if g.user[0] == 'A':
        create_todo_form = CreateTodo(request.form)
        if request.method == 'POST' and create_todo_form.validate():
            todo_dict = {}
            db = shelve.open('todo.db', 'c')

            try:
                todo_dict = db['Todo']
                Todo.count_id = db['Todo_id']
            except:
                print("Error in retrieving To Do list from Database")

            date = datetime.now()
            date = date.strftime("%A, %d %B %Y %I:%M%p")
            todo = Todo(create_todo_form.text.data, date)
            todo_dict[todo.get_todo_id()] = todo
            db['Todo'] = todo_dict
            db['Todo_id'] = Todo.count_id

            db.close()

            return redirect(url_for('admin_main'))
    return redirect(url_for('tutor_login'))


@app.route('/retrieveTodo')
def retrieve_todo():
    if g.user[0] == 'A':
        todo_dict = {}
        db = shelve.open('todo.db', 'r')
        todo_dict = db['Todo']
        db.close()

        todo_list = []
        for key in todo_dict:
            todo = todo_dict.get(key)
            todo_list.append(todo)

        return redirect(url_for('admin_main'))
    return redirect(url_for('tutor_login'))


@app.route('/updateTodo/<int:todo_id>', methods=['GET', 'POST'])
def update_todo(todo_id):
    if g.user[0] == 'A':
        update_todo_form = CreateTodo(request.form)
        if request.method == 'POST' and update_todo_form.validate():
            todo_dict = {}
            db = shelve.open('todo.db', 'w')
            todo_dict = db['Todo']

            todo = todo_dict.get(todo_id)
            todo.set_todo_text(update_todo_form.text.data)

            db['Todo'] = todo_dict
            db.close()

            return redirect(url_for('admin_main'))
        else:
            todo_dict = {}
            db = shelve.open('todo.db', 'r')
            todo_dict = db['Todo']
            db.close()

            todo = todo_dict.get(todo_id)
            update_todo_form.text.data = todo.get_todo_text()
            return redirect(url_for('admin_main'))
    return redirect(url_for('tutor_login'))


@app.route('/deleteTodo/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    todo_dict = {}
    db = shelve.open('todo.db', 'w')
    todo_dict = db['Todo']

    todo_dict.pop(todo_id)

    db['Todo'] = todo_dict
    db.close()

    return redirect(url_for('retrieve_todo'))


# -------------------- ADMIN END --------------------


# -------------------- GOH CHOON MENG, JEREN, TUTOR START--------------------
@app.route('/TutorRetrieveContent')
def tutor_retrieve_content():
    if g.user[0] == 'T':
        id_num = session["user"]

        tutor_profile_name = ""
        tutor_profile_img = ""

        with app.app_context():
            tutor_profile = Tutor.query.filter_by(tutor_id_num=id_num).first()
            tutor_id_num = tutor_profile.tutor_id_num
            if tutor_id_num == id_num:
                tutor_profile_name = tutor_profile.tutor_first_name + " " + tutor_profile.tutor_last_name
                tutor_profile_img = tutor_profile.tutor_img

        content_dict = {}
        file_dict2 = {}
        content_list = []

        try:
            db = shelve.open('content2.db', 'r')
            content_dict = db['Content']
            db.close()

            filename = []
            for key in content_dict:
                contentx = content_dict.get(key)
                content_list.append(contentx)

            for i in content_list:
                olo = i.get_cid()
                cname = i.get_cfile()
                file_dict2[olo] = cname
        except:
            pass
        tests_dict = {}
        tests_list = []
        try:
            db = shelve.open('content.db', 'r')
            tests_dict = db['Tests']
            db.close()

            for key in tests_dict:
                test = tests_dict.get(key)
                tests_list.append(test)
        except:
            pass

        # ---------- Display announcement ---------- #
        ann_dict = {}
        ann_list = []
        user_dict = {}
        file_dict = {}
        filename = []

        try:
            db = shelve.open('announcement.db', 'r')
            ann_dict = db['announce']
            db.close()

            for key in ann_dict:
                announcement = ann_dict.get(key)
                ann_list.append(announcement)

            for i in ann_list:
                lol = i.get_ann_id()
                iname = i.get_files()
                file_dict[lol] = iname

            for i in ann_list:
                user_id = i.get_id_num()
                if user_id[0] == "T":
                    tutor_account = Tutor.query.filter_by(tutor_id_num=user_id).first()
                    tutor_first_name = tutor_account.tutor_first_name
                    tutor_last_name = tutor_account.tutor_last_name
                    name = tutor_first_name + " " + tutor_last_name + "  (Tutor)"
                    user_dict[user_id] = name
                else:
                    user_dict[user_id] = 'Jabe Ez (Administrator)'

        except:
            pass

        return render_template('tutorRetrieveContent.html', count_test=len(tests_list), tests_list=tests_list,
                               ann_list=ann_list, user_dict=user_dict, file_dict=file_dict, id_num=id_num,
                               tutor_profile_name=tutor_profile_name, tutor_profile_img=tutor_profile_img,
                               content_list=content_list, count_content=len(content_list), file_dict2=file_dict2)
    return redirect(url_for("tutor_login"))


@app.route('/createContent', methods=['GET', 'POST'])
def create_content():
    if g.user[0] == "T":
        id_num = session['user']

        tutor_profile_name = ""
        tutor_profile_img = ""

        with app.app_context():
            tutor_profile = Tutor.query.filter_by(tutor_id_num=id_num).first()
            tutor_id_num = tutor_profile.tutor_id_num
            if tutor_id_num == id_num:
                tutor_profile_name = tutor_profile.tutor_first_name + " " + tutor_profile.tutor_last_name
                tutor_profile_img = tutor_profile.tutor_img

        content_form = CreateStudentContent(request.form)
        if request.method == 'POST' and content_form.validate():
            content_dict = {}
            db = shelve.open('content2.db', 'c')
            try:
                content_dict = db['Content']
            except:
                print('Error in retrieving student content from content.db')

            if 'contentfile' not in request.files:
                return redirect(request.url)

            cfile = request.files['contentfile']

            if cfile.filename == '':
                filename = ''
                cfile = filename

            elif cfile and allowed_file3(cfile.filename):
                filename = str(uuid.uuid1()) + "_" + secure_filename(cfile.filename)
                cfile.save(os.path.join(app.config['UPLOAD_FOLDER_CONTENT'], filename))
                cfile = filename
                print(cfile)

            else:
                return redirect(url_for('create_feedback_form'))

            contentx = Content(content_form.content_subject.data, content_form.cname.data, cfile)
            content_dict[contentx.get_cid()] = contentx
            db['Content'] = content_dict

            db.close()
            return redirect(url_for('tutor_retrieve_content'))
        return render_template('TutorCreateContent.html', form=content_form, tutor_profile_img=tutor_profile_img, tutor_profile_name=tutor_profile_name)
    return redirect(url_for('tutor_login'))


@app.route('/updateContent/<int:id>/', methods=['GET', 'POST'])
def update_content(id):
    if g.user[0] == "T":
        id_num = session["user"]

        tutor_profile_name = ""
        tutor_profile_img = ""

        with app.app_context():
            tutor_profile = Tutor.query.filter_by(tutor_id_num=id_num).first()
            tutor_id_num = tutor_profile.tutor_id_num
            if tutor_id_num == id_num:
                tutor_profile_name = tutor_profile.tutor_first_name + " " + tutor_profile.tutor_last_name
                tutor_profile_img = tutor_profile.tutor_img

        update_content_form = CreateStudentContent(request.form)
        if request.method == 'POST' and update_content_form.validate():
            content_dict = {}
            db = shelve.open('content2.db', 'w')
            content_dict = db['Content']

            contentx = content_dict.get(id)
            contentx.set_content_subject(update_content_form.content_subject.data)
            contentx.set_cname(update_content_form.cname.data)

            db['Content'] = content_dict
            db.close()

            return redirect(url_for('tutor_retrieve_content'))
        else:
            content_dict = {}
            db = shelve.open('content2.db', 'r')
            content_dict = db['Content']
            db.close()

            contentx = content_dict.get(id)
            update_content_form.content_subject.data = contentx.get_content_subject()
            update_content_form.cname.data = contentx.get_cname()

            return render_template('TutorUpdateContent.html', form=update_content_form, tutor_profile_img=tutor_profile_img, tutor_profile_name=tutor_profile_name)
    return redirect(url_for('tutor_login'))


@app.route('/deleteContent/<int:id>', methods=['POST'])
def delete_content(id):
    content_dict = {}
    db = shelve.open('content2.db', 'w')
    content_dict = db['Content']

    content_dict.pop(id)

    db['Content'] = content_dict
    db.close()

    return redirect(url_for('tutor_retrieve_content'))


@app.route('/tutorAnnouncement', methods=['GET', 'POST'])
def tutor_announcement():
    if g.user[0] == 'T':
        id_num = session['user']

        tutor_profile_name = ""
        tutor_profile_img = ""
        with app.app_context():
            tutor_profile = Tutor.query.filter_by(tutor_id_num=id_num).first()
            tutor_id_num = tutor_profile.tutor_id_num
            if tutor_id_num == id_num:
                tutor_profile_name = tutor_profile.tutor_first_name + " " + tutor_profile.tutor_last_name
                tutor_profile_img = tutor_profile.tutor_img

        ann_dict = {}
        file_dict = {}
        ann_list = []
        filename = []
        my_announcement = []
        try:
            db = shelve.open('announcement.db', 'r')
            ann_dict = db['announce']
            db.close()

            for key in ann_dict:
                announcement = ann_dict.get(key)
                ann_list.append(announcement)

            for i in ann_list:
                lol = i.get_ann_id()
                iname = i.get_files()
                file_dict[lol] = iname

            for j in ann_list:
                if j.get_id_num() == id_num:
                    my_announcement.append(j)
        except:
            pass

        create_announcement_form = CreateAnnouncementForm(request.form)
        tutor_list = []
        if request.method == 'POST' and create_announcement_form.validate():
            ann_dict = {}
            db = shelve.open('announcement.db', 'c')

            try:
                ann_dict = db['announce']
                Announcement.count_id = db['announce_id']

            except:
                db['announce'] = ann_dict

            if 'file' not in request.files:
                return redirect(request.url)

            afile = request.files['file']

            if afile.filename == '':
                filename = ''
                afile = filename

            elif afile and allowed_file(afile.filename):
                filename = str(uuid.uuid1()) + "_" + secure_filename(afile.filename)
                afile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                afile = filename

            else:
                filename = secure_filename(afile.filename)
                file_ext = allowed_file(filename)
                if file_ext not in app.config['ALLOWED_EXTENSIONS'] or file_ext != validate_image(afile.stream):
                    flash('Invalid File Type.')
                    return redirect(url_for('create_announcement'))

            date = datetime.now()
            date = date.strftime("%A, %d %B %Y %I:%M%p")
            update = None
            announcement = announce.Announcement(id_num, date, create_announcement_form.atitle.data,
                                                 create_announcement_form.acontent.data, afile, update)
            ann_dict[announcement.get_ann_id()] = announcement
            db['announce'] = ann_dict
            db['announce_id'] = Announcement.count_id
            db.close()

            return redirect(url_for('tutor_retrieve_content'))
        return render_template('tutorAnnouncement.html', form=create_announcement_form, tutor_list=tutor_list,
                               count=len(my_announcement), ann_list=my_announcement, file_dict=file_dict,
                               tutor_profile_name=tutor_profile_name, tutor_profile_img=tutor_profile_img)
    return redirect(url_for('tutor_login'))


@app.route('/updateTutorAnnouncement/<int:id>/', methods=['GET', 'POST'])
def tutor_update_announcement(id):
    if g.user[0] == "T":
        id_num = session['user']

        tutor_profile_name = ""
        tutor_profile_img = ""

        with app.app_context():
            tutor_profile = Tutor.query.filter_by(tutor_id_num=id_num).first()
            tutor_id_num = tutor_profile.tutor_id_num
            if tutor_id_num == id_num:
                tutor_profile_name = tutor_profile.tutor_first_name + " " + tutor_profile.tutor_last_name
                tutor_profile_img = tutor_profile.tutor_img

        ann_dict = {}
        file_dict = {}
        ann_list = []
        filename = []
        my_announcement = []
        try:
            db = shelve.open('announcement.db', 'r')
            ann_dict = db['announce']
            db.close()

            for key in ann_dict:
                announcement = ann_dict.get(key)
                ann_list.append(announcement)

            for i in ann_list:
                lol = i.get_ann_id()
                iname = i.get_files()
                file_dict[lol] = iname

            for j in ann_list:
                if j.get_id_num() == id_num:
                    my_announcement.append(j)

        except:
            pass

        edit_announcement_form = CreateAnnouncementForm(request.form)
        if request.method == 'POST' and edit_announcement_form.validate():
            ann_dict = {}
            db = shelve.open('announcement.db', 'w')
            ann_dict = db['announce']
            announcement = ann_dict.get(id)
            announcement.set_title(edit_announcement_form.atitle.data)
            announcement.set_content(edit_announcement_form.acontent.data)
            date2 = datetime.now()
            update = date2.strftime("%A, %d %B %Y %I:%M%p")
            announcement.set_update(update)
            db['announce'] = ann_dict
            db.close()
            return redirect(url_for('tutor_announcement'))
        else:
            ann_dict = {}
            db = shelve.open('announcement.db', 'r')
            ann_dict = db['announce']
            db.close()

            announcement = ann_dict.get(id)
            edit_announcement_form.atitle.data = announcement.get_title()
            edit_announcement_form.acontent.data = announcement.get_content()
        return render_template('updateTutorAnnouncement.html', form=edit_announcement_form, count=len(my_announcement),
                               ann_list=my_announcement, file_dict=file_dict, tutor_profile_name=tutor_profile_name,
                               tutor_profile_img=tutor_profile_img)
    return redirect(url_for('tutor_login'))


@app.route('/tdeleteAnnouncements/<int:id>', methods=['POST', 'GET'])
def t_delete_announcement(id):
    ann_dict = {}
    db = shelve.open('announcement.db', 'w')
    ann_dict = db['announce']
    ann_dict.pop(id)
    db['announce'] = ann_dict
    db.close()
    return redirect(url_for('tutor_retrieve_content'))


@app.route('/createTest', methods=['GET', 'POST'])
def create_tests():
    if g.user[0] == 'T':
        id_num = session['user']
        tutor_profile_name = ""
        tutor_profile_img = ""
        with app.app_context():
            tutor_profile = Tutor.query.filter_by(tutor_id_num=id_num).first()
            tutor_id_num = tutor_profile.tutor_id_num
            if tutor_id_num == id_num:
                tutor_profile_name = tutor_profile.tutor_first_name + " " + tutor_profile.tutor_last_name
                tutor_profile_img = tutor_profile.tutor_img

        create_test_question = CreateTestQuestion(request.form)
        if request.method == 'POST' and create_test_question.validate():
            tests_dict = {}
            db = shelve.open('content.db', 'c')
            try:
                tests_dict = db['Tests']
            except:
                print("Error in retrieving test from test.db.")
            test = Test.Test(create_test_question.content_id.data, create_test_question.content_subject.data,
                             create_test_question.marks.data, create_test_question.q1.data,
                             create_test_question.a1.data, create_test_question.q2.data, create_test_question.a2.data,
                             create_test_question.q3.data, create_test_question.a3.data)
            tests_dict[test.get_content_id()] = test
            db['Tests'] = tests_dict

            db.close()
            return redirect(url_for('tutor_retrieve_content'))
        return render_template('TutorCreateTest.html', form=create_test_question, tutor_profile_name=tutor_profile_name,
                               tutor_profile_img=tutor_profile_img)
    return redirect(url_for('tutor_login'))


@app.route('/updateTest/<string:id>/', methods=['GET', 'POST'])
def update_test(id):
    if g.user[0] == "T":
        id_num = session['user']
        tutor_profile_name = ""
        tutor_profile_img = ""

        with app.app_context():
            tutor_profile = Tutor.query.filter_by(tutor_id_num=id_num).first()
            tutor_id_num = tutor_profile.tutor_id_num
            if tutor_id_num == id_num:
                tutor_profile_name = tutor_profile.tutor_first_name + " " + tutor_profile.tutor_last_name
                tutor_profile_img = tutor_profile.tutor_img

        update_test_question = CreateTestQuestion(request.form)
        if request.method == 'POST' and update_test_question.validate():
            tests_dict = {}
            db = shelve.open('content.db', 'w')
            tests_dict = db['Tests']

            test = tests_dict.get(id)
            test.set_content_id(update_test_question.content_id.data)
            test.set_content_subject(update_test_question.content_subject.data)
            test.set_marks(update_test_question.marks.data)
            test.set_q1(update_test_question.q1.data)
            test.set_a1(update_test_question.a1.data)
            test.set_q2(update_test_question.q2.data)
            test.set_a2(update_test_question.a2.data)
            test.set_q3(update_test_question.q3.data)
            test.set_a3(update_test_question.a3.data)

            db['Tests'] = tests_dict
            db.close()

            return redirect(url_for('tutor_retrieve_content'))
        else:
            tests_dict = {}
            db = shelve.open('content.db', 'r')
            tests_dict = db['Tests']
            db.close()

            test = tests_dict.get(id)
            update_test_question.content_id.data = test.get_content_id()
            update_test_question.content_subject.data = test.get_content_subject()
            update_test_question.marks.data = test.get_marks()
            update_test_question.q1.data = test.get_q1()
            update_test_question.a1.data = test.get_a1()
            update_test_question.q2.data = test.get_q2()
            update_test_question.a2.data = test.get_a2()
            update_test_question.q3.data = test.get_q3()
            update_test_question.a3.data = test.get_a3()

        return render_template('TutorUpdateTest.html', form=update_test_question, tutor_profile_name=tutor_profile_name,
                               tutor_profile_img=tutor_profile_img)
    return redirect(url_for('tutor_login'))


@app.route('/deleteTest/<string:id>', methods=['POST'])
def delete_test(id):
    tests_dict = {}
    db = shelve.open('content.db', 'w')
    tests_dict = db['Tests']

    tests_dict.pop(id)

    db['Tests'] = tests_dict
    db.close()

    return redirect(url_for('tutor_retrieve_content'))


@app.route('/tutorNotification', methods=['GET', 'POST'])
def tutor_notification():
    if g.user[0] == "T":
        id_num = session["user"]

        tutor_profile_name = ""
        tutor_profile_img = ""

        with app.app_context():
            tutor_profile = Tutor.query.filter_by(tutor_id_num=id_num).first()
            tutor_id_num = tutor_profile.tutor_id_num
            if tutor_id_num == id_num:
                tutor_profile_name = tutor_profile.tutor_first_name + " " + tutor_profile.tutor_last_name
                tutor_profile_img = tutor_profile.tutor_img

        notification_dict = {}
        notification_list = []
        my_notification = []
        try:
            db = shelve.open('notification.db', 'r')
            notification_dict = db['Notification']
            db.close()

            notification_list = []
            my_notification = []
            for key in notification_dict:
                notif = notification_dict.get(key)
                notification_list.append(notif)

            for i in notification_list:
                if i.get_sender() == id_num:
                    my_notification.append(i)

        except:
            pass

        create_notification_form = CreateNotifications(request.form)
        if request.method == 'POST' and create_notification_form.validate():
            notification_dict = {}
            db = shelve.open('notification.db', 'c')

            try:
                notification_dict = db['Notification']
                Notification.count_id = db["Notification_id"]
            except:
                print("Error in retrieving Notifications from Database")

            sender = id_num
            date = datetime.now()
            date = date.strftime("%A, %d %B %Y %I:%M%p")
            notification = Notification(date, create_notification_form.title.data,
                                        create_notification_form.description.data,
                                        create_notification_form.target_user.data, sender)
            notification_dict[notification.get_notif_id()] = notification
            db['Notification'] = notification_dict
            db['Notification_id'] = Notification.count_id
            db.close()

            return redirect(url_for('tutor_notification'))
        return render_template('tutorNotification.html', form=create_notification_form, count=len(my_notification),
                               notification_list=my_notification, tutor_profile_name=tutor_profile_name,
                               tutor_profile_img=tutor_profile_img)
    return redirect(url_for('tutor_login'))


@app.route('/updateTutorNotification/<int:notif_id>/', methods=['GET', 'POST'])
def tutor_update_notification(notif_id):
    if g.user[0] == "T":
        id_num = session["user"]

        tutor_profile_name = ""
        tutor_profile_img = ""

        with app.app_context():
            tutor_profile = Tutor.query.filter_by(tutor_id_num=id_num).first()
            tutor_id_num = tutor_profile.tutor_id_num
            if tutor_id_num == id_num:
                tutor_profile_name = tutor_profile.tutor_first_name + " " + tutor_profile.tutor_last_name
                tutor_profile_img = tutor_profile.tutor_img

        notification_dict = {}
        notification_list = []
        my_notification = []
        try:
            db = shelve.open('notification.db', 'r')
            notification_dict = db['Notification']
            db.close()

            notification_list = []
            my_notification = []
            for key in notification_dict:
                notif = notification_dict.get(key)
                notification_list.append(notif)

            for i in notification_list:
                if i.get_sender() == id_num:
                    my_notification.append(i)

        except:
            pass

        update_notification_form = CreateNotifications(request.form)
        if request.method == 'POST' and update_notification_form.validate():
            notification_dict = {}
            db = shelve.open('notification.db', 'w')
            notification_dict = db['Notification']

            notif = notification_dict.get(notif_id)
            notif.set_target_user(update_notification_form.target_user.data)
            notif.set_title(update_notification_form.title.data)
            notif.set_description(update_notification_form.description.data)

            db['Notification'] = notification_dict
            db.close()

            return redirect(url_for('tutor_notification'))
        else:
            notification_dict = {}
            db = shelve.open('notification.db', 'r')
            notification_dict = db['Notification']
            db.close()

            notif = notification_dict.get(notif_id)
            update_notification_form.target_user.data = notif.get_target_user()
            update_notification_form.title.data = notif.get_title()
            update_notification_form.description.data = notif.get_description()

        return render_template('updateTutorNotification.html', form=update_notification_form,
                               count=len(my_notification), notification_list=my_notification,
                               tutor_profile_name=tutor_profile_name, tutor_profile_img=tutor_profile_img)
    return redirect(url_for('tutor_login'))


@app.route('/tutorFeedback', methods=['GET', 'POST'])
def tutor_feedback():
    if g.user[0] == "T":
        id_num = session['user']
        tutor_profile_name = ""
        tutor_profile_img = ""

        with app.app_context():
            tutor_profile = Tutor.query.filter_by(tutor_id_num=id_num).first()
            tutor_id_num = tutor_profile.tutor_id_num
            if tutor_id_num == id_num:
                tutor_profile_name = tutor_profile.tutor_first_name + " " + tutor_profile.tutor_last_name
                tutor_profile_img = tutor_profile.tutor_img

        name = ""
        feedback_dict = {}
        Sfeedback_list = []
        Tfeedback_list = []
        feedback_list = []
        file_dict = {}
        filename = []
        try:
            db = shelve.open('Feedback.db', 'r')
            feedback_dict = db['Feedback']
            db.close()

            for key in feedback_dict:
                feedback = feedback_dict.get(key)
                feedback_list.append(feedback)

            for i in feedback_list:
                lol = i.get_feedback_id()
                aname = i.get_feedback_file()
                file_dict[lol] = aname

            for j in feedback_list:
                if j.get_feedback_subject() == "Academic Assistance":
                    Sfeedback_list.append(j)

                if j.get_feedback_adminid() == id_num:
                    Tfeedback_list.append(j)
        except:
            pass

        if id_num[0] == 'S' and inspector.has_table("student"):
            student_account = Student.query.all()
            for i in student_account:
                student_id = i.student_id_num
                if id_num == student_id:
                    student_info = Student.query.filter_by(student_id_num=id_num).first()
                    name = student_info.student_first_name + " " + student_info.student_last_name
        elif id_num[0] == 'T' and inspector.has_table("tutor"):
            tutor_account = Tutor.query.all()
            for i in tutor_account:
                tutor_id = i.tutor_id_num
                if id_num == tutor_id:
                    tutor_info = Tutor.query.filter_by(tutor_id_num=id_num).first()
                    name = tutor_info.tutor_first_name + " " + tutor_info.tutor_last_name
        else:
            name = None

        create_feedback_form = CreateFeedback(request.form)
        if request.method == 'POST' and create_feedback_form.validate():
            feedback_dict = {}
            db = shelve.open('Feedback.db', 'c')
            try:
                feedback_dict = db['Feedback']
                Feedback.count_id = db['Feedback_feedback_id']

            except:
                print("Error in retrieving Feedback1 from Feedback.db.")
                db['Feedback'] = feedback_dict

            if 'file2' not in request.files:
                return redirect(request.url)

            file2 = request.files['file2']

            if file2.filename == '':
                filename = ''
                file2 = filename

            elif file2 and allowed_file2(file2.filename):
                filename = str(uuid.uuid1()) + "_" + secure_filename(file2.filename)
                file2.save(os.path.join(app.config['UPLOAD_FOLDER_ANDI'], filename))
                file2 = filename

            else:
                filename = secure_filename(file2.filename)
                file_ext = allowed_file2(filename)
                if file_ext not in app.config['ALLOWED_EXTENSIONS2'] or file_ext != validate_image(file2.stream):
                    flash('Invalid File Type')
                    return redirect(url_for('create_feedback_form'))

            date = datetime.now()
            date = date.strftime("%A, %d %B %Y %I:%M%p")
            feedback = Feedback(
                id_num,
                create_feedback_form.feedback_subject.data,
                create_feedback_form.feedback_title.data,
                create_feedback_form.feedback_description.data,
                name,
                date,
                file2)
            feedback_dict[feedback.get_feedback_id()] = feedback
            db['Feedback'] = feedback_dict
            db['Feedback_feedback_id'] = Feedback.count_id
            db.close()
            return redirect(url_for('tutor_feedback'))
        return render_template('tutorFeedback.html', form=create_feedback_form, Tcount=len(Tfeedback_list),
                               Tfeedback_list=Tfeedback_list, Scount=len(Sfeedback_list), Sfeedback_list=Sfeedback_list,
                               file_dict=file_dict, tutor_profile_name=tutor_profile_name,
                               tutor_profile_img=tutor_profile_img)
    return redirect(url_for('tutor_login'))


@app.route('/tdeleteFeedback/<int:id>', methods=['POST'])
def t_delete_feedback(id):
    feedback_dict = {}
    db = shelve.open('Feedback.db', 'w')
    feedback_dict = db['Feedback']
    feedback_dict.pop(id)
    db['Feedback'] = feedback_dict
    db.close()
    return redirect(url_for('tutor_feedback'))


@app.route('/tdeleteNotification/<int:notif_id>', methods=['POST'])
def delete_notification(notif_id):
    notification_dict = {}
    db = shelve.open('notification.db', 'w')
    notification_dict = db['Notification']

    notification_dict.pop(notif_id)

    db['Notification'] = notification_dict
    db.close()

    return redirect(url_for('tutor_notification'))


@app.route('/studentTestQuestion/<string:id>/', methods=['GET', 'POST'])
def student_test_question(id):
    if g.user[0] == 'S':
        id_num = session['user']
        student_profile_name = ""
        student_profile_img = ""

        with app.app_context():
            student_profile = Student.query.filter_by(student_id_num=id_num).first()
            student_id_num = student_profile.student_id_num
            if student_id_num == id_num:
                student_profile_name = student_profile.student_first_name + " " + student_profile.student_last_name
                student_profile_img = student_profile.student_img

        tests_dict = {}
        db = shelve.open('content.db', 'r')
        tests_dict = db['Tests']
        db.close()

        tests_list = []
        count_marks = 0
        for key in tests_dict:
            if key == id:
                tests = tests_dict.get(key)
                tests_list.append(tests)
                break
            else:
                print("Error")

        student_test_question = StudentTestQuestion(request.form)
        if request.method == 'POST':
            s_tests_dict = {}
            db = shelve.open('student.db', 'c')
            try:
                s_tests_dict = db['Tests']
            except:
                print("Error in retrieving test from test.db.")
            test = STEST.STest(student_test_question.content_id.data, student_test_question.content_subject.data,
                               student_test_question.a1.data, student_test_question.a2.data, student_test_question.a3.data)
            s_tests_dict[test.get_content_id()] = test
            db['Tests'] = s_tests_dict
            db.close()

            l1 = []
            l2 = []
            for key in tests_dict:
                if key == id:
                    test = tests_dict.get(key)
                    l1.append(test)

            for key in s_tests_dict:
                student_test = s_tests_dict.get(key)
                l2.append(student_test)

            for i in l1:
                a1 = i.get_a1()
                a2 = i.get_a2()
                a3 = i.get_a3()
                for j in l2:
                    sa1 = j.get_a1()
                    sa2 = j.get_a2()
                    sa3 = j.get_a3()
                    if a1 == sa1:
                        count_marks += 1
                    if a2 == sa2:
                        count_marks += 1
                    if a3 == sa3:
                        count_marks += 1

            marks_dict = {}
            db = shelve.open('content.db', 'w')
            try:
                marks_dict = db['Tests']
            except:
                print('error retrieving test marks')

            test = marks_dict.get(id)
            test.set_marks(count_marks)
            print(count_marks)
            db['Tests'] = marks_dict
            db.close()

            return redirect(url_for('retrieve_content'))
        return render_template('StudentTest.html', tests_list=tests_list, form=student_test_question, student_profile_img=student_profile_img, student_profile_name=student_profile_name)
    return redirect(url_for('student_login'))


@app.route('/StudentRetrieveContent')
def retrieve_content():
    if g.user[0] == "S":
        id_num = session['user']
        student_profile_name = ""
        student_profile_img = ""

        with app.app_context():
            student_profile = Student.query.filter_by(student_id_num=id_num).first()
            student_id_num = student_profile.student_id_num
            if student_id_num == id_num:
                student_profile_name = student_profile.student_first_name + " " + student_profile.student_last_name

                student_profile_img = student_profile.student_img

        content_dict = {}
        file_dict2 = {}
        content_list = []

        try:
            db = shelve.open('content2.db', 'r')
            content_dict = db['Content']
            db.close()

            filename = []
            for key in content_dict:
                contentx = content_dict.get(key)
                content_list.append(contentx)

            for i in content_list:
                olo = i.get_cid()
                cname = i.get_cfile()
                file_dict2[olo] = cname
        except:
            pass

        tests_dict = {}
        tests_list = []
        try:
            db = shelve.open('content.db', 'r')
            tests_dict = db['Tests']
            db.close()

            for key in tests_dict:
                test = tests_dict.get(key)
                tests_list.append(test)
        except:
            pass

        # ---------- Display announcement ---------- #
        ann_dict = {}
        ann_list = []
        user_dict = {}
        file_dict = {}
        filename = []

        try:
            db = shelve.open('announcement.db', 'r')
            ann_dict = db['announce']
            db.close()

            for key in ann_dict:
                announcement = ann_dict.get(key)
                ann_list.append(announcement)

            for i in ann_list:
                lol = i.get_ann_id()
                iname = i.get_files()
                file_dict[lol] = iname

            for i in ann_list:
                user_id = i.get_id_num()
                if user_id[0] == "T":
                    tutor_account = Tutor.query.filter_by(tutor_id_num=user_id).first()
                    tutor_first_name = tutor_account.tutor_first_name
                    tutor_last_name = tutor_account.tutor_last_name
                    name = tutor_first_name + " " + tutor_last_name + "  (Tutor)"
                    user_dict[user_id] = name
                else:
                    user_dict[user_id] = 'Jabe Ez (Administrator)'

        except:
            pass

        return render_template('StudentRetrieveContent.html', test_count=len(tests_list), tests_list=tests_list, student_profile_img=student_profile_img, student_profile_name=student_profile_name,  ann_list=ann_list, user_dict=user_dict, file_dict=file_dict,
                           content_list=content_list, count_content=len(content_list), file_dict2=file_dict2)
    return redirect(url_for('student_login'))


@app.route('/s_retrieveNotification')
def s_retrieve_notification():
    if g.user[0] == "S":
        id_num = session['user']
        student_profile_name = ""
        student_profile_img = ""

        with app.app_context():
            student_profile = Student.query.filter_by(student_id_num=id_num).first()
            student_id_num = student_profile.student_id_num
            if student_id_num == id_num:
                student_profile_name = student_profile.student_first_name + " " + student_profile.student_last_name
                student_profile_img = student_profile.student_img
        notification_dict = {}
        db = shelve.open('notification.db', 'r')
        notification_dict = db['Notification']
        db.close()
        sender_name = ''
        notification_list = []
        sender_dict = {}
        for key in notification_dict:
            notif = notification_dict.get(key)
            sender = notif.get_sender()
            if sender[0] == 'T':
                tutor_data = Tutor.query.filter_by(tutor_id_num=sender).first()
                sender_name = tutor_data.tutor_first_name + " " + tutor_data.tutor_last_name
                sender_dict[sender] = sender_name
            elif sender[0] == 'A':
                sender_name = 'Jabe Ez (Admin)'
                sender_dict[sender] = sender_name
            if notif.get_target_user() == id_num:
                notification_list.append(notif)

        return render_template('s_retrieveNotification.html', count=len(notification_list),
                               notification_list=notification_list, sender_name=sender_name, sender_dict=sender_dict, student_profile_img=student_profile_img, student_profile_name=student_profile_name)
    return redirect(url_for('student_login'))


@app.route('/studentFeedback', methods=['GET', 'POST'])
def student_feedback():
    if g.user[0] == "S":
        name = ""
        id_num = session['user']
        student_profile_name = ""
        student_profile_img = ""

        with app.app_context():
            student_profile = Student.query.filter_by(student_id_num=id_num).first()
            student_id_num = student_profile.student_id_num
            if student_id_num == id_num:
                student_profile_name = student_profile.student_first_name + " " + student_profile.student_last_name
                student_profile_img = student_profile.student_img
        feedback_dict = {}
        file_dict = {}
        feedback_list = []
        admin_account = []
        filename = []
        name_list = []
        try:
            db = shelve.open('Feedback.db', 'r')
            feedback_dict = db['Feedback']
            db.close()

            tutor_account = Tutor.query.all()
            for i in tutor_account:
                tutor_id = i.tutor_id_num
                if tutor_id == id_num:
                    details = Tutor.query.filter_by(tutor_id_num=id_num).first()
                    name_list.append(details)

            for key in feedback_dict:
                feedback = feedback_dict.get(key)
                if feedback.get_feedback_adminid() == id_num:
                    feedback_list.append(feedback)
                else:
                    admin = feedback_dict.get(key)
                    admin_account.append(admin)

            for i in feedback_list:
                lol = i.get_feedback_id()
                iname = i.get_feedback_file()
                file_dict[lol] = iname

        except:
            pass

        if id_num[0] == 'S' and inspector.has_table("student"):
            student_account = Student.query.all()
            for i in student_account:
                student_id = i.student_id_num
                if id_num == student_id:
                    student_info = Student.query.filter_by(student_id_num=id_num).first()
                    name = student_info.student_first_name + " " + student_info.student_last_name
        elif id_num[0] == 'T' and inspector.has_table("tutor"):
            tutor_account = Tutor.query.all()
            for i in tutor_account:
                tutor_id = i.tutor_id_num
                if id_num == tutor_id:
                    tutor_info = Tutor.query.filter_by(tutor_id_num=id_num).first()
                    name = tutor_info.tutor_first_name + " " + tutor_info.tutor_last_name
        else:
            name = None

        create_feedback_form = CreateFeedback(request.form)
        if request.method == 'POST' and create_feedback_form.validate():
            feedback_dict = {}
            db = shelve.open('Feedback.db', 'c')
            try:
                feedback_dict = db['Feedback']
                Feedback.count_id = db['Feedback_feedback_id']

            except:
                print("Error in retrieving Feedback2 from Feedback.db.")
                db['Feedback'] = feedback_dict

            if 'file2' not in request.files:
                return redirect(request.url)

            file2 = request.files['file2']

            if file2.filename == '':
                filename = ''
                file2 = filename

            elif file2 and allowed_file2(file2.filename):
                filename = str(uuid.uuid1()) + "_" + secure_filename(file2.filename)
                file2.save(os.path.join(app.config['UPLOAD_FOLDER_ANDI'], filename))
                file2 = filename

            else:
                filename = secure_filename(file2.filename)
                file_ext = allowed_file2(filename)
                if file_ext not in app.config['ALLOWED_EXTENSIONS2'] or file_ext != validate_image(file2.stream):
                    flash('Invalid File Type')
                    return redirect(url_for('create_feedback_form2'))

            date = datetime.now()
            date = date.strftime("%A, %d %B %Y %I:%M%p")
            feedback = Feedback(
                id_num,
                create_feedback_form.feedback_subject.data,
                create_feedback_form.feedback_title.data,
                create_feedback_form.feedback_description.data,
                name,
                date, file2)
            feedback_dict[feedback.get_feedback_id()] = feedback
            db['Feedback'] = feedback_dict
            db['Feedback_feedback_id'] = Feedback.count_id
            db.close()
            return redirect(url_for('student_feedback'))
        return render_template('studentFeedback.html', form=create_feedback_form,count=len(feedback_list), feedback_list=feedback_list, user=session['user'], name_list=name_list, file_dict=file_dict, student_profile_img=student_profile_img, student_profile_name=student_profile_name)
    return redirect(url_for('student_login'))

# ----------------- Chat Group ------------------ #


@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if g.user[0] == "T":
        id_num = session['user']
        if request.method == 'POST':

            if id_num[0] == 'T':
                tutor_info = Tutor.query.filter_by(tutor_id_num=id_num).first()
                first_name = tutor_info.tutor_first_name
                last_name = tutor_info.tutor_last_name
                username = first_name + ' ' + last_name + ' [TUTOR]'

            else:
                username = 'Anonymous'

            room = request.form['room']
            # Store the data in session
            session['username'] = username
            session['room'] = room
            return render_template('chatroom.html', session=session)
        else:
            if session.get('username') is not None:
                return render_template('chatroom.html', session=session)
            else:
                return redirect(url_for('index.html'))
    return redirect(url_for("tutor_login"))


@app.route('/s_chat', methods=['GET', 'POST'])
def s_chat():
    if g.user[0] == "S":
        id_num = session['user']
        if request.method == 'POST':

            if id_num[0] == 'S':
                student_info = Student.query.filter_by(student_id_num=id_num).first()
                first_name = student_info.student_first_name
                last_name = student_info.student_last_name
                username = first_name + ' ' + last_name + ' [STUDENT]'

            else:
                username = 'Anonymous'

            room = request.form['room']
            # Store the data in session
            session['username'] = username
            session['room'] = room
            return render_template('s_chatroom.html', session=session)
        else:
            if session.get('username') is not None:
                return render_template('s_chatroom.html', session=session)
            else:
                return redirect(url_for('index.html'))
    return redirect(url_for("student_login"))


@socketio.on('join', namespace='/chat')
def join(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('username') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room=room)


@app.post('/predict')
def predict():
    text = request.get_json().get("message")
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)


@app.route('/dropsession')
def drop_session():
    session.pop('user', None)
    return render_template('main.html')


if __name__ == '__main__':
    app.run(debug=True)
