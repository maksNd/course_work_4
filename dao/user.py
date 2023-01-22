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

    def update(self, user_data, email):
        user = self.search_by_email(email)
        if user_data.get('email') is not None:
            user.email = user_data.get('email')
        if user_data.get('name') is not None:
            user.name = user_data.get('name')
        if user_data.get('surname') is not None:
            user.surname = user_data.get('surname')
        if user_data.get('favorite_genre') is not None:
            user.favorite_genre = user_data.get('favorite_genre')
        if user_data.get('password') is not None:
            new_password = self.get_hash(user_data.get('password'))
            user.password = new_password

        # user = self.get_one(user_data.get('id'))
        # user.id = user_data.get('id')
        # user.email = user_data.get('email')
        # user.password = self.get_hash(user_data.get('password'))
        # user.name = user_data.get('name')
        # user.surname = user_data.get('surname')
        # user.favorite_genre = user_data.get('favorite_genre')

        self.session.add(user)
        self.session.commit()

    def delete(self, uid):
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()

    def search_by_email(self, email):
        user = self.session.query(User).filter(User.email == email).first()
        if user is None:
            return None
        return user


