class Announcement:
    count_id = 0

    def __init__(self, id_num, adate, atitle, acontent, afiles, update):
        Announcement.count_id += 1
        self.__id_num = id_num
        self.__ann_id = Announcement.count_id
        self.__atitle = atitle
        self.__acontent = acontent
        self.__adate = adate
        self.__afiles = afiles
        self.__update = update

    def get_id_num(self):
        return self.__id_num

    def get_date(self):
        return self.__adate

    def get_ann_id(self):
        return self.__ann_id

    def get_title(self):
        return self.__atitle

    def get_content(self):
        return self.__acontent

    def get_files(self):
        return self.__afiles

    def set_id_num(self, id_num):
        self.__id_num = id_num

    def set_title(self, atitle):
        self.__atitle = atitle

    def set_content(self, acontent):
        self.__acontent = acontent

    def set_ann_id(self, ann_id):
        self.__ann_id = ann_id

    def set_date(self, adate):
        self.__adate = adate

    def set_files(self, afiles):
        self.__afiles = afiles

    def set_update(self, update):
        self.__update = update

    def get_update(self):
        return self.__update
