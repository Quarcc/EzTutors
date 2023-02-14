class Feedback:
    count_id = 0

    def __init__(self, feedback_adminid, feedback_subject, feedback_title, feedback_description,
                 feedback_name,
                 feedback_date, feedback_file):
        Feedback.count_id += 1
        self.__feedback_id = Feedback.count_id
        self.__feedback_adminid = feedback_adminid
        self.__feedback_subject = feedback_subject
        self.__feedback_title = feedback_title
        self.__feedback_description = feedback_description
        self.__feedback_name = feedback_name
        self.__feedback_date = feedback_date
        self.__feedback_file = feedback_file

    def get_feedback_id(self):
        return self.__feedback_id

    def get_feedback_adminid(self):
        return self.__feedback_adminid

    def get_feedback_subject(self):
        return self.__feedback_subject

    def get_feedback_title(self):
        return self.__feedback_title

    def get_feedback_description(self):
        return self.__feedback_description

    def get_feedback_name(self):
        return self.__feedback_name

    def get_feedback_date(self):
        return self.__feedback_date

    def get_feedback_file(self):
        return self.__feedback_file

    def set_feedback_id(self, feedback_id):
        self.__feedback_id = feedback_id

    def set_feedback_adminid(self, feedback_adminid):
        self.__feedback_adminid = feedback_adminid

    def set_feedback_subject(self, feedback_subject):
        self.__feedback_subject = feedback_subject

    def set_feedback_title(self, feedback_title):
        self.__feedback_title = feedback_title

    def set_feedback_description(self, feedback_description):
        self.__feedback_description = feedback_description

    def set_feedback_name(self, feedback_name):
        self.__feedback_name = feedback_name

    def set_feedback_date(self, feedback_date):
        self.__feedback_date = feedback_date

    def set_feedback_file(self, feedback_file):
        self.__feedback_file = feedback_file
