from StudentContent import StudentContent


class Test(StudentContent):
    def __init__(self, content_id, content_subject, marks, q1, a1, q2, a2, q3, a3):
        super().__init__(content_id, content_subject)

        self.__marks = marks
        self.__q1 = q1
        self.__a1 = a1
        self.__q2 = q2
        self.__a2 = a2
        self.__q3 = q3
        self.__a3 = a3

    def set_marks(self, marks):
        self.__marks = marks

    def set_q1(self, q1):
        self.__q1 = q1

    def set_a1(self, a1):
        self.__a1 = a1

    def set_q2(self, q2):
        self.__q2 = q2

    def set_a2(self, a2):
        self.__a2 = a2
        
    def set_q3(self, q3):
        self.__q3 = q3

    def set_a3(self, a3):
        self.__a3 = a3

    def get_marks(self):
        return self.__marks

    def get_q1(self):
        return self.__q1

    def get_a1(self):
        return self.__a1

    def get_q2(self):
        return self.__q2

    def get_a2(self):
        return self.__a2
    
    def get_q3(self):
        return self.__q3

    def get_a3(self):
        return self.__a3
