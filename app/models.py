from flask_login import UserMixin

from .firestore_service import get_user


class UserData:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


class UserModel(UserMixin):
    def __init__(self, user_data):
        """
        :param user_data: UserData
        """
        self.id = user_data.id
        self.username = user_data.username
        self.password = user_data.password

    @staticmethod
    def query(user_id):
        user_doc = get_user(user_id)
        user_data = UserData(
            user_doc.id, user_doc.to_dict()['username'],
            user_doc.to_dict()['password'])
        return UserModel(user_data)
