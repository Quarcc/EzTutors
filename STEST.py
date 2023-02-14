from StudentContent import StudentContent


class STest(StudentContent):
    def __init__(self, content_id, content_subject, a1, a2, a3):
        super().__init__(content_id, content_subject)

        self.__a1 = a1
        self.__a2 = a2
        self.__a3 = a3

    def set_a1(self, a1):
        self.__a1 = a1

    def set_a2(self, a2):
        self.__a2 = a2

    def set_a3(self, a3):
        self.__a3 = a3

    def get_a1(self):
        return self.__a1

    def get_a2(self):
        return self.__a2

    def get_a3(self):
        return self.__a3

