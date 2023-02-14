class Notification:
    count_id = 0

    def __init__(self, upload_date, title, description, target_user, sender):
        Notification.count_id += 1
        self.__notif_id = Notification.count_id
        self.__upload_date = upload_date
        self.__title = title
        self.__description = description
        self.__target_user = target_user
        self.__sender = sender

    def set_notif_id(self, notif_id):
        self.__notif_id = notif_id
        
    def get_notif_id(self):
        return self.__notif_id
    
    def set_upload_date(self, upload_date):
        self.__upload_date = upload_date
        
    def get_upload_date(self):
        return self.__upload_date
    
    def set_title(self, title):
        self.__title = title
        
    def get_title(self):
        return self.__title
    
    def set_description(self, description):
        self.__description = description
        
    def get_description(self):
        return self.__description

    def set_target_user(self, target_user):
        self.__target_user = target_user

    def get_target_user(self):
        return self.__target_user
    
    def set_sender(self, sender):
        self.__sender = sender

    def get_sender(self):
        return self.__sender
