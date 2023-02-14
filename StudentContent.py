class StudentContent:
    def __init__(self, content_id, content_subject):
        self.__content_id = content_id
        self.__content_subject = content_subject

    def set_content_id(self, content_id):
        self.__content_id = content_id
    
    def set_content_subject(self, content_subject):
        self.__content_subject = content_subject

    def get_content_id(self):
        return self.__content_id

    def get_content_subject(self):
        return self.__content_subject



