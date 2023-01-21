import hashlib

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_hash(self, password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ).decode('utf-8', 'ignore')

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_all(self):
        return self.session.query(User).all()

    def create(self, user_data):
        hash_password = self.get_hash(user_data.get('password', None))
        user_data['password'] = hash_password
        user = User(**user_data)
        self.session.add(user)
        self.session.commit()
        return user

    def update(self, user_data):
        user = self.get_one(user_data.get('id'))
        user.id = user_data.get('id')
        user.username = user_data.get('username')
        user.password = self.get_hash(user_data.get('password'))
        user.role = user_data.get('role')

        self.session.add(user)
        self.session.commit()

    def delete(self, uid):
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()

    def search_by_login(self, login):
        user = self.session.query(User).filter(User.username == login).first()
        if user is None:
            return None
        return user


