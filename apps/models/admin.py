from apps.models.models import User, Admin
from apps.models import db
from apps.models.general import search_data, handle_modify_info, handle_change_password
import re

# from apps.models.models import conn_database
# session = conn_database()

session = db.session


class AdminManager:
    def __init__(self, datadict, handle_type):
        self._datadict = datadict
        if handle_type == 'change_user_password':
            self.data = self._change_user_password()
        if handle_type == 'delete_user':
            self.data = self._delete_user()
        if handle_type == 'add_user':
            self.data = self._add_user()
        if handle_type == 'modify_user_info':
            self.data = self._modify_user_info()
        if handle_type == 'get_all_users':
            self.data = self._get_all_users()
        if handle_type == 'check_admin':
            self.data = self._check_admin()

    def _add_user(self):
        if not session.query(User).filter_by(username=self._datadict.get('username')).first():
            try:
                user = User(
                    username=self._datadict.get('username'),
                    password=self._datadict.get('password'),
                    author=self._datadict.get('author'),
                    name=self._datadict.get('name'),
                    sex=self._datadict.get('sex'),
                    email=self._datadict.get('email'),
                    phone=self._datadict.get('phone'),
                )
                session.add(user)
                session.commit()
                return {'message': 'The user added successfully', 'result': True}
            except Exception as e:
                session.rollback()
                return {'message': re.findall(r'.+"(.+)"', str(e))[0], 'result': False}
        return {'message': 'The current user already exists, please change the user account', 'result': False}

    def _change_user_password(self):
        if session.query(User).filter_by(username=self._datadict.get('username')).first():
            username, new_pwd = self._datadict.get('username'), self._datadict.get('password')
            return handle_change_password(User, new_pwd, condition={'username': username})
        return {'message': 'The current user does not exist', 'result': False}

    def _delete_user(self):
        if session.query(User).filter_by(username=self._datadict.get('username')).first():
            try:
                session.query(User).filter_by(username=self._datadict.get('username')).delete()
                session.commit()
                return {'message': 'The user has been successfully deleted', 'result': True}
            except Exception as e:
                session.rollback()
                return {'message': re.findall(r'.+"(.+)"', str(e))[0], 'result': False}
        return {'message': 'The current user does not exist', 'result': False}

    def _modify_user_info(self):
        return handle_modify_info(User, self._datadict, key='username')

    def _get_all_users(self):
        page, all_page, users = search_data(table=User, datadict=self._datadict)
        all_user = []
        if users:
            for user in users:
                data = {
                    'username': user.username,
                    'name': user.name,
                    'sex': user.sex,
                    'email': user.email,
                    'phone': user.phone,
                    'author': user.author
                }
                all_user.append(data)
            all_data = {'current_page': page, 'all_page': all_page, 'users': all_user}
            return {'message': 'success', 'result': True, 'data': all_data}
        return {'message': 'There are currently no users', 'result': False}

    def _check_admin(self):
        if session.query(Admin).filter_by(username=self._datadict.get('username')).first():
            return {'message': 'The current user is a legitimate user', 'result': True}
        return {'message': 'The current user is an illegal user', 'result': False}
