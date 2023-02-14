class Content:
    count_id = 0

    def __init__(self, content_subject, cname, cfile):
        Content.count_id += 1
        self.__cid = Content.count_id
        self.__content_subject = content_subject
        self.__cname = cname
        self.__cfile = cfile

    def get_cid(self):
        return self.__cid

    def get_cname(self):
        return self.__cname

    def get_cfile(self):
        return self.__cfile

    def get_content_subject(self):
        return self.__content_subject

    def set_cid(self, cid):
        self.__cid = cid

    def set_cname(self, cname):
        self.__cname = cname

    def set_cfile(self, cfile):
        self.__cfile = cfile

    def set_content_subject(self, content_subject):
        self.__content_subject = content_subject
