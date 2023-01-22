import hashlib
import datetime
import calendar
import jwt

from dao.user import UserDAO
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS, SECRET, ALGO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, data):
        return self.dao.create(data)

    def update(self, user_data, email):
        return self.dao.update(user_data, email)

    def delete(self, uid):
        return self.dao.delete(uid)

    def get_hash(self, password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ).decode('utf-8', 'ignore')

    def generate_jwt(self, email, secret=SECRET, algo=ALGO):

        user_obj = {'email': email}

        days2 = datetime.datetime.utcnow() + datetime.timedelta(days=2)  # задаем время жизни токена
        user_obj['exp'] = calendar.timegm(days2.timetuple())  # кол-во секунд с января 1970 (дата истечения jwt)
        access_token = jwt.encode(user_obj, secret, algo)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)  # задаем время жизни токена
        user_obj['exp'] = calendar.timegm(days130.timetuple())  # кол-во секунд с января 1970 (дата истечения jwt)
        refresh_token = jwt.encode(user_obj, secret, algorithm=algo)
        return {'access_token': access_token, 'refresh_token': refresh_token}

    def search_by_email(self, email):
        return self.dao.search_by_email(email)

    def check_token(self, token, secret=SECRET, algo=ALGO):
        try:
            jwt.decode(token, secret, algorithms=algo)
            return True
        except Exception:
            return False

    def check_email_password_confirmance(self, email, password):
        user = self.dao.search_by_email(email)
        if user is None:
            return False
        if user.password != self.get_hash(password):
            return False
        return True

    def check_token_email_conformance(self, email, token, secret=SECRET, algo=ALGO):
        if self.search_by_email(email) is None:
            return False
        if self.check_token(token) is False:
            return False
        if email != jwt.decode(token, secret, algorithms=algo)['email']:
            return False
        return True
